from camac.dossier_import.config.common import PersonalDataTriageFieldsMixin
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.validation import TargetStatus
from camac.dossier_import.writers import (
    CalumaAnswerWriter,
    CalumaCombinedStreetAndNumberWriter,
    CalumaPlotDataWriter,
    CalumaTableAnswerWriter,
    DossierWriter,
    SubmitDateWriter,
)
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
    "last_name": "name",
    "first_name": "vorname",
    "street_and_number": "strasse-und-nr",
    "zip": "plz",
    "town": "ort",
    "phone": "telefon",
    "email": "e-mail",
}

PLOT_DATA_MAPPING = {
    "plot_number": "parzellennummer",
    "egrid_number": "e-grid-nr",
    "coord_east": "koordinaten-ost",
    "coord_north": "koordinaten-nord",
}


class KtStGallenDossierWriter(PersonalDataTriageFieldsMixin, DossierWriter):
    id = CalumaAnswerWriter(
        target="kommunale-gesuchsnummer", formatter="to-string", protected=True
    )
    proposal = CalumaAnswerWriter(target="beschreibung-bauvorhaben", protected=True)
    cantonal_id = CalumaAnswerWriter(
        target="kantonale-gesuchsnummer", formatter="to-string"
    )
    plot_data = CalumaPlotDataWriter(
        target="parzellen", column_mapping=PLOT_DATA_MAPPING
    )
    usage = CalumaAnswerWriter(target="zonenplan")
    application_type = CalumaAnswerWriter(target="geschaeftstyp")
    submit_date = SubmitDateWriter()
    decision_date = CalumaAnswerWriter(target="entscheid-datum", task="decision")
    publication_date = CalumaAnswerWriter(target="datum-publikation")
    construction_start_date = CalumaAnswerWriter(target="baubeginn")
    profile_approval_date = CalumaAnswerWriter(target="datum-schnurgeruestabnahme")
    final_approval_date = CalumaAnswerWriter(target="datum-schlussabnahme")
    completion_date = CalumaAnswerWriter(target="bauende")
    link = CalumaAnswerWriter(target="link")
    custom_1 = CalumaAnswerWriter(target="freies-textfeld-1")
    custom_2 = CalumaAnswerWriter(target="freies-textfeld-2")
    street = CalumaCombinedStreetAndNumberWriter(
        target="strasse-und-nr",
        fields=["street", "street_number"],
    )
    city = CalumaAnswerWriter(target="ort")
    applicant = CalumaTableAnswerWriter(
        target="gesuchstellerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    landowner = CalumaTableAnswerWriter(
        target="grundeigentuemerin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
    )
    project_author = CalumaTableAnswerWriter(
        target="projektverfasserin",
        column_mapping=PERSON_MAPPING,
        value_mapping=PERSON_VALUE_MAPPING,
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
        DONE = DECIDED + ["init-construction-monitoring", "complete-instance"]

        return {
            TargetStatus.SUBMITTED.value: SUBMITTED,
            TargetStatus.APPROVED.value: DECIDED,
            TargetStatus.WRITTEN_OFF.value: DONE,
            TargetStatus.REJECTED.value: DONE,
            TargetStatus.DONE.value: DONE,
        }[dossier._meta.target_state]
