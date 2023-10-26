import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def be_data_sources(
    question_factory, question_option_factory, option_factory, settings
):
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
def be__config(gis_data_source_factory, question_factory):
    return gis_data_source_factory(
        client=GISDataSource.CLIENT_BEGIS,
        config={
            "service_code": "a42geo_ebau_kt_wfs_d_fk",
            "layers": {
                "GEODB.GSK25_GSK_VW": {
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
                },
                "BALISKBS_KBS": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "belasteter-standort",
                            "mapper": "boolean",
                        },
                    ],
                },
                "GK5_SY": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "gebiet-mit-naturgefahren",
                            "mapper": "boolean",
                        },
                    ],
                },
                "BAUINV_BAUINV_VW": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "handelt-es-sich-um-ein-baudenkmal",
                            "mapper": "boolean",
                        },
                    ],
                },
                "GEODB.UZP_LSG_VW": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "objekt-des-besonderen-landschaftsschutzes",
                            "mapper": "boolean",
                        },
                    ],
                },
                "ARCHINV_FUNDST": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "gebiet-mit-archaeologischen-objekten",
                            "mapper": "boolean",
                        },
                    ],
                },
                "NSG_NSGP": {
                    "is_boolean": True,
                    "properties": [
                        {
                            "question": "naturschutz",
                            "mapper": "boolean",
                        },
                    ],
                },
                "GEODB.UZP_BAU_VW": {
                    "is_boolean": False,
                    "properties": [
                        {
                            "question": "nutzungszone",
                        },
                    ],
                },
                "GEODB.UZP_UEO_VW": {
                    "is_boolean": False,
                    "properties": [
                        {
                            "question": "ueberbauungsordnung",
                        },
                    ],
                },
            },
        },
    )


@pytest.mark.parametrize(
    "egrid",
    [
        "CH673533354667",
        "CH643546955207",
        "CH851446093521",
    ],
)
@pytest.mark.vcr()
def test_be_client(
    db,
    admin_client,
    snapshot,
    vcr_config,
    be__config,
    egrid,
    be_data_sources,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={
            "egrid": egrid,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.mark.parametrize(
    "egrid",
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
    egrid,
    be_data_sources,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={
            "egrid": egrid,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    snapshot.assert_match(response.json())
