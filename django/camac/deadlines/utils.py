from datetime import date

from django.conf import settings

from camac.settings.modules.deadlines_schema import CalculationConfig
from camac.utils import is_public_holiday, is_weekend_day


def exclude_suspension_date(date: date) -> bool:
    if not settings.DEADLINES:  # pragma: no cover
        return False

    calculation_settings: CalculationConfig = settings.DEADLINES.calculation

    return (calculation_settings.exclude_weekends and is_weekend_day(date)) or (
        calculation_settings.exclude_public_holidays and is_public_holiday(date)
    )
