import pytest
from caluma.caluma_form.models import Question
from django.core.cache import cache
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def be_data_sources(
    question_factory, question_option_factory, option_factory, settings
):
    call_command("loaddata", settings.ROOT_DIR("kt_bern/config/gis.json"))
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
                "s3-s3zu",
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
            for i, option in enumerate(reversed(config[2])):
                question_option_factory(
                    question=q,
                    option=option_factory(slug=f"{slug}-{option}", label=option),
                    sort=i,
                )

    return GISDataSource.objects.all()


@pytest.mark.parametrize(
    "egrids",
    [
        "CH673533354667",
        "CH643546955207",
        "CH851446093521",
        "CH396480523621",
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
    gis_snapshot,
    vcr_config,
    egrids,
    be_data_sources,
    settings,
):
    # TODO: Update testing when sync=True works for testing, django_q sync=True is still broken.
    cache.clear()
    settings.BE_GIS_ENABLE_QUEUE = False
    settings.GIS_REQUESTS_BATCH_SIZE = 1

    response = admin_client.get(
        reverse("gis-data"),
        data={
            "egrids": egrids,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == gis_snapshot


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
    gis_snapshot,
    vcr_config,
    egrids,
    be_data_sources,
    settings,
):
    settings.BE_GIS_ENABLE_QUEUE = False

    response = admin_client.get(
        reverse("gis-data"),
        data={
            "egrids": egrids,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == gis_snapshot
