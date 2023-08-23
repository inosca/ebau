import pytest
from caluma.caluma_form.models import Question
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from camac.gis.models import GISConfig

DEFAULT_COORDS = (2607160.642708333, 1228434.884375)
FOREST_COORDS = (2606252.261979167, 1230759.5796875001)


@pytest.fixture
def so_simple_config(gis_config_factory, question_factory):
    question_factory(slug="gemeinde", type=Question.TYPE_DYNAMIC_CHOICE)

    return gis_config_factory(
        client=GISConfig.CLIENT_SOGIS,
        config={
            "layer": "ch.so.agi.gemeindegrenzen.data",
            "properties": [{"propertyName": "gemeindename", "question": "gemeinde"}],
        },
    )


@pytest.fixture
def so_filter_config(gis_config_factory, question_factory):
    question_factory(slug="wald", type=Question.TYPE_TEXT)

    return gis_config_factory(
        client=GISConfig.CLIENT_SOGIS,
        config={
            "layer": "ch.so.agi.av.bodenbedeckung.data",
            "filter": '[["art_txt","ilike","%Wald%"]]',
            "buffer": 50,
            "properties": [{"propertyName": "art_txt", "question": "wald"}],
        },
    )


@pytest.fixture
def so_nested_config(gis_config_factory, question_factory):
    question_factory(slug="e-grid-global", type=Question.TYPE_TEXT)
    question_factory(slug="parzellen", type=Question.TYPE_TABLE)
    question_factory(slug="e-grid", type=Question.TYPE_TEXT)
    question_factory(slug="parzellennummer", type=Question.TYPE_INTEGER)

    return gis_config_factory(
        client=GISConfig.CLIENT_SOGIS,
        config={
            "layer": "ch.so.agi.av.grundstuecke.rechtskraeftig.data",
            "properties": [
                {"propertyName": "egrid", "question": "e-grid-global"},
                {"propertyName": "egrid", "question": "parzellen.e-grid"},
                {
                    "propertyName": "nummer",
                    "question": "parzellen.parzellennummer",
                },
            ],
        },
    )


@pytest.fixture
def so_unknown_layer_config(so_simple_config):
    so_simple_config.config["layer"] = "ch.so.agi.av.unknown_layer"
    so_simple_config.save()

    return so_simple_config


@pytest.fixture
def so_unknown_property_config(so_simple_config):
    so_simple_config.config["properties"][0]["propertyName"] = "unknown_property"
    so_simple_config.save()

    return so_simple_config


@pytest.fixture
def so_unknown_question_config(so_simple_config):
    so_simple_config.config["properties"][0]["question"] = "unknown_question"
    so_simple_config.save()

    return so_simple_config


@pytest.fixture
def so_all_config(so_simple_config, so_filter_config, so_nested_config):
    return GISConfig.objects.all()


@pytest.mark.parametrize(
    "coords,config,expected_status",
    [
        (DEFAULT_COORDS, lazy_fixture("so_simple_config"), status.HTTP_200_OK),
        (FOREST_COORDS, lazy_fixture("so_filter_config"), status.HTTP_200_OK),
        (DEFAULT_COORDS, lazy_fixture("so_nested_config"), status.HTTP_200_OK),
        (DEFAULT_COORDS, lazy_fixture("so_all_config"), status.HTTP_200_OK),
        # Error test cases
        (
            DEFAULT_COORDS,
            lazy_fixture("so_unknown_layer_config"),
            status.HTTP_400_BAD_REQUEST,
        ),
        (
            DEFAULT_COORDS,
            lazy_fixture("so_unknown_property_config"),
            status.HTTP_200_OK,
        ),
        (
            DEFAULT_COORDS,
            lazy_fixture("so_unknown_question_config"),
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.vcr()
def test_sogis_client(
    db,
    admin_client,
    config,
    coords,
    expected_status,
    snapshot,
    vcr_config,
):
    response = admin_client.get(
        reverse("gis-data"), data={"x": coords[0], "y": coords[1]}
    )

    assert response.status_code == expected_status
    snapshot.assert_match(response.json())


@pytest.mark.parametrize(
    "params,message",
    [
        ({}, "Required parameter x was not passed"),
        ({"x": 123}, "Required parameter y was not passed"),
        ({"x": 123, "y": "notafloat"}, "Coordinates must be floats"),
    ],
)
def test_params(db, admin_client, so_simple_config, params, message):
    response = admin_client.get(reverse("gis-data"), data=params)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()[0] == message
