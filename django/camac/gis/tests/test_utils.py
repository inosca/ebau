import pytest

from camac.gis import utils


@pytest.mark.parametrize(
    "value,cast,result",
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


def test_get_bbox():
    assert utils.get_bbox(100.123, 200.234) == "100.123,200.234,100.123,200.234"
    assert utils.get_bbox(100.123, 200.234, 50) == "75.123,175.234,125.123,225.234"
    assert utils.get_bbox("1.1", "2.2") == "1.1,2.2,1.1,2.2"

    with pytest.raises(ValueError) as e:
        utils.get_bbox("abc", "def")

    assert str(e.value) == "Koordinaten müssen Gleitkommazahlen sein"


def test_join():
    assert utils.join("test", 1.123, None, "", "test", 0) == "test, 1.123, 0"
