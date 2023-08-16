import pytest
from django.urls import reverse
from rest_framework import status

from camac.gis.models import GISConfig


@pytest.fixture
def param_config(gis_config_factory, question_factory):
    question_factory(slug="parzellen")
    question_factory(slug="lagekoordinaten-ost")
    question_factory(slug="lagekoordinaten-nord")

    return gis_config_factory(
        client=GISConfig.CLIENT_PARAM,
        config={
            "x": {"question": "parzellen.lagekoordinaten-ost", "cast": "float"},
            "y": {"question": "parzellen.lagekoordinaten-nord", "cast": "float"},
        },
    )


def test_param_client(db, admin_client, param_config, snapshot):
    response = admin_client.get(
        reverse("gis-data"), data={"x": 2607160.642708333, "y": 1228434.884375}
    )

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


def test_required_params(db, admin_client, gis_config_factory):
    gis_config_factory(
        client=GISConfig.CLIENT_PARAM,
        config={
            "test": {"question": "some-question"},
        },
    )

    response = admin_client.get(reverse("gis-data"))

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == "Required parameter test was not passed"
