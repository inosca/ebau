from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.utils import mark_work_items_as_imported
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaListAnswerWriter,
    CalumaPlotDataWriter,
    CaseMetaWriter,
    DossierWriter,
)
from camac.instance.domain_logic.decision import DecisionLogic
from camac.instance.models import Instance

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
    id = CalumaAnswerWriter(
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
    decision_date = CalumaAnswerWriter(target="entscheid-datum", task="decision")
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

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)
        work_items = instance.case.work_items.all()
        mark_work_items_as_imported(work_items)

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

    def get_workflow_skip_path(self, instance: Instance, dossier: Dossier) -> list[str]:
        """Return the skip path per target state."""
        SUBMITTED = ["submit"]
        DECIDED = SUBMITTED + [
            "formal-exam",
            "material-exam",
            "distribution",
            "decision",
        ]
        REJECTED = DECIDED + ["complete-instance"]
        DONE = DECIDED + ["init-construction-monitoring", "complete-instance"]

        return {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: DECIDED,
            TargetStatus.REJECTED.value: REJECTED,
            TargetStatus.WRITTEN_OFF.value: DECIDED,
            TargetStatus.DONE.value: DONE,
        }[dossier._meta.target_state]

    def before_skip_work_item(
        self, work_item: WorkItem, instance: Instance, dossier: Dossier
    ):
        """Correct instance state for written-off dossiers.

        A written-off dossier needs the same post-decision handling as a
        withdrawal, which depends on the instance being in the withdrawal state
        while the decision work item is completed.
        """
        super().before_skip_work_item(work_item, instance, dossier)

        if (
            work_item.task_id == "decision"
            and dossier._meta.target_state == TargetStatus.WRITTEN_OFF.value
        ):
            # Set instance state to withdrawal so that the workflow creates the
            # correct work items. This will be resetted afterwards in the
            # `post_complete_decision_building_permit` method
            instance.set_instance_state(
                settings.WITHDRAWAL["INSTANCE_STATE"], self._user
            )
            DecisionLogic.post_complete_decision_building_permit(
                instance, work_item, self._caluma_user, self._user
            )

    def write_decision_form(self, decision_work_item: WorkItem, dossier: Dossier):
        """Write the decision including a construction tee without restoration.

        Additionally answer the "Bauabschlag" question with "Ohne
        Wiederherstellung" in order to not cause a construction monitoring
        process for rejected dossiers.
        """
        super().write_decision_form(decision_work_item, dossier)

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
