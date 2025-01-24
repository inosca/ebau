import json

import pytest
from caluma.caluma_form.models import Question
from django.conf import settings
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource

TEST_SCENARIOS = [
    {
        # Grundinformationen (Adresse, Grundstück, Zone, etc.)
        "coords": (2635082.564072413, 1241236.536643672),
        "checked_questions": [
            "gemeinde",
            "ort-grundstueck",
            "parzelle",
        ],
    },
    {
        # Waldnaturschutzinventar
        "coords": (2657749, 1240978),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # Landschaftsschutzdekrete (detailliert Legende)
        "coords": (2657686.7954999995, 1241576.6492766952),
        "checked_questions": ["ueberlagerte-schutzzonen-und-schutzobjekte"],
    },
    {
        # BLN - Bundesinventar der Landschaften und Naturdenkmäler von nationaler Bedeutung
        "coords": (2657645.3687233045, 1241677.0886165234),
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
    question_factory, question_option_factory, option_factory, mock_municipalities
):
    gis_questions = [
        ("gemeinde", Question.TYPE_DYNAMIC_CHOICE),
        ("ort-grundstueck", Question.TYPE_TEXT),
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
        type = config[1]
        q = question_factory(slug=slug, type=type, label=slug)
        if len(config) == 3:
            for i, option in enumerate(reversed(config[2])):
                question_option_factory(
                    question=q,
                    option=option_factory(slug=f"{slug}-{option}", label=option),
                    sort=i,
                )

    Question.objects.filter(slug="gemeinde").update(data_source="Municipalities")
    mock_municipalities(["Aarburg", "Woanders"])

    return GISDataSource.objects.all()


@pytest.fixture
def ag_config(gis_data_source_factory, question_factory):
    call_command("loaddata", settings.ROOT_DIR("kt_ag/config/gis.json"))

    return GISDataSource.objects.all()


@pytest.mark.parametrize(
    "scenario",
    TEST_SCENARIOS,
)
@pytest.mark.vcr()
def test_ag_client(
    db,
    admin_client,
    gis_snapshot,
    vcr_config,
    ag_config,
    scenario,
    ag_data_sources,
):
    x, y = scenario["coords"]
    response = admin_client.get(
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

    assert response.status_code == status.HTTP_200_OK
    checked_data = {
        k: v
        for k, v in response.json()["data"].items()
        if k in scenario["checked_questions"]
    }

    assert checked_data == gis_snapshot
