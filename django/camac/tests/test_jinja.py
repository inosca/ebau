import pytest

from ..jinja import dateformat, getwithdefault


@pytest.mark.parametrize("inp,expected", [("2019-12-31", "31.12.2019"), (None, "")])
def test_dateformat(inp, expected):
    formatted = dateformat(inp)
    assert formatted == expected


@pytest.mark.parametrize(
    "inp,default,expected",
    [("text", "", "text"), (None, "", ""), (None, "something", "something")],
)
def test_getwithdefault(inp, default, expected):
    formatted = getwithdefault(inp, default=default)
    assert formatted == expected
