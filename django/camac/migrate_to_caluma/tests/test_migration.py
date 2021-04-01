import pytest

from camac.migrate_to_caluma.management.commands.migrate_cases import extract_parcels


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
