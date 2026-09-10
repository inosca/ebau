from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

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
    CalumaPlotDataWriter,
    CalumaTableAnswerWriter,
    DossierWriter,
    EbauNumberWriter,
    ResponsibleUserWriter,
    SubmitDateWriter,
)
from camac.instance.domain_logic import SUBMIT_DATE_FORMAT, CreateInstanceLogic
from camac.instance.domain_logic.decision import DecisionLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.instance.utils import get_construction_control, set_construction_control
from camac.permissions.events import core as permissions_events
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

    id = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string", protected=True
    )
    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben", protected=True)
    cantonal_id = EbauNumberWriter(target="ebau-number")
    plot_data = CalumaPlotDataWriter(
        target="parzelle", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungszone")
    application_type = CalumaAnswerWriter(target="geschaeftstyp-import")
    submit_date = SubmitDateWriter()
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
    applicant = CalumaTableAnswerWriter(
        target="personalien-gesuchstellerin",
        column_mapping=APPLICANT_MAPPING,
        value_mapping={
            "is_juristic_person": {
                True: "juristische-person-gesuchstellerin-ja",
                False: "juristische-person-gesuchstellerin-nein",
            }
        },
    )
    landowner = CalumaTableAnswerWriter(
        target="personalien-grundeigentumerin",
        column_mapping=LANDOWNER_MAPPING,
        value_mapping={
            "is_juristic_person": {
                True: "juristische-person-grundeigentuemerin-ja",
                False: "juristische-person-grundeigentuemerin-nein",
            }
        },
    )
    project_author = CalumaTableAnswerWriter(
        target="personalien-projektverfasserin",
        column_mapping=PROJECTAUTHOR_MAPPING,
        value_mapping={
            "is_juristic_person": {
                True: "juristische-person-projektverfasserin-ja",
                False: "juristische-person-projektverfasserin-nein",
            }
        },
    )

    responsible = ResponsibleUserWriter(target="TODO_RESPONSIBLE_SERVICE__USER")

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

        creation_data = {
            "instance_state": instance_state,
            "previous_instance_state": instance_state,
            "user": self._user,
            "group": self._group,
            "form": Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        }

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
            skip_applicant_creation=True,
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
        permissions_events.Trigger.instance_submitted(None, instance)
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
        answers = []
        triage_question = "weitere-personen"
        for table_question in [
            "grundeigentumerin",
            "projektverfasserin",
        ]:
            if (
                table_answer := instance.case.document.answers.filter(
                    question_id=f"personalien-{table_question}"
                ).first()
            ) and table_answer.documents.exists():
                value = f"{triage_question}-{table_question}"
                answers.append(value)
        form_api.save_answer(
            document=instance.case.document,
            question=Question.objects.get(pk=triage_question),
            value=answers,
            user=self._caluma_user,
        )

    def get_existing_dossier_ids(self, dossier_ids):
        return list(
            Tags.objects.filter(
                name__in=dossier_ids, service=self._group.service
            ).values_list("name", flat=True)
        )

    def find_existing_instance(self, dossier, user):
        return (
            tag := Tags.objects.filter(
                name=dossier.id, service=self._group.service
            ).first()
        ) and tag.instance

    def link_instance_and_dossier(self, instance, dossier, user):
        """Make the instance retrievable by the dossier.

        The reverse of `self.find_existing_instance`
        :param instance:
        :param dossier:
        :param user:
        """
        Tags.objects.create(
            name=dossier.id, service=self._group.service, instance=instance
        )
        construction_control = get_construction_control(self._group.service)
        Tags.objects.create(
            name=dossier.id, service=construction_control, instance=instance
        )

    def _post_create_instance(self, instance, dossier):
        save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gemeinde"),
            value=str(self._group.service_id),
            user=self._caluma_user,
        )

    def get_workflow_skip_path(self, instance: Instance, dossier: Dossier) -> list[str]:
        """Return the skip path for the building-permit and preliminary workflows.

        The `PRELIMINARY` workflow ends at the decision, so its `DONE` path does
        not include the post-decision building-permit tasks (`sb1`, `sb2`,
        `complete`).
        """
        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + ["ebau-number", "distribution", "decision"]
        DONE = DECIDED + ["sb1", "sb2", "complete"]

        if dossier._meta.workflow == "PRELIMINARY":
            DONE = DECIDED

        return {
            "SUBMITTED": SUBMITTED,
            "APPROVED": DECIDED,
            "REJECTED": DECIDED,
            "WRITTEN OFF": DECIDED,
            "DONE": DONE,
        }[dossier._meta.target_state]

    def after_skip_work_item(
        self, work_item: WorkItem, instance: Instance, dossier: Dossier
    ):
        """Set up the construction control and, for `SUBMITTED`, the ebau number.

        After the decision, the construction control service is granted access
        so it can take over. When only importing up to `SUBMITTED`, the ebau
        number work item is skipped and its form filled so the case lands in the
        correct instance state (circulation vs. submitted).
        """
        if (
            work_item.task_id == "decision"
            and DecisionLogic.should_continue_after_decision(instance, work_item)
        ):
            set_construction_control(instance)

        if dossier._meta.target_state == "SUBMITTED":
            if instance.case.meta.get("ebau-number"):
                ebau_work_item = instance.case.work_items.get(task_id="ebau-number")
                skip_work_item(
                    ebau_work_item,
                    user=self._caluma_user,
                    context=self.get_skip_context(ebau_work_item),
                )
                self.write_ebau_number_form(instance, ebau_work_item, dossier)
                instance.instance_state = InstanceState.objects.get(
                    name="circulation_init"
                )
            else:
                instance.instance_state = InstanceState.objects.get(name="subm")
            instance.save()

        super().after_skip_work_item(work_item, instance, dossier)

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
                    detail=_(
                        "Failed to write %(value)s to %(target)s for dossier %(dossier)s"
                    )
                    % {
                        "value": value,
                        "target": ebau_number_slug,
                        "dossier": instance,
                    },
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
                    detail=_(
                        "Failed to write %(value)s to %(target)s for dossier %(dossier)s"
                    )
                    % {
                        "value": f"'{exists_slug}-yes'",
                        "target": exists_slug,
                        "dossier": instance,
                    },
                )
            )
            return

    def get_decision_answer_value(self, dossier: Dossier) -> str:
        """Map the target state to a decision answer, per workflow.

        The building-permit and preliminary-clarification workflows use
        different decision answers (e.g. approved/rejected vs.
        positive/negative, and depreciated for a written-off building permit).
        """
        decision = settings.DECISION["ANSWERS"]["DECISION"]
        decision_mapping = {
            "BUILDINGPERMIT": {
                TargetStatus.APPROVED.value: decision["APPROVED"],
                TargetStatus.REJECTED.value: decision["REJECTED"],
                TargetStatus.WRITTEN_OFF.value: decision["DEPRECIATED"],
                TargetStatus.DONE.value: decision["APPROVED"],
            },
            "PRELIMINARY": {
                TargetStatus.APPROVED.value: decision["POSITIVE"],
                TargetStatus.REJECTED.value: decision["NEGATIVE"],
                TargetStatus.WRITTEN_OFF.value: decision["NEGATIVE"],
                TargetStatus.DONE.value: decision["POSITIVE"],
            },
        }

        return decision_mapping[dossier._meta.workflow][dossier._meta.target_state]

    def write_decision_form(self, decision_work_item: WorkItem, dossier: Dossier):
        """Write the decision form including an unknown approval type.

        The approval type is not available from the import, so building-permit
        decisions get the `UNKNOWN` approval type.
        """
        super().write_decision_form(decision_work_item, dossier)

        if dossier._meta.workflow == "BUILDINGPERMIT":
            form_api.save_answer(
                document=decision_work_item.document,
                question=Question.objects.get(
                    pk=settings.DECISION["QUESTIONS"]["APPROVAL_TYPE"]
                ),
                value=settings.DECISION["ANSWERS"]["APPROVAL_TYPE"]["UNKNOWN"],
                user=self._caluma_user,
            )
