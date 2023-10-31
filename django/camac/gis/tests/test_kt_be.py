import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def be_data_sources(question_factory, question_option_factory, option_factory):
    gis_questions = [
        ("nutzungszone", Question.TYPE_TEXT),
        ("ueberbauungsordnung", Question.TYPE_TEXT),
        ("gebiet-mit-archaeologischen-objekten", Question.TYPE_CHOICE, ["ja", "nein"]),
        ("belasteter-standort", Question.TYPE_CHOICE, ["ja", "nein"]),
        ("handelt-es-sich-um-ein-baudenkmal", Question.TYPE_CHOICE, ["ja", "nein"]),
        ("gebiet-mit-naturgefahren", Question.TYPE_CHOICE, ["ja", "nein"]),
        (
            "objekt-des-besonderen-landschaftsschutzes",
            Question.TYPE_CHOICE,
            ["ja", "nein"],
        ),
        ("naturschutz", Question.TYPE_CHOICE, ["ja", "nein"]),
        (
            "gewaesserschutzbereich-v2",
            Question.TYPE_MULTIPLE_CHOICE,
            ["ueb", "ao", "au"],
        ),
        (
            "grundwasserschutzzonen-v2",
            Question.TYPE_MULTIPLE_CHOICE,
            [
                "s1",
                "s2",
                "s3zu",
                "sh",
                "sm",
                "sa",
                "sbw",
            ],
        ),
    ]
    for config in gis_questions:
        slug = config[0]
        type = config[1]
        q = question_factory(slug=slug, type=type, label=slug)
        if len(config) == 3:
            for option in config[2]:
                question_option_factory(
                    question=q,
                    option=option_factory(slug=f"{slug}-{option}", label=option),
                )

    return GISDataSource.objects.all()


@pytest.fixture
def be__config(gis_data_source_factory):
    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "service_code": "of_inlandwaters01_de_ms_wfs",
            "layers": {
                "GSK25_GSK_VW_3275": {
                    "is_boolean": False,
                    "properties": [
                        {
                            "question": "gewaesserschutzbereich-v2",
                            "mapper": "gewaesserschutzbereich_v2",
                        },
                        {
                            "question": "grundwasserschutzzonen-v2",
                            "mapper": "grundwasserschutzzonen_v2",
                        },
                    ],
                }
            },
        },
    )

    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "layers": {
                "BALISKBS_KBS_VW_1764": {
                    "is_boolean": True,
                    "properties": [
                        {"mapper": "boolean", "question": "belasteter-standort"}
                    ],
                }
            },
            "service_code": "of_environment02_de_ms_wfs",
        },
    )

    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "layers": {
                "GK5_SY_VW_21534": {
                    "is_boolean": True,
                    "properties": [
                        {"mapper": "boolean", "question": "gebiet-mit-naturgefahren"}
                    ],
                }
            },
            "service_code": "of_geoscientificinformation01_de_ms_wfs",
        },
    )

    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "service_code": "of_structure01_de_ms_wfs",
            "layers": {
                "BAUINV_BAUINVGB_VW_13644": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "handelt-es-sich-um-ein-baudenkmal",
                            "mapper": "boolean",
                        }
                    ],
                }
            },
        },
    )

    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "service_code": "of_planningcadastre01_de_ms_wfs",
            "layers": {
                "UZP_LSG_VW_13624": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "objekt-des-besonderen-landschaftsschutzes",
                            "mapper": "boolean",
                        }
                    ],
                },
                "UZP_UEO_VW_13678": {
                    "is_boolean": False,
                    "properties": [
                        {
                            "question": "ueberbauungsordnung",
                            "mapper": "ueberbauungsordnung",
                        }
                    ],
                },
                "UZP_BAU_VW_13587": {
                    "is_boolean": False,
                    "properties": [
                        {"question": "nutzungszone", "mapper": "nutzungszone"}
                    ],
                },
            },
        },
    )

    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "service_code": "of_environment01_de_ms_wfs",
            "layers": {
                "NSG_NSGP_VW_13597": {
                    "is_boolean": True,
                    "properties": [{"question": "naturschutz", "mapper": "boolean"}],
                }
            },
        },
    )

    gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "service_code": "of_society01_de_ms_wfs",
            "layers": {
                "ARCHINV_FUNDST_VW_14657": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "gebiet-mit-archaeologischen-objekten",
                            "mapper": "boolean",
                        }
                    ],
                }
            },
        },
    )

    return GISDataSource.objects.all()


@pytest.mark.parametrize(
    "egrids",
    [
        "CH673533354667",
        "CH643546955207",
        "CH851446093521",
        "CH673533354667,CH643546955207",
        "CH673533354667,CH851446093521",
        "CH643546955207,CH851446093521",
        "CH643546955207,CH843546955632",
        "CH643546955207,CH851446093521,CH673533354667",
    ],
)
@pytest.mark.vcr()
def test_be_client(
    db,
    admin_client,
    snapshot,
    vcr_config,
    be__config,
    egrids,
    be_data_sources,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={
            "egrids": egrids,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.parametrize(
    "egrids",
    [
        "doesntexist",
        "emptypolygon",
        "emptygis",
    ],
)
@pytest.mark.vcr()
def test_be_client_error(
    db,
    admin_client,
    snapshot,
    vcr_config,
    be__config,
    egrids,
    be_data_sources,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={
            "egrids": egrids,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    snapshot.assert_match(response.json())
