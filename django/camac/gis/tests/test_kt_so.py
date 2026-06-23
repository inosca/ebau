import pytest
import requests
from caluma.caluma_form.models import Question
from django.core.management import call_command
from django.http import QueryDict
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.gis.clients.sogis import SoGisClient
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
def so_data_sources(
    caluma_question_factory,
    caluma_question_option_factory,
    caluma_option_factory,
    settings,
    mock_municipalities,
):
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
        ("gis-daten-uebernommen", Question.TYPE_CHOICE),
        ("flaeche-m", Question.TYPE_TEXT),
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
        caluma_question_factory(slug=slug, type=type)

    Question.objects.filter(slug="gemeinde").update(data_source="Municipalities")
    caluma_question_option_factory(
        pk="gis-daten-uebernommen.gis-daten-uebernommen-ja",
        question=Question.objects.get(pk="gis-daten-uebernommen"),
        option=caluma_option_factory(pk="gis-daten-uebernommen-ja"),
    )
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
    celery_fake_worker,
    so_data_sources,
    vcr_config,
):
    x, y = scenario["coords"]
    response = admin_client.get(
        reverse("gis-data"), data={"x": x, "y": y, "applied": "ja"}
    )

    assert response.status_code == status.HTTP_200_OK

    celery_fake_worker.run_tasks()

    task_id = response.json()["task_id"]
    response = admin_client.get(reverse("gis-data", args=[task_id]))

    checked_data = {
        k: v
        for k, v in response.json()["data"].items()
        if k in scenario["checked_questions"]
    }

    assert checked_data == gis_snapshot


@pytest.fixture
def so_fake_data_source(gis_data_source_factory, caluma_question_factory):
    caluma_question_factory(
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
    celery_fake_worker,
    gis_snapshot,
    vcr_config,
):
    response_0 = admin_client.get(
        reverse("gis-data"),
        data={"x": TEST_SCENARIOS[0]["coords"][0], "y": TEST_SCENARIOS[0]["coords"][1]},
    )

    celery_fake_worker.run_tasks()

    task_id = response_0.json()["task_id"]

    response_1 = admin_client.get(
        reverse("gis-data", args=[task_id]),
        data={"x": TEST_SCENARIOS[0]["coords"][0], "y": TEST_SCENARIOS[0]["coords"][1]},
    )

    assert response_1.status_code == expected_status
    assert response_1.json() == gis_snapshot


@pytest.mark.django_db
@pytest.mark.django_db
def test_sogis_client_string_concat_concatenates_multiple_matching_features(
    caluma_question_factory, mocker
):
    caluma_question_factory(slug="archaeologie", type=Question.TYPE_TEXTAREA)

    client = SoGisClient(QueryDict("x=100&y=200"))
    response = mocker.Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {
        "features": [
            {
                "properties": {
                    "thema": "ch.SO.Archaeologie",
                    "beschreibung": "Fundstelle A",
                }
            },
            {
                "properties": {
                    "thema": "ch.SO.Archaeologie",
                    "beschreibung": "Fundstelle B",
                }
            },
        ]
    }
    client.session.get = mocker.Mock(return_value=response)

    data = client.process_data_source(
        {
            "layer": "test-layer",
            "properties": [
                {
                    "topic": "ch.SO.Archaeologie",
                    "question": "archaeologie",
                    "propertyName": "beschreibung",
                }
            ],
        },
        None,
    )

    assert data == {"archaeologie": "Fundstelle A, Fundstelle B"}


@pytest.mark.django_db
def test_sogis_client_process_list_data_source(caluma_question_factory, mocker):
    client = SoGisClient(QueryDict("x=2607345&y=1228110"))
    caluma_question_factory(slug="gemeinde", type=Question.TYPE_TEXT)
    caluma_question_factory(slug="gemeindenummer-bfs", type=Question.TYPE_INTEGER)

    config = {
        "layer": "ch.so.dsbjd.ebauso_lokalisation_grundstueck.data",
        "mergeStrategyOverride": "list",
        "properties": [
            {"question": "gemeinde", "propertyName": "gemeinde"},
            {
                "cast": "integer",
                "question": "gemeindenummer-bfs",
                "propertyName": "bfsnr",
            },
            {"question": "parzellen.e-grid", "propertyName": "egrid"},
            {"question": "parzellen.parzellennummer", "propertyName": "nummer"},
            {"question": "parzellen.grundstueckart", "propertyName": "art"},
            {"question": "parzellen.flaeche-m", "propertyName": "flaechenmass"},
            {
                "question": "parzellen.grundbuchkreis",
                "propertyName": "grundbuchkreis",
            },
            {
                "question": "parzellen.amtschreiberei",
                "propertyName": "amtschreiberei",
            },
        ],
    }

    features = [
        {
            "properties": {
                "gemeinde": "Solothurn",
                "bfsnr": "2601",
                "egrid": "CH123",
                "nummer": "1000",
                "art": "Liegenschaft",
                "flaechenmass": 500,
                "grundbuchkreis": "Solothurn",
                "amtschreiberei": "Region Solothurn",
            }
        },
        {
            "properties": {
                "gemeinde": "Solothurn",
                "bfsnr": "2601",
                "egrid": "CH456",
                "nummer": "1001",
                "art": "SelbstRecht.Baurecht",
                "flaechenmass": 100,
                "grundbuchkreis": "Solothurn",
                "amtschreiberei": "Region Solothurn",
            }
        },
    ]

    response = mocker.Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"features": features}
    client.session.get = mocker.Mock(return_value=response)

    assert client.process_data_source(config, None) == {
        "gemeinde": "Solothurn",
        "gemeindenummer-bfs": "2601",
        "parzellen": [
            {
                "e-grid": "CH123",
                "parzellennummer": "1000",
                "grundstueckart": "Liegenschaft",
                "flaeche-m": "500",
                "grundbuchkreis": "Solothurn",
                "amtschreiberei": "Region Solothurn",
            },
            {
                "e-grid": "CH456",
                "parzellennummer": "1001",
                "grundstueckart": "SelbstRecht.Baurecht",
                "flaeche-m": "100",
                "grundbuchkreis": "Solothurn",
                "amtschreiberei": "Region Solothurn",
            },
        ],
    }


def test_sogis_client_matches_topic():
    client = SoGisClient(QueryDict("x=2607345&y=1228110"))

    properties = {
        "thema": "ch.SO.NutzungsplanungGrundnutzung",
        "beschreibung": "Wohnzone",
    }

    assert client.matches_topic(
        properties,
        {
            "topic": "ch.SO.NutzungsplanungGrundnutzung",
            "propertyName": "beschreibung",
            "question": "nutzungsplanung-grundnutzung",
        },
    )

    assert not client.matches_topic(
        properties,
        {
            "topic": "ch.SO.Denkmalschutz",
            "propertyName": "beschreibung",
            "question": "denkmalschutz",
        },
    )

    assert client.matches_topic(
        properties,
        {
            "propertyName": "beschreibung",
            "question": "nutzungsplanung-grundnutzung",
        },
    )


@pytest.mark.django_db
def test_sogis_client_process_data_source_filters_by_topic(
    caluma_question_factory, requests_mock, settings
):
    caluma_question_factory(
        slug="nutzungsplanung-grundnutzung",
        type=Question.TYPE_TEXTAREA,
    )

    settings.SO_GIS_BASE_URL = "https://example.com"
    settings.SO_GIS_VERIFY_SSL = True

    client = SoGisClient(QueryDict("x=2607345&y=1228110"))

    requests_mock.get(
        "https://example.com/api/data/v1/ch.so.dsbjd.ebauso_fachthemen_flaechen.data/?bbox=2607345.0,1228110.0,2607345.0,1228110.0",
        json={
            "features": [
                {
                    "properties": {
                        "thema": "ch.SO.NutzungsplanungGrundnutzung",
                        "beschreibung": "Wohnzone",
                    }
                },
                {
                    "properties": {
                        "thema": "ch.SO.Denkmalschutz",
                        "beschreibung": "Should be ignored",
                    }
                },
            ]
        },
    )

    data = client.process_data_source(
        {
            "layer": "ch.so.dsbjd.ebauso_fachthemen_flaechen.data",
            "properties": [
                {
                    "topic": "ch.SO.NutzungsplanungGrundnutzung",
                    "question": "nutzungsplanung-grundnutzung",
                    "propertyName": "beschreibung",
                },
                {
                    "topic": "ch.SO.Wasserschutz",
                    "question": "table.question",
                    "propertyName": "beschreibung",
                },
            ],
        },
        None,
    )

    assert data == {"nutzungsplanung-grundnutzung": "Wohnzone"}


def test_sogis_client_process_list_data_source_skips_empty_values(mocker):
    config = {
        "properties": [
            {
                "propertyName": "empty_value",
                "question": "table.question1",
            },
            {
                "propertyName": "valid_value",
                "question": "table.question1",
            },
            {
                "propertyName": "empty_value",
                "question": "table.question2",
            },
            {
                "propertyName": "valid_value",
                "question": "table.question3",
            },
        ],
    }

    features = [
        {
            "properties": {
                "empty_value": "",
                "valid_value": "foo",
            },
        },
        {
            "properties": {
                "empty_value": "",
                "valid_value": "",
            },
        },
    ]

    client = SoGisClient(QueryDict("x=2607345&y=1228110"))
    response = mocker.Mock()
    response.raise_for_status.return_value = None
    response.json.return_value = {"features": features}
    client.session.get = mocker.Mock(return_value=response)

    assert client.process_data_source(config | {"layer": "test-layer"}, None) == {
        "table": [
            {"question1": "foo", "question2": None, "question3": "foo"},
            {"question1": None, "question2": None, "question3": None},
        ]
    }


def test_sogis_client_get_data_raises_runtime_error_on_http_error(mocker):
    client = SoGisClient(QueryDict("x=2607345&y=1228110"))

    response = mocker.Mock()
    response.status_code = 500
    response.raise_for_status.side_effect = requests.HTTPError

    client.session.get = mocker.Mock(return_value=response)

    with pytest.raises(RuntimeError) as exc:
        client.process_data_source(
            {
                "layer": "test-layer",
                "properties": [],
            },
            None,
        )

    assert "500" in str(exc.value)


def test_sogis_client_get_hidden_questions():
    assert SoGisClient.get_hidden_questions(
        {
            "properties": [
                {"question": "visible-question"},
                {"question": "hidden-question", "hidden": True},
            ]
        }
    ) == ["hidden-question"]
