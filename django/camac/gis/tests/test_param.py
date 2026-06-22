import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def param_data_source(gis_data_source_factory, caluma_question_factory):
    caluma_question_factory(slug="parzellen", type=Question.TYPE_TABLE)
    caluma_question_factory(slug="lagekoordinaten-ost", type=Question.TYPE_FLOAT)
    caluma_question_factory(slug="lagekoordinaten-nord", type=Question.TYPE_FLOAT)

    return gis_data_source_factory(
        client=GISDataSource.CLIENT_PARAM,
        config=[
            {
                "parameterName": "x",
                "question": "parzellen.lagekoordinaten-ost",
                "cast": "float",
            },
            {
                "parameterName": "y",
                "question": "parzellen.lagekoordinaten-nord",
                "cast": "float",
            },
        ],
    )


@pytest.mark.django_db
def test_param_client(
    admin_client, param_data_source, gis_snapshot, celery_fake_worker
):
    response = admin_client.get(
        reverse("gis-data"), data={"x": 2607160.642708333, "y": 1228434.884375}
    )

    assert response.status_code == status.HTTP_200_OK
    assert "task_id" in response.json()

    celery_fake_worker.run_tasks()

    task_id = response.json()["task_id"]

    response = admin_client.get(
        reverse("gis-data", args=[task_id]),
        data={"x": 2607160.642708333, "y": 1228434.884375},
    )
    assert response.json() == gis_snapshot


@pytest.mark.django_db
def test_required_params(admin_client, gis_data_source_factory):
    gis_data_source_factory(
        client=GISDataSource.CLIENT_PARAM,
        config=[
            {"parameterName": "test", "question": "some-question"},
        ],
    )

    response = admin_client.get(reverse("gis-data"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == "Erforderlicher Parameter test wurde nicht übergeben"
