import zoneinfo
from datetime import datetime

import pytest
from pytest_lazy_fixtures import lf

from camac.instance.placeholders.utils import format_datetime


@pytest.mark.parametrize(
    ("value", "datetime_type", "expected_output", "canton_dms_settings"),
    [
        (
            datetime(
                2026, 7, 20, 14, 30, tzinfo=zoneinfo.ZoneInfo(key="Europe/Zurich")
            ),
            "createdAt",
            "20. Juli 2026, 14.30 Uhr",
            lf("sg_dms_settings"),
        ),
        (
            datetime(2026, 7, 20, 14, 30),
            "modifiedAt",
            "Zuletzt bearbeitet am 20. Juli 2026 um 14.30",
            lf("sg_dms_settings"),
        ),
        (
            datetime(2026, 7, 20, 14, 30),
            "createdAt",
            "Erstellt am 20.07.2026 um 14:30",
            lf("gr_dms_settings"),
        ),
    ],
)
def test_format_datetime(value, datetime_type, expected_output, canton_dms_settings):
    result = format_datetime(value, datetime_type)

    assert result == expected_output
