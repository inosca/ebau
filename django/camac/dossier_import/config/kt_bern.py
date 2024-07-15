from typing import List

from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from rest_framework.exceptions import ValidationError

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.core.models import InstanceService
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import (
    Message,
    MessageCodes,
    Severity,
)
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaListAnswerWriter,
    CalumaPlotDataWriter,
    CaseMetaWriter,
    DossierWriter,
    EbauNumberWriter,
)
from camac.instance.domain_logic import SUBMIT_DATE_FORMAT, CreateInstanceLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.instance.utils import get_construction_control, set_construction_control
from camac.tags.models import Tags

APPLICANT_MAPPING = {
    "is_juristic_person": "juristische-person-gesuchstellerin",
    "company": "name-juristische-person-gesuchstellerin",
    "last_name": "name-gesuchstellerin",
    "first_name": "vorname-gesuchstellerin",
    "street": "strasse-gesuchstellerin",
    "street_number": "nummer-gesuchstellerin",
    "zip": "plz-gesuchstellerin",
    "town": "ort-gesuchstellerin",
    "phone": "telefon-oder-mobile-gesuchstellerin",
    "email": "e-mail-gesuchstellerin",
}

LANDOWNER_MAPPING = {
    "is_juristic_person": "juristische-person-grundeigentuemerin",
    "company": "name-juristische-person-grundeigentuemerin",
    "last_name": "name-grundeigentuemerin",
    "first_name": "vorname-grundeigentuemerin",
    "street": "strasse-grundeigentuemerin",
    "street_number": "nummer-grundeigentuemerin",
    "zip": "plz-grundeigentuemerin",
    "town": "ort-grundeigentuemerin",
    "phone": "telefon-oder-mobile-grundeigentuemerin",
    "email": "e-mail-grundeigentuemerin",
}

PROJECTAUTHOR_MAPPING = {
    "is_juristic_person": "juristische-person-projektverfasserin",
    "company": "name-juristische-person-projektverfasserin",
    "last_name": "name-projektverfasserin",
    "first_name": "vorname-projektverfasserin",
    "street": "strasse-projektverfasserin",
    "street_number": "nummer-projektverfasserin",
    "zip": "plz-projektverfasserin",
    "town": "ort-projektverfasserin",
    "phone": "telefon-oder-mobile-projektverfasserin",
    "email": "e-mail-projektverfasserin",
}

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid-nr",
    "coord_east": "lagekoordinaten-ost",
    "coord_north": "lagekoordinaten-nord",
}


class KtBernDossierWriter(DossierWriter):
    """
    Dossier writer for importing dossiers from a ZIP archive.

    This writer assumes that the ZIP archive contains the following structure:

    - dossiers.xlsx containing metadata as well as form data (one line per dossier)
    - for each dossier: optionally a directory (named after the first column in dossier.xlsx)
      containing the documents to be attached to the dossier.
    """

    id: str = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string"
    )
    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben")
    cantonal_id = EbauNumberWriter(target="ebau-number")
    plot_data = CalumaPlotDataWriter(
        target="parzelle", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungszone")
    application_type = CalumaAnswerWriter(target="geschaeftstyp-import")
    submit_date = CaseMetaWriter(target="submit-date", formatter="datetime-to-string")
    decision_date = CalumaAnswerWriter(target="decision-date", task="decision")
    publication_date = CalumaAnswerWriter(target="datum-publikation")
    construction_start_date = CalumaAnswerWriter(target="datum-baubeginn")
    profile_approval_date = CalumaAnswerWriter(target="datum-schnurgeruestabnahme")
    final_approval_date = CalumaAnswerWriter(target="datum-schlussabnahme")
    completion_date = CalumaAnswerWriter(target="bauende")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    street = CalumaAnswerWriter(target="strasse-flurname")
    street_number = CalumaAnswerWriter(target="nr", formatter="to-string")
    city = CalumaAnswerWriter(target="ort-grundstueck")
    applicant = CalumaListAnswerWriter(
        target="personalien-gesuchstellerin",
        column_mapping=APPLICANT_MAPPING,
        value_mapping={
            "is_juristic_person": {
                True: "juristische-person-gesuchstellerin-ja",
                False: "juristische-person-gesuchstellerin-nein",
            }
        },
    )
    landowner = CalumaListAnswerWriter(
        target="personalien-grundeigentumerin",
        column_mapping=LANDOWNER_MAPPING,
        value_mapping={
            "is_juristic_person": {
                True: "juristische-person-grundeigentuemerin-ja",
                False: "juristische-person-grundeigentuemerin-nein",
            }
        },
    )
    project_author = CalumaListAnswerWriter(
        target="personalien-projektverfasserin",
        column_mapping=PROJECTAUTHOR_MAPPING,
        value_mapping={
            "is_juristic_person": {
                True: "juristische-person-projektverfasserin-ja",
                False: "juristische-person-projektverfasserin-nein",
            }
        },
    )

    def create_instance(self, dossier: Dossier) -> Instance:
        """Create a Camac NG Instance with a case.

        camac.instance.domain_logic.CreateInstanceLogic should be able to do the job and
        spit out a reasonably generic starting point.
        """
        instance_state = InstanceState.objects.get(
            pk=settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"]
            .get(dossier._meta.workflow, {})
            .get(dossier._meta.target_state)
        )

        creation_data = dict(
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=self._user,
            group=self._group,
            form=Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        )

        workflow_slug = {
            "BUILDINGPERMIT": "building-permit",
            "PRELIMINARY": "preliminary-clarification",
        }

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=self._caluma_user,
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.DOSSIER_IMPORT["CALUMA_FORM"]
            ),
            start_caluma=True,
            workflow_slug=workflow_slug[dossier._meta.workflow],
        )

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )
        meta = {
            "submit-date": dossier.submit_date.strftime(SUBMIT_DATE_FORMAT),
        }

        instance.case.meta.update(meta)
        instance.case.save()

        return instance

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed
        if the associated triage question whether the data is different from the
        applicant is answered with yes. This method checks if there is any data
        in the personal table and answers the triage question accordingly.
        """

        pass  # TODO: do something similar to kt_so e. g. below
        # for table_question in [
        #     "personalien-grundeigentuemerin",
        #     "personalien-projektverfasserin",
        #     # As the invoice recipient can not be passed to the import, the
        #     # table will always be empty and the triage question will always be
        #     # answered with "no". However, we still use the same logic as for
        #     # the others in order to avoid more code.
        #     "personalien-rechnungsempfaengerin",
        # ]:
        # table_answer = instance.case.document.answers.filter(
        #     question_id=table_question
        # ).first()
        # has_rows = table_answer.documents.exists() if table_answer else False

        # suffix = "ja" if has_rows else "nein"
        # triage_question = f"{table_question}-abweichend"
        # value = f"{triage_question}-{suffix}"

        # form_api.save_answer(
        #     document=instance.case.document,
        #     question=Question.objects.get(pk=triage_question),
        #     value=value,
        #     user=self._caluma_user,
        # )

    def existing_dossier(self, dossier_id):
        return (
            tag := Tags.objects.filter(
                name=dossier_id, service=self._group.service
            ).first()
        ) and tag.instance

    def set_dossier_id(self, instance, dossier_id):
        """Make the instance retrievable by dossier_id."""
        Tags.objects.create(
            name=dossier_id, service=self._group.service, instance=instance
        )
        construction_control = get_construction_control(self._group.service)
        Tags.objects.create(
            name=dossier_id, service=construction_control, instance=instance
        )

    def _post_create_instance(self, instance, dossier):
        save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gemeinde"),
            value=str(self._group.service_id),
            user=self._caluma_user,
        )

    def _set_workflow_state(  # noqa: C901
        self,
        instance: Instance,
        dossier,
    ) -> List[Message]:
        """Advance instance's case through defined workflow sequence to target state.

        In order to advance to a specified worklow state after every flow all tasks need to be
        in a status other than ready so that the relevant work_item can be completed.

        Therefore every target_state needs to be informed on the sibling work-items and how to handle
        them before completion and progression to the next task in line.

        This is configured in the following:

        <TARGETSTATE> = [
            (<task_to_complete>: [<task_to_sikp>, ... ]),
            ...
        ]

        If required this could be extended with the option to handle sibling tasks differently on each stage, such
         as cancelling them instead of skipping.
        """
        messages = []
        target_state = dossier._meta.target_state

        # configure workflow state advance path and strategies (skip | cancel)
        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + ["ebau-number", "distribution", "decision"]
        DONE = DECIDED + ["sb1", "sb2", "complete"]

        if dossier._meta.workflow == "PRELIMINARY":
            DONE = DECIDED

        path_to_state = {
            "SUBMITTED": SUBMITTED,
            "APPROVED": DECIDED,
            "REJECTED": DECIDED,
            "WRITTEN OFF": DECIDED,
            "DONE": DONE,
        }

        default_context = {"no-notification": True, "no-history": True}

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except WorkItem.DoesNotExist as e:
                messages.append(
                    Message(
                        level=Severity.ERROR.value,
                        code=MessageCodes.WORKFLOW_SKIP_ITEM_FAILED.value,
                        detail=(
                            f"Skip work item with task_id {task_id} failed with "
                            f"{DossierWriter.ConfigurationError(e)}."
                        ),
                    )
                )
                continue

            if task_id == "decision":
                self.write_decision_form(work_item, dossier)

            config = get_caluma_setting("PRE_COMPLETE") and get_caluma_setting(
                "PRE_COMPLETE"
            ).get(work_item.task_id)
            if config:
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, self._caluma_user)
            skip_work_item(work_item, user=self._caluma_user, context=default_context)
            if task_id == "decision":
                set_construction_control(instance)
            if target_state == "SUBMITTED":
                if instance.case.meta.get("ebau-number"):
                    work_item = instance.case.work_items.get(task_id="ebau-number")
                    skip_work_item(
                        work_item, user=self._caluma_user, context=default_context
                    )
                    self.write_ebau_number_form(instance, work_item, dossier)
                    instance.instance_state = InstanceState.objects.get(
                        name="circulation_init"
                    )
                else:
                    instance.instance_state = InstanceState.objects.get(name="subm")
                instance.save()
        messages.append(  # pragma: no cover
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=f"Workflow state set to {target_state}.",
            )
        )
        return messages

    def write_ebau_number_form(self, instance, ebau_number_work_item, dossier):
        document = ebau_number_work_item.document
        ebau_number_slug = "ebau-number-existing"
        question = Question.objects.get(slug=ebau_number_slug)
        value = instance.case.meta.get("ebau-number")
        try:
            save_answer(
                question=question,
                document=document,
                value=value,
                user=self._caluma_user,
            )
        except ValidationError:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=f"Failed to write {value} to {ebau_number_slug} for dossier {instance}",
                )
            )
            return
        exists_slug = "ebau-number-has-existing"
        question_exists = Question.objects.get(slug=exists_slug)
        try:
            save_answer(
                question=question_exists,
                document=document,
                value=f"{exists_slug}-yes",
                user=self._caluma_user,
            )
        except ValidationError:  # pragma: no cover
            dossier._meta.errors.append(
                Message(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    detail=f"Failed to write '{exists_slug}-yes' to {exists_slug} for dossier {instance}",
                )
            )
            return

    def write_decision_form(self, decision_work_item, dossier):
        decision_mapping = {
            "BUILDINGPERMIT": {
                TargetStatus.APPROVED.value: settings.DECISION["ANSWERS"]["DECISION"][
                    "APPROVED"
                ],
                TargetStatus.REJECTED.value: settings.DECISION["ANSWERS"]["DECISION"][
                    "REJECTED"
                ],
                TargetStatus.WRITTEN_OFF.value: settings.DECISION["ANSWERS"][
                    "DECISION"
                ]["DEPRECIATED"],
                TargetStatus.DONE.value: settings.DECISION["ANSWERS"]["DECISION"][
                    "APPROVED"
                ],
            },
            "PRELIMINARY": {
                TargetStatus.APPROVED.value: settings.DECISION["ANSWERS"]["DECISION"][
                    "POSITIVE"
                ],
                TargetStatus.REJECTED.value: settings.DECISION["ANSWERS"]["DECISION"][
                    "NEGATIVE"
                ],
                TargetStatus.WRITTEN_OFF.value: settings.DECISION["ANSWERS"][
                    "DECISION"
                ]["NEGATIVE"],
                TargetStatus.DONE.value: settings.DECISION["ANSWERS"]["DECISION"][
                    "POSITIVE"
                ],
            },
        }
        form_api.save_answer(
            document=decision_work_item.document,
            question=Question.objects.get(
                slug=settings.DECISION["QUESTIONS"]["DECISION"]
            ),
            value=decision_mapping[dossier._meta.workflow][dossier._meta.target_state],
            user=self._caluma_user,
        )
        if dossier._meta.workflow == "BUILDINGPERMIT":
            form_api.save_answer(
                document=decision_work_item.document,
                question=Question.objects.get(
                    pk=settings.DECISION["QUESTIONS"]["APPROVAL_TYPE"]
                ),
                value=settings.DECISION["ANSWERS"]["APPROVAL_TYPE"]["UNKNOWN"],
                user=self._caluma_user,
            )
