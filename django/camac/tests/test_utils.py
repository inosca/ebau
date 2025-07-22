from contextlib import nullcontext as no_exception
from datetime import date

import pytest
from django_q.tasks import async_task, result

from camac.settings.ebau_schema import ModuleApplicationConfig
from camac.settings.utils import is_module_enabled

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


@pytest.mark.parametrize(
    "input_date,expected",
    [
        [date(2025, 2, 28), False],  # Friday
        [date(2025, 3, 1), True],  # Saturday
        [date(2025, 3, 2), True],  # Sunday
        [date(2025, 3, 3), False],  # Monday
        [date(2025, 3, 4), False],  # Tuesday
        [date(2025, 3, 5), False],  # Wednesday
        [date(2025, 3, 6), False],  # Thursday
        [date(2025, 3, 7), False],  # Friday
    ],
)
def test_is_weekend(input_date, expected):
    assert utils.is_weekend_day(input_date) == expected


@pytest.mark.parametrize(
    "input_date",
    [
        date(2025, 1, 1),  # New Year's Day
        date(2025, 4, 21),  # Easter Monday
        date(2025, 5, 29),  # Ascension Day
        date(2025, 6, 9),  # Whit Monday
        date(2025, 8, 1),  # Swiss National Day
        date(2025, 12, 25),  # Christmas Day
        date(2025, 12, 26),  # St. Stephen's Day
    ],
)
def test_is_public_holiday_not_implemented(
    settings,
    input_date,
):
    """Non-implemented subdivisions should not match any public holidays."""
    settings.APPLICATION["SHORT_NAME"] = "test"

    assert not utils.is_public_holiday(input_date)


@pytest.mark.parametrize(
    "input_date,expected",
    [
        [date(2025, 1, 1), True],  # New Year's Day
        [date(2025, 1, 2), False],  # Berchtold's Day not in GR
        [date(2025, 1, 3), False],
        [date(2025, 4, 17), False],
        [date(2025, 4, 18), False],  # Good Friday not in GR
        [date(2025, 4, 19), False],
        [date(2025, 4, 20), False],
        [date(2025, 4, 21), True],  # Easter Monday
        [date(2025, 4, 22), False],
        [date(2025, 5, 28), False],
        [date(2025, 5, 29), True],  # Ascension Day
        [date(2025, 5, 30), False],
        [date(2025, 6, 8), False],
        [date(2025, 6, 9), True],  # Whit Monday
        [date(2025, 8, 1), True],  # Swiss National Day
        [date(2025, 8, 2), False],
        [date(2025, 12, 24), False],
        [date(2025, 12, 25), True],  # Christmas Day
        [date(2025, 12, 26), True],  # St. Stephen's Day
        [date(2025, 12, 27), False],
    ],
)
def test_is_public_holiday_gr(
    input_date,
    expected,
    set_application_gr,
):
    assert utils.is_public_holiday(input_date) == expected


@pytest.mark.parametrize("enable_delay", [True, False])
@pytest.mark.parametrize(
    "input_date,expected",
    [
        # No-holiday Friday
        [date(2025, 2, 28), date(2025, 2, 28)],
        # No holiday Monday
        [date(2025, 3, 2), date(2025, 3, 3)],
        # Weekend gap Saturday
        [date(2025, 3, 1), date(2025, 3, 3)],
        # Weekend gap Sunday
        [date(2025, 3, 3), date(2025, 3, 3)],
        # New Year's Day -> Skip new_years_day for GR,
        [date(2025, 1, 1), date(2025, 1, 2)],
        # # Saturday -> Skip weekend + easter_monday for GR
        [date(2025, 4, 19), date(2025, 4, 22)],
    ],
)
def test_delay_next_workingday(
    settings,
    input_date,
    expected,
    set_application_gr,
    enable_delay,
):
    """Check if the next working day is calculated correctly when enabled.

    The deadline is postponed to the next working day if the current day is a
    weekend or a public holiday.

    If the setting is disabled, the deadline is not postponed.
    """
    if not enable_delay:
        settings.APPLICATION["DEADLINE_POSTPONE_NEXT_WORKINGDAY"] = False
        expected = input_date

    assert utils.delay_next_workingday(input_date) == expected


@pytest.mark.parametrize(
    "fail_forever, expectation",
    [
        (True, pytest.raises(RuntimeError)),
        (False, no_exception()),
    ],
)
def test_retry_utility(fail_forever, expectation):
    foo = []

    def do_the_thing():
        # If fail_forever is True, we fail each time we're called.
        # If it's False, succeed after a few tries
        if len(foo) < 2 or fail_forever:
            foo.append(3)
            raise RuntimeError("List too short")
        return 5

    with expectation:
        assert utils.retry(do_the_thing) == 5


def _example_task(n1, n2):
    return n1 + n2


def test_django_q_sync_fixture_disabled(db):
    """Demo: Django-Q Background task without sync mode."""
    task_id = async_task(_example_task, 1, 3)
    assert task_id
    assert result(task_id, wait=10) is None


def test_django_q_sync_fixture_enabled(db, django_q_sync_mode):
    """Demo: Django-Q Background task with sync mode fixture."""
    task_id = async_task(_example_task, 1, 3)
    assert task_id
    assert result(task_id, wait=10) == 4


def test_is_module_enabled():
    assert not is_module_enabled({}, False)
    assert not is_module_enabled({}, True)

    assert not is_module_enabled({"ENABLED": None})
    assert not is_module_enabled({"ENABLED": False})
    assert is_module_enabled({"ENABLED": True})

    assert is_module_enabled({"ENABLED": None}, True)
    assert is_module_enabled({"ENABLED": False}, True)
    assert is_module_enabled({"ENABLED": True}, True)

    conf_enabled: ModuleApplicationConfig = ModuleApplicationConfig(enabled=True)
    conf_not_enabled: ModuleApplicationConfig = ModuleApplicationConfig()
    assert is_module_enabled(conf_enabled)
    assert not is_module_enabled(conf_not_enabled)

    assert is_module_enabled(conf_enabled, True)
    assert not is_module_enabled(conf_not_enabled, True)
