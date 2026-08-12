import json
from urllib.parse import parse_qs, urlencode, urlparse

import pytest
from caluma.caluma_form.models import Question
from django.http import QueryDict
from shapely import LineString

from camac.gis.clients.admin import AdminGisClient

MARKERS = [(2607000, 1228000), (2607100, 1228000), (2607100, 1228100)]


def make_client(markers=MARKERS[:1], geometry="POINT"):
    query = json.dumps(
        {"markers": [{"x": x, "y": y} for x, y in markers], "geometry": geometry}
    )

    return AdminGisClient(QueryDict(urlencode({"query": query})))


def spatial_param(geometry, markers=MARKERS, buffer=0):
    return make_client(markers, geometry)._build_spatial_param(
        [{"x": x, "y": y} for x, y in markers], geometry, buffer
    )


def rings(param):
    return json.loads(param["geometry"])["rings"]


@pytest.mark.parametrize(
    ("buffer", "expected"),
    [
        (0, "2607000.0,1228000.0,2607000.0,1228000.0"),
        (100, "2606950.0,1227950.0,2607050.0,1228050.0"),
    ],
)
def test_admin_client_sends_a_point_as_an_envelope(buffer, expected):
    """A buffered point stays the box it has always been sent as, not a circle."""
    assert spatial_param("POINT", MARKERS[:1], buffer) == {
        "geometryType": "esriGeometryEnvelope",
        "geometry": expected,
    }


def test_admin_client_sends_an_unbuffered_line_as_a_polyline():
    """A ring would match what the line encloses instead of what it crosses."""
    param = spatial_param("LINESTRING")

    assert param["geometryType"] == "esriGeometryPolyline"
    assert json.loads(param["geometry"]) == {"paths": [[list(m) for m in MARKERS]]}


@pytest.mark.parametrize("geometry", ["LINESTRING", "POLYGON"])
def test_admin_client_sends_a_buffered_shape_as_a_ring(geometry):
    param = spatial_param(geometry, buffer=50)

    assert param["geometryType"] == "esriGeometryPolygon"

    (closed,) = rings(param)
    assert closed[0] == closed[-1], "the ring has to be closed"

    xs = [x for x, _ in closed]
    ys = [y for _, y in closed]
    assert min(xs) < min(x for x, _ in MARKERS)
    assert max(ys) > max(y for _, y in MARKERS)


def test_admin_client_sends_a_single_ring_for_a_looping_line():
    """A line drawn back onto itself leaves a hole that cannot be sent.

    `identify` answers `400 Please provide a valid geometry` to any `rings` array
    that does not hold exactly one ring. That was checked against the live API
    with a hole, with a disjoint ring and with a copy of the first ring. So the
    enclosed area gets reported as covered, even though the buffer never reaches
    it.
    """
    loop = [(2607000, 1228000), (2607400, 1228000), (2607400, 1228400)]
    loop += [(2607000, 1228400), loop[0]]

    drawn = LineString(loop).buffer(25)
    assert len(drawn.interiors) == 1, "the loop does enclose a hole"

    (outline,) = rings(spatial_param("LINESTRING", loop, buffer=50))
    assert outline == [list(point) for point in drawn.exterior.coords]


@pytest.mark.django_db
def test_admin_client_process_data_source(
    caluma_question_factory, requests_mock, settings
):
    caluma_question_factory(slug="bundesinventare", type=Question.TYPE_TEXTAREA)
    caluma_question_factory(slug="flaeche", type=Question.TYPE_INTEGER)

    settings.ADMIN_GIS_BASE_URL = "https://example.com"
    settings.ADMIN_GIS_VERIFY_SSL = True

    requests_mock.get(
        "https://example.com/rest/services/api/MapServer/identify",
        json={
            "results": [
                {
                    "layerName": "Auen",
                    "attributes": {"name": "Emme", "flaeche": 42, "leer": ""},
                },
                {
                    "layerName": "Hochmoore",
                    "attributes": {"name": "Balmoos", "flaeche": 0},
                },
            ]
        },
    )

    data = make_client(MARKERS, "POLYGON").process_data_source(
        {
            "layers": ["ch.bafu.bundesinventare-auen"],
            "buffer": 100,
            "attributes": [
                {
                    "attributeName": "name",
                    "question": "bundesinventare",
                    "template": "{label}: {value}",
                },
                # Falsy values are skipped, so only the first result counts.
                {"attributeName": "flaeche", "question": "flaeche", "cast": "integer"},
                {"attributeName": "fehlt", "question": "bundesinventare"},
            ],
        },
        None,
    )

    assert data == {
        "bundesinventare": "Auen: Emme, Hochmoore: Balmoos",
        "flaeche": 42,
    }

    query = parse_qs(urlparse(requests_mock.request_history[0].url).query)
    assert query["layers"] == ["all:ch.bafu.bundesinventare-auen"]
    assert query["geometryType"] == ["esriGeometryPolygon"]


@pytest.mark.django_db
def test_admin_client_returns_nothing_without_results(requests_mock, settings):
    settings.ADMIN_GIS_BASE_URL = "https://example.com"
    settings.ADMIN_GIS_VERIFY_SSL = True

    requests_mock.get(
        "https://example.com/rest/services/api/MapServer/identify",
        json={"error": {"code": 400}},
    )

    assert (
        make_client().process_data_source(
            {"layers": ["ch.bafu.bundesinventare-auen"], "attributes": []}, None
        )
        == {}
    )


@pytest.mark.django_db
def test_admin_client_raises_runtime_error_on_http_error(requests_mock, settings):
    settings.ADMIN_GIS_BASE_URL = "https://example.com"
    settings.ADMIN_GIS_VERIFY_SSL = True

    requests_mock.get(
        "https://example.com/rest/services/api/MapServer/identify", status_code=500
    )

    with pytest.raises(RuntimeError) as exc:
        make_client().process_data_source(
            {"layers": ["ch.bafu.bundesinventare-auen"], "attributes": []}, None
        )

    assert "500" in str(exc.value)
