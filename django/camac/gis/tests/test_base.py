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


def test_process_data_source(db, gis_data_source):
    gis_client = GISBaseClient(GISDataSource.objects.all())
    fake_data = {}

    with pytest.raises(NotImplementedError):
        gis_client.process_data_source(gis_data_source, fake_data)


def test_view_structure(
    db,
    admin_client,
    gis_data_source_factory,
    mocker,
    question_factory,
    snapshot,
):
    question_factory(
        slug="text-question",
        label="Text Question",
        type=Question.TYPE_TEXT,
    )
    question_factory(
        slug="table-question",
        label="Table Question",
        type=Question.TYPE_TABLE,
        row_form__slug="table-form",
    )
    question_factory(
        slug="table-question-1",
        label="Question 1 in table",
        type=Question.TYPE_TEXT,
    )
    question_factory(
        slug="table-question-2",
        label="Question 2 in table",
        type=Question.TYPE_TEXT,
    )

    gis_data_source_factory()

    mocker.patch("camac.gis.views.get_client", return_value=FakeClient)
    mocker.patch("camac.gis.models.GISDataSource.get_required_params", return_value=[])

    response = admin_client.get(reverse("gis-data"))

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())
