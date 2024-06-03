from typing import List

from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form as CalumaForm, Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.core.models import InstanceService
from camac.core.utils import generate_sort_key
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
)
from camac.instance.domain_logic import CreateInstanceLogic
from camac.instance.domain_logic.decision import DecisionLogic
from camac.instance.models import Form, Instance, InstanceState
from camac.tags.models import Keyword

PERSON_VALUE_MAPPING = {
    "is_juristic_person": {
        True: "juristische-person-ja",
        False: "juristische-person-nein",
    }
}

PERSON_MAPPING = {
    "is_juristic_person": "juristische-person",
    "company": "juristische-person-name",
    "last_name": "nachname",
    "first_name": "vorname",
    "street": "strasse",
    "street_number": "strasse-nummer",
    "zip": "plz",
    "town": "ort",
    "phone": "telefon",
    "email": "e-mail",
}

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid",
    "coord_east": "lagekoordinaten-ost",
    "coord_north": "lagekoordinaten-nord",
}


class KtSolothurnDossierWriter(DossierWriter):
    id: str = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string", protected=True
    )
    proposal = CalumaAnswerWriter(target="umschreibung-bauprojekt", protected=True)
    cantonal_id = CalumaAnswerWriter(
        target="kantonale-gesuchsnummer", formatter="to-string"
    )
    plot_data = CalumaPlotDataWriter(
        target="parzellen", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungsplanung-grundnutzung")
    application_type = CalumaAnswerWriter(target="geschaeftstyp")
    submit_date = CaseMetaWriter(
        target="submit-date", formatter="datetime-to-string", protected=True
    )
    publication_date = CalumaAnswerWriter(target="datum-publikation")
    construction_start_date = CalumaAnswerWriter(target="datum-baubeginn")
    profile_approval_date = CalumaAnswerWriter(target="datum-schnurgeruestabnahme")
    final_approval_date = CalumaAnswerWriter(target="datum-schlussabnahme")
    completion_date = CalumaAnswerWriter(target="bauende")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    street = CalumaAnswerWriter(target="strasse-flurname")
    street_number = CalumaAnswerWriter(target="strasse-nummer", formatter="to-string")
    city = CalumaAnswerWriter(target="ort")
    applicant = CalumaListAnswerWriter(
        target="bauherrin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    landowner = CalumaListAnswerWriter(
        target="grundeigentuemerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    project_author = CalumaListAnswerWriter(
        target="projektverfasserin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )

    def create_instance(self, dossier: Dossier) -> Instance:
        instance_state = InstanceState.objects.get(
            name=settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"].get(
                dossier._meta.target_state
            )
        )

        creation_data = dict(
            instance_state=instance_state,
            previous_instance_state=instance_state,
            user=self._user,
            group=self._group,
            form=Form.objects.get(pk=settings.DOSSIER_IMPORT["FORM_ID"]),
        )

        instance = CreateInstanceLogic.create(
            creation_data,
            caluma_user=self._caluma_user,
            camac_user=self._user,
            group=self._group,
            caluma_form=CalumaForm.objects.get(
                pk=settings.DOSSIER_IMPORT["CALUMA_FORM"]
            ),
            start_caluma=True,
        )

        InstanceService.objects.create(
            instance=instance,
            service_id=self._group.service_id,
            active=1,
            activation_date=None,
        )

        dossier_number = CreateInstanceLogic.generate_identifier(
            instance, dossier.submit_date.year
        )

        instance.case.meta.update(
            {
                "dossier-number": dossier_number,
                "dossier-number-sort": generate_sort_key(dossier_number),
            }
        )
        instance.case.save()

        return instance

    def existing_dossier(self, dossier_id):
        keyword = Keyword.objects.filter(
            name=dossier_id, service=self._group.service
        ).first()

        return keyword.instances.first() if keyword else None

    def set_dossier_id(self, instance, dossier_id):
        keyword = Keyword.objects.filter(
            name=dossier_id, service=self._group.service
        ).first()

        if keyword:  # pragma: no cover
            # This only happens after an import was undone
            keyword.instances.add(instance)
        else:
            instance.keywords.create(name=dossier_id, service=self._group.service)

    def _post_create_instance(self, instance: Instance, dossier: Dossier):
        save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gemeinde"),
            value=str(self._group.service_id),
            user=self._caluma_user,
        )

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed
        if the associated triage question whether the data is different from the
        applicant is answered with yes. This method checks if there is any data
        in the personal table and answers the triage question accordingly.
        """

        for table_question in [
            "grundeigentuemerin",
            "projektverfasserin",
            # As the invoice recipient can not be passed to the import, the
            # table will always be empty and the triage question will always be
            # answered with "no". However, we still use the same logic as for
            # the others in order to avoid more code.
            "rechnungsempfaengerin",
        ]:
            table_answer = instance.case.document.answers.filter(
                question_id=table_question
            ).first()
            has_rows = table_answer.documents.exists() if table_answer else False

            suffix = "ja" if has_rows else "nein"
            triage_question = f"{table_question}-abweichend"
            value = f"{triage_question}-{suffix}"

            form_api.save_answer(
                document=instance.case.document,
                question=Question.objects.get(pk=triage_question),
                value=value,
                user=self._caluma_user,
            )

    def _set_workflow_state(self, instance: Instance, dossier) -> List[Message]:
        messages = []
        target_state = dossier._meta.target_state

        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + [
            "formal-exam",
            "material-exam",
            "distribution",
            "decision",
        ]
        REJECTED = DECIDED + ["complete-instance"]
        DONE = DECIDED + ["init-construction-monitoring", "complete-instance"]

        path_to_state = {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: DECIDED,
            TargetStatus.REJECTED.value: REJECTED,
            TargetStatus.WRITTEN_OFF.value: DECIDED,
            TargetStatus.DONE.value: DONE,
        }

        default_context = {"no-notification": True, "no-history": True, "skip": True}

        # In order for a work item to be completed no sibling work items can be
        # in state ready. They have to be dealt with in advance.
        for task_id in path_to_state[target_state]:
            try:
                work_item = instance.case.work_items.get(task_id=task_id)
            except WorkItem.DoesNotExist as e:  # pragma: no cover
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

                if target_state == TargetStatus.WRITTEN_OFF.value:
                    # Set instance state to withdrawal so that the workflow
                    # creates the correct work items. This will be resetted
                    # afterwards in the post_complete_decision_building_permit
                    # method
                    instance.set_instance_state(
                        settings.WITHDRAWAL["INSTANCE_STATE"], self._user
                    )
                    DecisionLogic.post_complete_decision_building_permit(
                        instance, work_item, self._caluma_user, self._user
                    )

            if config := get_caluma_setting("PRE_COMPLETE") and get_caluma_setting(
                "PRE_COMPLETE"
            ).get(work_item.task_id):
                for action_name, tasks in config.items():
                    action = getattr(workflow_api, f"{action_name}_work_item")

                    for item in work_item.case.work_items.filter(
                        task_id__in=tasks, status=WorkItem.STATUS_READY
                    ):
                        action(item, self._caluma_user)

            skip_work_item(work_item, user=self._caluma_user, context=default_context)

        messages.append(  # pragma: no cover
            Message(
                level=Severity.DEBUG.value,
                code=MessageCodes.SET_WORKFLOW_STATE.value,
                detail=f"Workflow state set to {target_state}.",
            )
        )

        return messages

    def write_decision_form(self, decision_work_item, dossier):
        decision_mapping = {
            TargetStatus.APPROVED.value: settings.DECISION["ANSWERS"]["DECISION"][
                "APPROVED"
            ],
            TargetStatus.REJECTED.value: settings.DECISION["ANSWERS"]["DECISION"][
                "REJECTED"
            ],
            TargetStatus.WRITTEN_OFF.value: settings.DECISION["ANSWERS"]["DECISION"][
                "WITHDRAWAL"
            ],
            TargetStatus.DONE.value: settings.DECISION["ANSWERS"]["DECISION"][
                "APPROVED"
            ],
        }

        form_api.save_answer(
            document=decision_work_item.document,
            question=Question.objects.get(
                slug=settings.DECISION["QUESTIONS"]["DECISION"]
            ),
            value=decision_mapping[dossier._meta.target_state],
            user=self._caluma_user,
        )

        if dossier._meta.target_state == TargetStatus.REJECTED.value:
            form_api.save_answer(
                document=decision_work_item.document,
                question=Question.objects.get(
                    pk=settings.DECISION["QUESTIONS"]["BAUABSCHLAG"]
                ),
                value=settings.DECISION["ANSWERS"]["BAUABSCHLAG"][
                    "OHNE_WIEDERHERSTELLUNG"
                ],
                user=self._caluma_user,
            )

    def _handle_document(self, *args, **kwargs):
        return self._handle_alexandria_document(*args, **kwargs)
