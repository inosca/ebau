import json

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Question
from django.conf import settings

from camac.caluma.extensions.events.construction_monitoring import (
    can_perform_construction_monitoring,
)
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.utils import mark_work_items_as_imported
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaCombinedStreetAndNumberWriter,
    CalumaListAnswerWriter,
    CalumaPlotDataWriter,
    CaseMetaWriter,
    DossierWriter,
)
from camac.instance.models import Instance, InstanceState
from camac.settings.utils import is_module_enabled

PERSON_VALUE_MAPPING = {
    "is_juristic_person": {
        True: "juristische-person-gesuchstellerin-ja",
        False: "juristische-person-gesuchstellerin-nein",
    }
}

PERSON_MAPPING = {
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

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid-nr",
    "coord_east": "lagekoordinaten-ost",
    "coord_north": "lagekoordinaten-nord",
}


class KtGraubundenDossierWriter(DossierWriter):
    id = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string", protected=True
    )
    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben", protected=True)
    cantonal_id = CalumaAnswerWriter(
        target="kantonale-gesuchsnummer", formatter="to-string"
    )
    plot_data = CalumaPlotDataWriter(
        target="parzelle", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="nutzungsplanung-grundnutzung")
    application_type = CalumaAnswerWriter(target="geschaeftstyp")
    submit_date = CaseMetaWriter(
        target="submit-date", formatter="datetime-to-string", protected=True
    )
    decision_date = CalumaAnswerWriter(target="decision-date", task="decision")
    publication_date = CalumaAnswerWriter(target="datum-publikation")
    construction_start_date = CalumaAnswerWriter(target="datum-baubeginn")
    profile_approval_date = CalumaAnswerWriter(target="datum-schnurgeruestabnahme")
    final_approval_date = CalumaAnswerWriter(target="datum-schlussabnahme")
    completion_date = CalumaAnswerWriter(target="bauende")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    project_cost = CalumaAnswerWriter(target="projektkosten")
    street = CalumaCombinedStreetAndNumberWriter(
        target="street-and-housenumber",
        fields=["street", "street_number"],
    )
    city = CalumaAnswerWriter(target="ort-grundstueck")
    applicant = CalumaListAnswerWriter(
        target="personalien-gesuchstellerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    landowner = CalumaListAnswerWriter(
        target="personalien-grundeigentumerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    project_author = CalumaListAnswerWriter(
        target="personalien-projektverfasserin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )

    def get_instance_state(self, dossier):
        # Todo: remove this clause when construction monitoring is on production.
        instance_state_mapping = settings.DOSSIER_IMPORT["INSTANCE_STATE_MAPPING"]

        if not is_module_enabled("CONSTRUCTION_MONITORING"):  # pragma: no cover
            instance_state_mapping["APPROVED"] = "construction-acceptance"

        return InstanceState.objects.get(
            name=instance_state_mapping.get(dossier._meta.target_state)
        )

    def _post_write_fields(self, instance, dossier):
        self._write_triage_fields(instance)
        self._write_gis_coordinates(instance, dossier)
        work_items = instance.case.work_items.all()
        mark_work_items_as_imported(work_items)

    def _write_triage_fields(self, instance: Instance):
        """Write triage answers for personal data.

        The table questions for landowner, and project author are only displayed if the multi-select contains these values.
        """

        extra_values = []
        for table_question in [
            "personalien-grundeigentumerin",
            "personalien-projektverfasserin",
        ]:
            table_answer = instance.case.document.answers.filter(
                question_id=table_question
            ).first()
            has_rows = table_answer.documents.exists() if table_answer else False
            if has_rows:
                if table_question == "personalien-grundeigentumerin":
                    extra_values.append("weitere-personen-grundeigentumerin")
                elif table_question == "personalien-projektverfasserin":
                    extra_values.append("weitere-personen-projektverfasserin")

        form_api.save_answer(
            document=instance.case.document,
            question=Question.objects.get(pk="weitere-personen"),
            value=extra_values,
            user=self._caluma_user,
        )

    def _write_gis_coordinates(self, instance: Instance, dossier: Dossier):
        coordinates = getattr(dossier, "coordinates", []) or []
        form_api.save_answer(
            document=instance.case.document,
            question=Question.objects.get(slug="gis-map"),
            value=json.dumps(
                {
                    "markers": [{"x": coord.e, "y": coord.n} for coord in coordinates],
                    "geometry": "POINT",
                }
            ),
            user=self._caluma_user,
        )

    def get_workflow_skip_path(self, instance: Instance, dossier: Dossier) -> list[str]:
        """Return the skip path per target state."""
        SUBMITTED = ["submit"] + (
            [settings.CONSTRUCTION_MONITORING.get("INIT_CONSTRUCTION_MONITORING_TASK")]
            if can_perform_construction_monitoring(instance)
            else []
        )
        DECIDED = SUBMITTED + [
            "formal-exam",
            "distribution",
            "decision",
        ]
        REJECTED = DECIDED + ["create-manual-workitems", "complete-instance"]
        DONE = (
            DECIDED
            + ["create-manual-workitems"]
            + (
                []
                if is_module_enabled("CONSTRUCTION_MONITORING")
                else ["construction-acceptance"]
            )
            + ["complete-instance"]
        )

        return {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: DECIDED,
            TargetStatus.REJECTED.value: REJECTED,
            TargetStatus.DONE.value: DONE,
            TargetStatus.WRITTEN_OFF.value: DECIDED,
        }[dossier._meta.target_state]
