import json

import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def ech0206_data_sources(
    question_factory, question_option_factory, option_factory, settings
):
    gis_questions = [
        ("egid-nr", Question.TYPE_TEXT),
        (
            "energie-waermequelle-heizung",
            Question.TYPE_CHOICE,
            [
                "7500",
                "7501",
                "7510",
                "7511",
                "7512",
                "7513",
                "7520",
                "7530",
                "7540",
                "7541",
                "7542",
                "7550",
                "7560",
                "7570",
                "7580",
                "7581",
                "7582",
                "7598",
                "7599",
                "noch-nicht-festgelegt",
            ],
        ),
        (
            "energie-waermequelle-warmwasser",
            Question.TYPE_CHOICE,
            [
                "7500",
                "7501",
                "7510",
                "7511",
                "7512",
                "7513",
                "7520",
                "7530",
                "7540",
                "7541",
                "7542",
                "7550",
                "7560",
                "7570",
                "7580",
                "7581",
                "7582",
                "7598",
                "7599",
                "noch-nicht-festgelegt",
            ],
        ),
        (
            "waermeerzeuger-warmwasser",
            Question.TYPE_CHOICE,
            [
                "7600",
                "7610",
                "7620",
                "7630",
                "7632",
                "7634",
                "7640",
                "7650",
                "7651",
                "7660",
                "7699",
            ],
        ),
        (
            "waermeerzeuger-heizung",
            Question.TYPE_CHOICE,
            [
                "7400",
                "7410",
                "7420",
                "7430",
                "7431",
                "7432",
                "7433",
                "7434",
                "7435",
                "7436",
                "7440",
                "7441",
                "7450",
                "7451",
                "7460",
                "7461",
                "7499",
                "noch-nicht-festgelegt",
            ],
        ),
    ]

    for config in gis_questions:
        slug = config[0]
        question_type = config[1]
        q = question_factory(slug=slug, type=question_type, label=slug)
        if len(config) == 3:
            for option in config[2]:
                question_option_factory(
                    question=q,
                    option=option_factory(slug=f"{slug}-{option}", label=option),
                )

    return GISDataSource.objects.all()


@pytest.fixture
def ech0206__config(gis_data_source_factory, question_factory):
    gis_data_source_factory(
        client=GISDataSource.CLIENT_KT_GR,
        config=[
            {
                "identifier": "gebaeudeadressen_av",
                "properties": [
                    {"question": "egid-nr", "propertyName": "gwr_egid"},
                ],
            },
        ],
    )
    gis_data_source_factory(
        client=GISDataSource.CLIENT_ECH_0206,
        config=[
            {
                "properties": [
                    {
                        "question": "energie-waermequelle-heizung",
                        "propertyName": "thermotechnicalDeviceForHeating1.energySourceHeating",
                    },
                    {
                        "question": "weitere-energie-waermequelle-heizung",
                        "propertyName": "thermotechnicalDeviceForHeating2.energySourceHeating",
                    },
                    {
                        "question": "waermeerzeuger-heizung",
                        "propertyName": "thermotechnicalDeviceForHeating1.heatGeneratorHeating",
                    },
                    {
                        "question": "weitere-waermeerzeuger-heizung",
                        "propertyName": "thermotechnicalDeviceForHeating2.heatGeneratorHeating",
                    },
                    {
                        "question": "energie-waermequelle-warmwasser",
                        "propertyName": "thermotechnicalDeviceForWarmWater1.energySourceHeating",
                    },
                    {
                        "question": "weitere-energie-waermequelle-warmwasser",
                        "propertyName": "thermotechnicalDeviceForWarmWater2.energySourceHeating",
                    },
                    {
                        "question": "waermeerzeuger-warmwasser",
                        "propertyName": "thermotechnicalDeviceForWarmWater1.heatGeneratorHotWater",
                    },
                    {
                        "question": "weitere-waermeerzeuger-warmwasser",
                        "propertyName": "thermotechnicalDeviceForWarmWater2.heatGeneratorHotWater",
                    },
                ]
            },
            {
                "properties": [
                    {
                        "question": "amtliche-gebaeudenummer",
                        "propertyName": "officialBuildingNo",
                    }
                ]
            },
            {
                "properties": [
                    {"question": "gwr-gebaeudevolumen", "propertyName": "volume"}
                ]
            },
            {
                "properties": [
                    {
                        "question": "energiebezugsflaeche",
                        "propertyName": "energyRelevantSurface",
                    }
                ]
            },
            {
                "properties": [
                    {
                        "hidden": True,
                        "mapper": "heat_surface",
                        "question": "werden-flaechen-beheizt",
                    }
                ]
            },
            {
                "properties": [
                    {
                        "hidden": True,
                        "mapper": "warm_water_connection",
                        "question": "ist-ein-warmwasseranschluss-geplant",
                    }
                ]
            },
        ],
    )


@pytest.mark.parametrize(
    "query_x,query_y",
    [
        (
            2759664.9038492967,
            1191395.5015286694,
        ),  # multiple egid numbers with multiple properties
        (
            2759647.4234941704,
            1191526.8007143869,
        ),  # egid nr with Energiebezugsfläche
        (
            2759652.9068137,
            1191423.1268269215,
        ),  # no egid number
        (
            2759746.044642407,
            1191415.6188414234,
        ),  # single egid number
        (
            2759772.4989033034,
            1191611.9958049427,
        ),  # Energie-/Wärmequelle Heizung= Unbestimmt & official building = NN
        (
            2760073.7106244904,
            1191456.8678512666,
        ),  # Werden Flächen beheizt? --> Nein  and Ist ein Warmwasseranschluss geplant? --> Nein
        (
            2759626.1504406286,
            1191908.3321774867,
        ),  # Ist ein Warmwasseranschluss geplant? --> Nein
    ],
)
@pytest.mark.vcr()
def test_ech0206_client(
    db,
    admin_client,
    snapshot,
    vcr_config,
    ech0206__config,
    query_x,
    query_y,
    ech0206_data_sources,
):
    query = {"markers": [{"x": query_x, "y": query_y}], "geometry": "POINT"}
    response = admin_client.get(
        reverse("gis-data"),
        data={
            "query": json.dumps(query),
            "form": "baugesuch",
        },
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())
