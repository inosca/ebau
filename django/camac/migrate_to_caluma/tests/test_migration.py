import pytest

from camac.migrate_to_caluma.management.commands.migrate_cases import extract_parcels
from camac.migrate_to_caluma.transforms import Transform


@pytest.mark.parametrize(
    "input,expected",
    [
        ("1,1208,2", [1, 2]),
        ("1208 / 1 / 39", [1, 39]),
        ("1208 + 1", [1]),
        ("1208 und 1", [1]),
        ("1208 und 1", [1]),
        ("1218-329 / 1218-327 / 1218-326", [329, 327, 326]),
        ("L867.1213", [867]),
        ("div. Pz.", []),
        ("D (1396)", [1396]),
        ("1098.1205", [1098]),
    ],
)
def test_parcel_extraction(input, expected):
    assert extract_parcels(input) == expected


@pytest.mark.parametrize(
    "input,expected",
    [
        ("1 Mio", "1000000"),
        ("1 mio", "1000000"),
        ("24 Mio.", "24000000"),
        ("24'000 Mio.", "24000000000"),
        ("24.00 Fr", "24"),
        ("30.00 Fr", "30"),
        ("Fr. 30.00", "30"),
        ("Fr. 30.50", "30.5"),
        ("Fr. 30.000", "30"),
        ("Mio 2.4", "2400000"),
    ],
)
def test_extract_number(input, expected):
    assert Transform.extract_number(input) == expected
