import pytest

from .. import utils

SOME_TEST_DICT = {"foo": {"bar": {"this": {"goes": {"even": {"deeper": "a value"}}}}}}


def test_get_dict_item():
    assert (
        utils.get_dict_item(SOME_TEST_DICT, "foo.bar.this.goes.even.deeper")
        == "a value"
    )

    assert (
        utils.get_dict_item(SOME_TEST_DICT, "foo!bar!this!goes!even!deeper", sep="!")
        == "a value"
    )


def test_get_dict_item_fail():
    with pytest.raises(KeyError) as excinfo:
        utils.get_dict_item(SOME_TEST_DICT, "foo.bar.this.goes.wrong.here")

    assert excinfo.match("foo.bar.this.goes.wrong")


def test_get_dict_item_default():
    res = utils.get_dict_item(
        SOME_TEST_DICT, "foo.bar.this.goes.wrong.here", default="blah"
    )

    assert res == "blah"
