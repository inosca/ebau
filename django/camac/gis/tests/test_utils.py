import pytest

from camac.gis import utils


@pytest.mark.parametrize(
    ("value", "cast", "result"),
    [
        ("1234", "integer", 1234),
        ("test", "integer", None),
        ("12.4", "float", 12.4),
        ("test", "float", None),
        (123, "string", "123"),
        (1.3, "string", "1.3"),
    ],
)
def test_cast(value, cast, result):
    assert utils.cast(value, cast) == result


def test_to_query():
    assert (
        utils.to_query({"foo": 123, "bar": False, "baz": None}) == "foo=123&bar=False"
    )


@pytest.mark.parametrize(
    ("geometry_type", "markers", "expected"),
    [
        ("POINT", [(100.123, 200.234)], "Point"),
        ("LINESTRING", [(0, 0), (10, 10)], "LineString"),
        ("POLYGON", [(0, 0), (10, 0), (10, 10)], "Polygon"),
    ],
)
def test_build_shape(geometry_type, markers, expected):
    shape = utils.build_shape([{"x": x, "y": y} for x, y in markers], geometry_type)

    assert shape.geom_type == expected


def test_buffered_spends_half_the_buffer_on_each_side():
    point = utils.build_shape([{"x": 100.123, "y": 200.234}], "POINT")

    assert utils.buffered(point).bounds == (100.123, 200.234, 100.123, 200.234)
    assert utils.buffered(point, 50).bounds == (75.123, 175.234, 125.123, 225.234)


def test_concat_values():
    assert (
        utils.concat_values("test  ", 1.123, None, "", "  test", 0) == "test, 1.123, 0"
    )
    assert utils.concat_values("test  ") == "test"
    assert utils.concat_values(17) == 17
    assert utils.concat_values(None, 12.3) == 12.3
