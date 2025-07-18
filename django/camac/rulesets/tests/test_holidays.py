from camac.rulesets.holidays import (
    AargauAdministrationHolidays,
)


def test_aargau_administration_holidays(snapshot):
    holidays = AargauAdministrationHolidays(years=[2025])

    assert {d.isoformat(): n for d, n in holidays.items()} == snapshot
