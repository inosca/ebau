import pytest
from caluma.caluma_form.models import Question
from django.core.management import call_command
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
from rest_framework import status

from camac.gis.models import GISDataSource

TEST_COORDINATES = {
    "default": (2607160.642708333, 1228434.884375),
    "near-forest": (2606261.686890635, 1230671.22757022),
    "moor-and-sanctuary": (2595908.1098607033, 1223872.4541323201),
    "bln-and-ivs-regional-local": (2606265.992581233, 1235122.657259761),
    "ivs-national": (2607372.235299003, 1230212.5463196996),
    "monument": (2607376.2625398953, 1230171.7275696846),
    "crop-rotation-area": (2603913.165006131, 1227634.5322569455),
    "highway": (2611103.2977669733, 1228741.4541305029),
}


@pytest.fixture
def so_data_sources(question_factory, settings):
    call_command("loaddata", settings.ROOT_DIR("kt_so/config/gis.json"))

    gis_questions = [
        ("gemeinde", Question.TYPE_DYNAMIC_CHOICE),
        ("gemeindenummer-bfs", Question.TYPE_INTEGER),
        ("parzellen", Question.TYPE_TABLE),
        ("parzellennummer", Question.TYPE_TEXT),
        ("ort", Question.TYPE_TEXT),
        ("strasse-flurname", Question.TYPE_TEXT),
        ("strasse-nummer", Question.TYPE_TEXT),
        ("e-grid", Question.TYPE_TEXT),
        ("lagekoordinaten-ost", Question.TYPE_FLOAT),
        ("lagekoordinaten-nord", Question.TYPE_FLOAT),
        ("richtplan-grundnutzung", Question.TYPE_TEXTAREA),
        ("richtplan-weiteres", Question.TYPE_TEXTAREA),
        ("nutzungsplanung-grundnutzung", Question.TYPE_TEXTAREA),
        ("nutzungsplanung-weitere-festlegungen", Question.TYPE_TEXTAREA),
        ("weitere-gis-informationen", Question.TYPE_TEXTAREA),
        ("bundesinventare", Question.TYPE_TEXTAREA),
    ]

    for slug, type in gis_questions:
        question_factory(slug=slug, type=type)

    return GISDataSource.objects.all()


@pytest.mark.parametrize("name,coords", TEST_COORDINATES.items())
@pytest.mark.vcr()
def test_sogis_client(
    db,
    admin_client,
    snapshot,
    name,
    coords,
    so_data_sources,
    vcr_config,
):
    x, y = coords
    response = admin_client.get(reverse("gis-data"), data={"x": x, "y": y})

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())


@pytest.fixture
def so_fake_data_source(gis_data_source_factory, question_factory):
    question_factory(slug="gemeinde", type=Question.TYPE_DYNAMIC_CHOICE)

    return gis_data_source_factory(
        client=GISDataSource.CLIENT_SOGIS,
        config={
            "layer": "ch.so.agi.gemeindegrenzen.data",
            "properties": [{"propertyName": "gemeindename", "question": "gemeinde"}],
        },
    )


@pytest.fixture
def so_unknown_layer_data_source(so_fake_data_source):
    so_fake_data_source.config["layer"] = "ch.so.agi.av.unknown_layer"
    so_fake_data_source.save()

    return so_fake_data_source


@pytest.fixture
def so_unknown_property_data_source(so_fake_data_source):
    so_fake_data_source.config["properties"][0]["propertyName"] = "unknown_property"
    so_fake_data_source.save()

    return so_fake_data_source


@pytest.fixture
def so_unknown_question_data_source(so_fake_data_source):
    so_fake_data_source.config["properties"][0]["question"] = "unknown_question"
    so_fake_data_source.save()

    return so_fake_data_source


@pytest.mark.parametrize(
    "data_source,expected_status",
    [
        (lazy_fixture("so_unknown_layer_data_source"), status.HTTP_400_BAD_REQUEST),
        (lazy_fixture("so_unknown_property_data_source"), status.HTTP_200_OK),
        (lazy_fixture("so_unknown_question_data_source"), status.HTTP_200_OK),
    ],
)
@pytest.mark.vcr()
def test_sogis_client_errors(
    db,
    admin_client,
    data_source,
    expected_status,
    snapshot,
    vcr_config,
):
    response = admin_client.get(
        reverse("gis-data"),
        data={"x": TEST_COORDINATES["default"][0], "y": TEST_COORDINATES["default"][1]},
    )

    assert response.status_code == expected_status
    snapshot.assert_match(response.json())
