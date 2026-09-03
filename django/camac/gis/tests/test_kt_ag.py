import json

import pytest
from caluma.caluma_form.models import Question
from django.conf import settings
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.gis.clients.ag import AgGisClient
from camac.gis.models import GISDataSource


def test_get_address_data_with_multiple_results(requests_mock, settings):
    response = {
        "results": [
            {
                "properties": {
                    "stn_label": "Bahnhofstrasse",
                    "adr_number": "1338",
                    "zip_label": "4663 Aarburg",
                }
            },
            {
                "properties": {
                    "stn_label": "Andere Strasse",
                    "adr_number": "32",
                    "zip_label": "9999 Nirvana",
                }
            },
            {
                "properties": {
                    "stn_label": "Bahnhofstrasse",
                    "adr_number": "1337",
                    "zip_label": "4663 Aarburg",
                }
            },
        ]
    }
    settings.ADMIN_GIS_BASE_URL = "https://example.com"
    requests_mock.get(
        "https://example.com/rest/services/ech/MapServer/identify", json=response
    )

    address_response = AgGisClient({}).get_address_response(
        [{"x": 2635082, "y": 1241236}]
    )

    assert AgGisClient.get_address_data(address_response) == {
        "street-and-housenumber": "Bahnhofstrasse 1337, 1338; Andere Strasse 32",
        "plz": 4663,
    }
    assert AgGisClient.get_address_data({}) == {}


TEST_SCENARIOS = [
    {
        # Grundinformationen (Adresse, Grundstück, Zone, etc.)
        "coords": (2635082.564072413, 1241236.536643672),
        "checked_questions": [
            "gemeinde",
            "grundstuecksflaeche",
            "ort-grundstueck",
            "parzelle",
            "plz",
            "street-and-housenumber",
        ],
    },
    {
        # Waldnaturschutzinventar
        "coords": (2657749, 1240978),
        "isos": "national",
        "checked_questions": [
            "zonenplan",
            "ueberlagerte-schutzzonen-und-schutzobjekte",
        ],
    },
    {
        # Landschaftsschutzdekrete (detailliert Legende)
        "coords": (2657686.7954999995, 1241576.6492766952),
        "isos": "regional",
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # BLN - Bundesinventar der Landschaften und Naturdenkmäler von nationaler Bedeutung
        "coords": (2657645.3687233045, 1241677.0886165234),
        "isos": "lokal",
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Wildtierkorridore: Perimeter und Warteräume
        "coords": (2657308, 1241300),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Wasser-und Zugvogelreservate
        "coords": (2670201, 1242283),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Trockenwiesen
        "coords": (2645903, 1252830),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Amphibienlaichgebiet - ortsfeste Objekte
        "coords": (2647143, 1250753),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Amphibienlaichgebiet - Wanderobjekte
        "coords": (2650151, 1244549),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Hecke
        "coords": (2650119, 1244361),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Kantonale Denkmalschutzobjekte
        "coords": (2654406.245488748, 1243184.0781744092),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Geschützte Naturobjekte im Kulturlandplan
        "coords": (2650229, 1238861),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Geschützte Kulturobjekte im Kulturlandplan
        "coords": (2650103, 1238632),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Naturschutzgebiet von kant. Bedeutung (NkB) Richtplan L 2.5
        "coords": (2663425, 1247037),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Bundesinventar der Flachmoore von nationaler Bedeutung
        "coords": (2663415, 1247092),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Weilerzone
        "coords": (2652240, 1243774),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Auengebiete von nationaler Bedeutung
        "coords": (2670175, 1242187),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Bundesinventar der Hoch- und Übergangsmoore von nationaler Bedeutung
        "coords": (2665946, 1245959),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Überlagerte Schutzräume für Lebensräume und Landschaften (ohne Gewässerraum)
        "coords": (2654826, 1243271),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Bauinventarobjekte
        "coords": (2654357, 1241392),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Gebäude unter Schutz
        "coords": (2654391, 1241377),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Kurzinventar Denkmalpflege
        "coords": (2655777, 1242133),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Archäologische Fundstellen nach Typ, mit Denkmalschutz
        "coords": (2654373, 1242470),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Kantonale Denkmalschutzobjekte
        "coords": (2654406, 1243184),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Hochwasser, Gefahrenzone Hochwasser, gewaesserschutzbereich
        "coords": (2654643, 1244046),
        "checked_questions": [
            "plan-der-gefahrenkommission",
            "das-bauvorhaben-befindet-sich-in",
        ],
    },
    {
        # Bauzonen: Grundnutzung
        "coords": (2654743, 1243772),
        "checked_questions": ["zonenplan"],
    },
    {
        # Permanenter Rutsch, gefahrenzone-massenbewegungen
        "coords": (2642903, 1240177),
        "checked_questions": [
            "plan-der-gefahrenkommission",
            "das-bauvorhaben-befindet-sich-in",
        ],
    },
    {
        # Assekuranznummer
        "coords": (2643609, 1241663),
        "checked_questions": ["gebaeude", "amtliche-gebaeudenummer", "egid-nr"],
    },
    {
        # Kantonaler Nutzungsplan Verkehr
        "coords": (2635722, 1239843),
        "checked_questions": ["gestaltungs-und-erschliessungsplan"],
    },
    {
        # Gewässerschutzbereich Au, Eisenbahnlinie
        "coords": (2635666, 1240642),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # grundwasserschutzzone
        "coords": (2636545, 1239084),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # Bachkataster
        "coords": (2636602, 1239145),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # Gewässerraum
        "coords": (2636488, 1239256),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # Chemiesicherheit
        "coords": (2636719, 1239492),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # Risikokataster: Konsultationsbereich Gasleitung : Chemiesicherheit
        "coords": (2636488, 1239256),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # Kantons- oder Nationalstrassen
        "coords": (2636625, 1239426),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in", "kantonsstrassen"],
    },
    {
        # Waldgrenze
        "coords": (2635317, 1238615),
        "checked_questions": ["waldareal"],
    },
    {
        # Prüfperimeter Bodenaushub
        "coords": (2634417, 1240019),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
    {
        # Kataster belasteter Standorte
        "coords": (2634847, 1238635),
        "checked_questions": ["das-bauvorhaben-befindet-sich-in"],
    },
]


@pytest.fixture
def ag_data_sources(
    caluma_question_factory,
    caluma_question_option_factory,
    caluma_option_factory,
    mock_municipalities,
):
    gis_questions = [
        ("gemeinde", Question.TYPE_DYNAMIC_CHOICE),
        ("grundstuecksflaeche", Question.TYPE_FLOAT),
        ("ort-grundstueck", Question.TYPE_TEXT),
        ("plz", Question.TYPE_INTEGER),
        ("street-and-housenumber", Question.TYPE_TEXT),
        ("parzellen", Question.TYPE_TABLE),
        ("parzellennummer", Question.TYPE_TEXT),
        ("e-grid-nr", Question.TYPE_TEXT),
        (
            "waldareal",
            Question.TYPE_CHOICE,
            ["ja", "waldabstandsbereich", "nein"],
        ),
        ("kantonsstrassen", Question.TYPE_CHOICE, ["ja", "nein"]),
        ("denkmalschutzobjekt", Question.TYPE_CHOICE, ["ja", "nein"]),
        ("ausserhalb-bauzone", Question.TYPE_CHOICE, ["ja", "nein"]),
        (
            "das-bauvorhaben-befindet-sich-in",
            Question.TYPE_MULTIPLE_CHOICE,
            [
                "gewaesserraum",
                "gewaesserschutzbereich",
                "grundwasserschutzzone",
                "kataster-belasteter-standorte",
                "pruefperimeter-bodenaushub",
                "eisenbahnlinie",
                "archaeologische-fundstelle",
                "gefahrenzone-massenbewegungen",
                "gefahrenzone",
                "risikokataster-chemiesicherheit",
            ],
        ),
    ]

    for config in gis_questions:
        slug = config[0]
        question_type = config[1]
        question = caluma_question_factory(slug=slug, type=question_type, label=slug)
        if len(config) == 3:
            for i, option in enumerate(reversed(config[2])):
                caluma_question_option_factory(
                    question=question,
                    option=caluma_option_factory(slug=f"{slug}-{option}", label=option),
                    sort=i,
                )

    Question.objects.filter(slug="gemeinde").update(data_source="Municipalities")
    mock_municipalities(["Aarburg", "Woanders"])

    return GISDataSource.objects.all()


@pytest.fixture
def ag_config(gis_data_source_factory, caluma_question_factory):
    call_command("loaddata", settings.ROOT_DIR("kt_ag/config/gis.json"))

    return GISDataSource.objects.all()


def test_ag_client_isos_request(mocker, settings):
    settings.AG_GIS_BASE_URL = "https://example.com/rest/services"
    markers = [{"x": 2659704.2, "y": 1238402.6}]
    client = AgGisClient({})
    get_identify_response = mocker.patch.object(client, "get_identify_response")

    client.get_isos_identify_response(markers)

    get_identify_response.assert_called_once_with(
        markers,
        0,
        "are_isos/MapServer",
        "all:15",
    )


def test_ag_client_returns_all_buildings():
    client = AgGisClient({})
    agis_info = [
        {
            "layerName": "AV: Assekuranznummern",
            "attributes": {"EGID": "123", "ASSNR": "10"},
        },
        {"layerName": "AV: Parzellen", "attributes": {"NUMMER": "42"}},
        {
            "layerName": "AV: Assekuranznummern",
            "attributes": {"EGID": "456", "ASSNR": "11"},
        },
    ]

    assert client.get_building_data(agis_info) == [
        {"egid-nr": "123", "amtliche-gebaeudenummer": "10"},
        {"egid-nr": "456", "amtliche-gebaeudenummer": "11"},
    ]


def test_ag_client_uses_only_first_layer_when_configured(mocker):
    markers = [{"x": 2634951.5, "y": 1241103.9}]
    client = AgGisClient(
        {"query": json.dumps({"markers": markers, "geometry": "POINT"})}
    )
    mocker.patch.object(
        client,
        "get_agis_identify_response",
        side_effect=[
            {
                "results": [
                    {
                        "layerName": "AV: Parzellen",
                        "attributes": {"NUMMER": "541", "FLAECHE": "112"},
                    },
                    {
                        "layerName": "AV: Parzellen",
                        "attributes": {"NUMMER": "534", "FLAECHE": "255"},
                    },
                ]
            },
            {"results": []},
        ],
    )
    config = [
        {
            "mapper": "properties",
            "identifier": "AV: Parzellen",
            "take_first": True,
            "properties": [
                {
                    "question": "grundstuecksflaeche",
                    "propertyName": "FLAECHE",
                }
            ],
        }
    ]

    result = client.process_data_source(config, None)

    assert result["grundstuecksflaeche"] == "112"
    assert result["parzelle"][0]["parzellennummer"] == "541"


@pytest.mark.parametrize(
    "scenario",
    TEST_SCENARIOS,
)
@pytest.mark.vcr
@pytest.mark.django_db
def test_ag_client(
    admin_client,
    gis_snapshot,
    mocker,
    vcr_config,
    celery_fake_worker,
    ag_config,
    scenario,
    ag_data_sources,
):
    isos_results = []
    if significance := scenario.get("isos"):
        isos_results.append(
            {
                "layerName": "Ortsbilder PDF-Perimeter (ISOS-I-basiert)",
                "attributes": {"Bedeutung": significance},
            }
        )
    mocker.patch.object(
        AgGisClient,
        "get_isos_identify_response",
        return_value={"results": isos_results},
    )
    mocker.patch.object(
        AgGisClient,
        "get_address_response",
        return_value={
            "results": [
                {
                    "properties": {
                        "stn_label": "Bahnhofstrasse",
                        "adr_number": "1337",
                        "zip_label": "4663 Aarburg",
                    },
                },
                {
                    "properties": {
                        "stn_label": "Andere Strasse",
                        "adr_number": "32",
                        "zip_label": "9999 Nirvana",
                    },
                },
            ],
        },
    )
    x, y = scenario["coords"]
    response_0 = admin_client.get(
        reverse("gis-data"),
        data={
            "query": json.dumps(
                {
                    "markers": [{"x": x, "y": y}],
                    "geometry": "POINT",
                }
            ),
            "form": "baugesuch",
        },
    )

    task_id = response_0.json()["task_id"]

    celery_fake_worker.run_tasks()

    response_1 = admin_client.get(
        reverse("gis-data", args=[task_id]),
        data={
            "query": json.dumps(
                {
                    "markers": [{"x": x, "y": y}],
                    "geometry": "POINT",
                }
            ),
            "form": "baugesuch",
        },
    )

    assert response_1.status_code == status.HTTP_200_OK
    checked_data = {
        k: v
        for k, v in response_1.json()["data"].items()
        if k in scenario["checked_questions"]
    }

    assert checked_data == gis_snapshot
