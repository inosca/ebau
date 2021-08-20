import datetime

import pytest

from camac.stats.cycle_time import _compute_total_idle_days


@pytest.mark.parametrize(
    "sorted_durations,expected",
    [
        (
            [
                (datetime.date(1994, 5, 25), datetime.date(1994, 5, 28)),
                (datetime.date(1994, 5, 27), datetime.date(1994, 5, 30)),
                (datetime.date(1994, 6, 4), datetime.date(1994, 6, 9)),
                (datetime.date(1994, 6, 6), datetime.date(1994, 6, 8)),
                (datetime.date(1994, 6, 7), datetime.date(1994, 6, 11)),
            ],
            12,
        )
    ],
)
def test_compute_total_idle_days(sorted_durations, expected):
    assert _compute_total_idle_days(sorted_durations) == expected
