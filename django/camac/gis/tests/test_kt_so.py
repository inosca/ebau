import pytest
from caluma.caluma_form.models import Question
from django.core.management import call_command
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.gis.models import GISDataSource

TEST_SCENARIOS = [
    {
        # Grundinformationen (Adresse, Grundstück, Zone, etc.)
        "coords": (2607345, 1228110),
        "checked_questions": [
            "gemeinde",
            "gemeindenummer-bfs",
            "strasse-flurname",
            "strasse-nummer",
            "plz",
            "ort",
            "parzellen",
            "nutzungsplanung-grundnutzung",
            "nutzungsplanung-grundnutzung-kanton",
            "nutzungsplanung-weitere-festlegungen",
        ],
    },
    {
        # Wald- und Gewässernähe
        "coords": (2606564, 1227444),
        "checked_questions": ["weitere-gis-informationen"],
    },
    {
        # Fruchtfolgefläche
        "coords": (2606403, 1230468),
        "checked_questions": ["fruchtfolgeflaeche"],
    },
    {
        # Naturgefahren
        "coords": (2610176, 1229506),
        "checked_questions": ["naturgefahren-gis"],
    },
    {
        # Altlasten
        "coords": (2606257, 1227893),
        "checked_questions": ["altlasten-gis"],
    },
    {
        # Gewässerschutz
        "coords": (2606323, 1230662),
        "checked_questions": ["gewaesserschutz"],
    },
    {
        # Denkmalschutz
        "coords": (2607278, 1228635),
        "checked_questions": ["denkmalschutz"],
    },
    {
        # Archäologie
        "coords": (2606997, 1228295),
        "checked_questions": ["archaeologie"],
    },
    {
        # Bundesinventare: IVS Regional und Lokal
        "coords": (2605769, 1224934),
        "checked_questions": ["bundesinventare"],
    },
    {
        # Bundesinventare: IVS National
        "coords": (2606771, 1225353),
        "checked_questions": ["bundesinventare"],
    },
    {
        # Bundesinventare: BLN
        "coords": (2602055, 1231778),
        "checked_questions": ["bundesinventare"],
    },
    {
        # Bundesinventare: Trockenwiesen und -weiden
        "coords": (2596747, 1230180),
        "checked_questions": ["bundesinventare"],
    },
    {
        # Bundesinventare: Hochmoore
        "coords": (2617752, 1224560),
        "checked_questions": ["bundesinventare"],
    },
    {
        # Bundesinventare: Flachmoore, Wasser- und Zugvogelreservate, Amphibienlaichgebiete (Ortsfeste Objekte)
        "coords": (2595903, 1223703),
        "checked_questions": ["bundesinventare"],
    },
    {
        # Bundesinventare: Auengebiete
        "coords": (2600778, 1225954),
        "checked_questions": ["bundesinventare"],
    },
]


@pytest.fixture
def so_data_sources(question_factory, settings, mock_municipalities):
    call_command("loaddata", settings.ROOT_DIR("kt_so/config/gis.json"))

    gis_questions = [
        ("gemeinde", Question.TYPE_DYNAMIC_CHOICE),
        ("gemeindenummer-bfs", Question.TYPE_INTEGER),
        ("parzellen", Question.TYPE_TABLE),
        ("parzellennummer", Question.TYPE_TEXT),
        ("ort", Question.TYPE_TEXT),
        ("plz", Question.TYPE_TEXT),
        ("strasse-flurname", Question.TYPE_TEXT),
        ("strasse-nummer", Question.TYPE_TEXT),
        ("e-grid", Question.TYPE_TEXT),
        ("lagekoordinaten-ost", Question.TYPE_FLOAT),
        ("lagekoordinaten-nord", Question.TYPE_FLOAT),
        ("flaeche-m", Question.TYPE_INTEGER),
        ("nutzungsplanung-grundnutzung", Question.TYPE_TEXTAREA),
        ("nutzungsplanung-grundnutzung-kanton", Question.TYPE_TEXTAREA),
        ("nutzungsplanung-weitere-festlegungen", Question.TYPE_TEXTAREA),
        ("weitere-gis-informationen", Question.TYPE_TEXTAREA),
        ("fruchtfolgeflaeche", Question.TYPE_TEXTAREA),
        ("naturgefahren-gis", Question.TYPE_TEXTAREA),
        ("altlasten-gis", Question.TYPE_TEXTAREA),
        ("gewaesserschutz", Question.TYPE_TEXTAREA),
        ("denkmalschutz", Question.TYPE_TEXTAREA),
        ("archaeologie", Question.TYPE_TEXTAREA),
        ("bundesinventare", Question.TYPE_TEXTAREA),
    ]

    for slug, type in gis_questions:
        question_factory(slug=slug, type=type)

    Question.objects.filter(slug="gemeinde").update(data_source="Municipalities")
    mock_municipalities(["Solothurn"])

    return GISDataSource.objects.all()


@pytest.mark.parametrize(
    "scenario",
    TEST_SCENARIOS,
    # Make sure the generated test names are zero-padded in order for the
    # snapshots to be in the same order as the scenario definitions above.
    ids=lambda val: f"scenario_{str(TEST_SCENARIOS.index(val) + 1).zfill(2)}",
)
@pytest.mark.vcr()
def test_sogis_client(
    db,
    admin_client,
    gis_snapshot,
    scenario,
    so_data_sources,
    vcr_config,
):
    x, y = scenario["coords"]
    response = admin_client.get(reverse("gis-data"), data={"x": x, "y": y})

    assert response.status_code == status.HTTP_200_OK

    checked_data = {
        k: v
        for k, v in response.json()["data"].items()
        if k in scenario["checked_questions"]
    }

    assert checked_data == gis_snapshot


@pytest.fixture
def so_fake_data_source(gis_data_source_factory, question_factory):
    question_factory(
        slug="gemeinde",
        type=Question.TYPE_DYNAMIC_CHOICE,
        data_source="Municipalities",
    )

    return gis_data_source_factory(
        pk="49992886-4602-4eb3-8499-ebeb58c9f17d",
        client=GISDataSource.CLIENT_SOGIS,
        config={
            "layer": "ch.so.agi.gemeindegrenzen.data",
            "properties": [{"propertyName": "gemeindename", "question": "gemeinde"}],
        },
    )


@pytest.fixture
def so_unknown_layer_data_source(so_fake_data_source):
    so_fake_data_source.config["layer"] = "ch.so.agi.av.unknown_layer"
    so_fake_data_source.save()

    return so_fake_data_source


@pytest.fixture
def so_unknown_property_data_source(so_fake_data_source):
    so_fake_data_source.config["properties"][0]["propertyName"] = "unknown_property"
    so_fake_data_source.save()

    return so_fake_data_source


@pytest.fixture
def so_unknown_question_data_source(so_fake_data_source):
    so_fake_data_source.config["properties"][0]["question"] = "unknown_question"
    so_fake_data_source.save()

    return so_fake_data_source


@pytest.mark.parametrize(
    "data_source,expected_status",
    [
        (lf("so_unknown_layer_data_source"), status.HTTP_200_OK),
        (lf("so_unknown_property_data_source"), status.HTTP_200_OK),
        (lf("so_unknown_question_data_source"), status.HTTP_200_OK),
    ],
)
@pytest.mark.vcr()
def test_sogis_client_errors(
    db,
    admin_client,
    data_source,
    expected_status,
    gis_snapshot,
    vcr_config,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={"x": TEST_SCENARIOS[0]["coords"][0], "y": TEST_SCENARIOS[0]["coords"][1]},
    )

    assert response.status_code == expected_status
    assert response.json() == gis_snapshot
