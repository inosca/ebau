import pytest

from ..jinja import dateformat, emptystring


@pytest.mark.parametrize("inp,expected", [("2019-12-31", "31.12.2019"), (None, "")])
def test_dateformat(inp, expected):
    formatted = dateformat(inp)
    assert formatted == expected


@pytest.mark.parametrize("inp,expected", [("text", "text"), (None, "")])
def test_emptystring(inp, expected):
    formatted = emptystring(inp)
    assert formatted == expected
