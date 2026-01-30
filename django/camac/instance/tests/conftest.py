import pytest

from camac.tests.utils import Utils


@pytest.fixture
def ur_master_data_case_gwr(
    ur_instance, ur_master_data_case, workflow_entry_factory, utils: Utils
):
    ur_master_data_case.meta = {"dossier-number": "1201-21-003"}
    ur_master_data_case.save()

    document = ur_master_data_case.document

    # Completed date
    # Assert that workflow entry of last group (phase) is selected
    workflow_entry = next(
        filter(
            lambda entry: entry.workflow_item_id == 67,
            ur_instance.workflowentry_set.all(),
        ),
        None,
    )

    workflow_entry_factory(
        instance=ur_instance,
        workflow_date="2021-08-05 08:00:06+00",
        group=2,
        workflow_item=workflow_entry.workflow_item,
    )

    # Energy devices
    # Check logic for heating / warmwater devices and
    # primary / secondary devices
    table_answer = document.answers.filter(question_id="haustechnik-tabelle").first()
    utils.add_table_answer(
        document,
        "haustechnik-tabelle",
        [
            {
                "gehoert-zu-gebaeudenummer": "Villa",
                "anlagetyp": "anlagetyp-warmwasser",
                "heizsystem-art": "-zusatzheizung",
                "hauptheizungsanlage": "hauptheizungsanlage-gas",
            }
        ],
        table_answer,
    )

    return ur_master_data_case


@pytest.fixture
def sz_master_data_case_gwr(sz_master_data_case, form_field_factory):
    sz_instance = sz_master_data_case.instance

    # GWR Form
    form_field_factory(
        instance=sz_instance,
        name="gwr",
        value=[
            {
                "kategorie": "Gebäude ohne Wohnnutzung",
                "heizungsart": "Einzelofenheizung",
                "energietrager-heizung": "Holz",
                "energietrager-warmwasser": "Elektrizität",
                "geschosse": 2,
                "wohnungen": [
                    {
                        "stockwerk": "1. OG",
                        "maisonette": "Ja",
                        "lage": "Nord",
                        "zimmer": 4,
                        "flache": 42,
                        "kuchenart": "Kochnische (unter 4m²)",
                    }
                ],
            }
        ],
    )

    return sz_instance.case


@pytest.fixture
def sz_master_data_case_gwr_v2(sz_master_data_case, form_field_factory):
    sz_instance = sz_master_data_case.instance

    # GWR Form v2
    form_field_factory(
        instance=sz_instance,
        name="gwr-v2",
        value=[
            {
                "gebaeudebezeichnung": "Grosses Haus",
                "kategorie": "Gebäude mit ausschliesslicher Wohnnutzung",
                "zivilschutzraum": "Ja",
                "heizungsart": "Wärmepumpe für mehrere Gebäude",
                "energietrager-heizung": "Erdwärme (generisch)",
                "waermeerzeuger-warmwasser": "Zentraler Elektroboiler",
                "energietrager-warmwasser": "Sonne (thermisch)",
                "geschosse": 4,
                "wohnraeume": 24,
                "wohnungen": [
                    {
                        "stockwerk": "Parterre",
                        "maisonette": "Nein",
                        "lage": "West",
                        "zimmer": 2,
                        "flache": 70,
                        "kocheinrichtung": "Ja",
                    },
                    {
                        "stockwerk": "2. UG",
                        "maisonette": "Nein",
                        "lage": "Ost",
                        "zimmer": 3,
                        "flache": 24,
                        "kocheinrichtung": "Nein",
                    },
                ],
            }
        ],
    )

    return sz_instance.case
