import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.clients.base import GISBaseClient
from camac.gis.models import GISDataSource


class FakeClient(GISBaseClient):
    def process_data_source(self, config, intermediate_data):
        return {
            "text-question": "foo",
            "table-question": [
                {
                    "table-question-1": "row 1 value 1",
                    "table-question-2": "row 1 value 2",
                },
                {
                    "table-question-1": "row 2 value 1",
                    "table-question-2": "row 2 value 2",
                },
            ],
        }


@pytest.mark.django_db
def test_process_data_source(gis_data_source):
    gis_client = GISBaseClient(GISDataSource.objects.all())
    fake_data = {}

    with pytest.raises(NotImplementedError):
        gis_client.process_data_source(gis_data_source, fake_data)


@pytest.mark.django_db
def test_view_structure(
    admin_client,
    celery_fake_worker,
    gis_data_source_factory,
    mocker,
    caluma_question_factory,
    gis_snapshot,
):
    caluma_question_factory(
        slug="text-question",
        label="Text Question",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        slug="table-question",
        label="Table Question",
        type=Question.TYPE_TABLE,
        row_form__slug="table-form",
    )
    caluma_question_factory(
        slug="table-question-1",
        label="Question 1 in table",
        type=Question.TYPE_TEXT,
    )
    caluma_question_factory(
        slug="table-question-2",
        label="Question 2 in table",
        type=Question.TYPE_TEXT,
    )

    gis_data_source_factory()

    gis_client_mock = mocker.patch(
        "camac.gis.tasks._get_client", return_value=FakeClient
    )
    mocker.patch("camac.gis.models.GISDataSource.get_required_params", return_value=[])

    # TODO: call counts
    assert gis_client_mock.call_count == 0

    # First round - tasks were only scheduled
    response = admin_client.get(reverse("gis-data"))
    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    # Run the task
    celery_fake_worker.run_tasks(raise_errors=True)

    assert gis_client_mock.call_count == 1

    # Second round - tasks should be completed now and have data
    response = admin_client.get(reverse("gis-data", args=[data["task_id"]]))
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == gis_snapshot
