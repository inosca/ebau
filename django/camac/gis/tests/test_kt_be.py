import pytest
from caluma.caluma_form.models import Question
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def vcr_config():
    # also match on body to avoid egrid response mismatch due to the out of order threaded handling
    return {
        "match_on": ["method", "scheme", "host", "port", "path", "query", "body"],
    }


@pytest.fixture
def be_data_sources(
    caluma_question_factory,
    caluma_question_option_factory,
    caluma_option_factory,
    settings,
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
        q = caluma_question_factory(slug=slug, type=type, label=slug)
        if len(config) == 3:
            for i, option in enumerate(reversed(config[2])):
                caluma_question_option_factory(
                    question=q,
                    option=caluma_option_factory(slug=f"{slug}-{option}", label=option),
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
    celery_fake_worker,
    egrids,
    be_data_sources,
    settings,
):
    # TODO: Update testing when sync=True works for testing, django_q sync=True is still broken.
    settings.BE_GIS_ENABLE_QUEUE = False
    # Without this, threads may run out-of-order and cause VCRpy to return
    # the wrong data (or fail)
    settings.GIS_REQUESTS_BATCH_SIZE = 1

    response_0 = admin_client.get(
        reverse("gis-data"),
        data={
            "egrids": egrids,
        },
    )
    task_id = response_0.json()["task_id"]

    celery_fake_worker.run_tasks()

    response = admin_client.get(
        reverse("gis-data", args=[task_id]),
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
@pytest.mark.vcr(allow_playback_repeats=True)
@pytest.mark.parametrize(
    "run_task, expected_result",
    [
        (True, status.HTTP_400_BAD_REQUEST),
        (False, status.HTTP_202_ACCEPTED),
    ],
)
def test_be_client_error(
    db,
    admin_client,
    gis_snapshot,
    vcr_config,
    celery_fake_worker,
    be_data_sources,
    settings,
    egrids,
    run_task,
    expected_result,
):
    # Without this, threads may run out-of-order and cause VCRpy to return
    # the wrong data (or fail)
    settings.GIS_REQUESTS_BATCH_SIZE = 1

    response_0 = admin_client.get(
        reverse("gis-data"),
        data={
            "egrids": egrids,
        },
    )
    task_id = response_0.json()["task_id"]

    # Run the task - and we expect the task to fail, as we want
    # to check the error reporting state afterwards
    if run_task:
        celery_fake_worker.run_tasks(raise_errors=False)

    response = admin_client.get(
        reverse("gis-data", args=[task_id]),
        data={
            "egrids": egrids,
        },
    )

    assert response.status_code == expected_result

    if expected_result == status.HTTP_400_BAD_REQUEST:
        error_data = response.json()

        # Before snapshot: This needs to be the same structure as
        # when processed by Celery in the actual background task.
        assert "detail" in error_data
        assert isinstance(error_data["detail"], str)
        assert error_data == gis_snapshot

    else:
        # 202 has no data - task is just simply not scheduled yet
        assert response.content == b""
