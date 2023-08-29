import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISDataSource


@pytest.fixture
def param_data_source(gis_data_source_factory, question_factory):
    question_factory(slug="parzellen", type=Question.TYPE_TABLE)
    question_factory(slug="lagekoordinaten-ost", type=Question.TYPE_FLOAT)
    question_factory(slug="lagekoordinaten-nord", type=Question.TYPE_FLOAT)

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


def test_param_client(db, admin_client, param_data_source, snapshot):
    response = admin_client.get(
        reverse("gis-data"), data={"x": 2607160.642708333, "y": 1228434.884375}
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


def test_required_params(db, admin_client, gis_data_source_factory):
    gis_data_source_factory(
        client=GISDataSource.CLIENT_PARAM,
        config=[
            {"parameterName": "test", "question": "some-question"},
        ],
    )

    response = admin_client.get(reverse("gis-data"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == "Required parameter test was not passed"
