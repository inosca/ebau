import json
import re
from xml.dom import minidom
from xml.etree import ElementTree as ET

import pytest

from camac.gis_export.formatters import (
    ENTSCHEID_VALUES,
    FACHSTELLEN_VALUES,
    STATUS_BY_STATE,
    STATUS_VALUES,
    ExportValidationError,
    _child_type,
    _geometrie,
    _geometrie_flaeche,
    _geometrie_linie,
    _geometrie_punkt,
    _grundstuecke,
    _map_fachstelle,
    _map_status,
    _validate,
    build_sogis_transfer_xml,
)
from camac.gis_export.models import SOGISExport
from camac.gis_export.so_schema import (
    INTERLIS,
    SO_DSBJD_eBauSO_Geschaefte_20250422 as so_schema,
)

MODEL_TAG = re.compile(r"<ns\d+:(\w+)")


def _drawn(geometry_type: str, points: list[dict]) -> str:
    """Render points as the `gis-karte` answer the map would have written."""
    return json.dumps(
        {
            "geometry": geometry_type,
            "markers": [{"x": v["ost"], "y": v["nord"]} for v in points],
        }
    )


def _mandatory_export(instance_id: int, **overrides) -> SOGISExport:
    """Build an unsaved export holding only what the .ili marks MANDATORY.

    The value types mirror their Caluma questions: `plz` is text, the
    coordinates are numeric.
    """
    fields = {
        "identifikator": f"2601-2026-{instance_id}",
        "bfsnr": 2601,
        "verfahrensart": "Baugesuch",
        "status": "Pruefung.formell",
        "ebau_link": f"https://ebau.example/cases/{instance_id}",
        # Satisfies MANDATORY CONSTRAINT DEFINED(Geometrie_Punkt) OR ...
        "plot_point": {"ost": 2607000.5, "nord": 1228500.5},
        "gesuchsteller": [
            {
                "adresse": {
                    "natuerliche_person": {"name": "Muster", "vorname": "Reto"},
                    "adresse": {"plz": "4500", "ortschaft": "Solothurn"},
                },
                "vertretung": None,
            }
        ],
        "grundstuecke": [{"nummer": "1234", "egrid": "CH807306613464"}],
    }
    fields.update(overrides)

    return SOGISExport(instance_id=instance_id, hash=f"hash-{instance_id}", **fields)


def _person_adresse(name: str, vorname: str) -> dict:
    return {
        "natuerliche_person": {"name": name, "vorname": vorname},
        "juristische_person": {"name": f"{name} AG"},
        "adresse": {
            "strassenname": "Teststrasse",
            "hausnummer": "12a",
            "plz": "4500",
            "ortschaft": "Solothurn",
        },
    }


def _full_export(instance_id: int) -> SOGISExport:
    """Build an unsaved export covering every attribute the serializer maps.

    Choice answers carry the option label, never the slug. The slugs would
    also exceed the TEXT*20 limit on Arbeiten_Art and Bauwerk_Art.
    """
    return _mandatory_export(
        instance_id,
        ausserhalb_bauzone=True,
        lokalisation={
            "strassenname": "Baustellenweg",
            "hausnummer": "12",
            "plz": "4500",
            "ortschaft": "Solothurn",
        },
        # A BAG {1..*}: the first applicant carries a Vertretung, the second none.
        gesuchsteller=[
            {
                "adresse": _person_adresse("Muster", "Reto"),
                "vertretung": _person_adresse("Vertretung", "Vera"),
            },
            {
                "adresse": _person_adresse("Beispiel", "Bea"),
                "vertretung": None,
            },
        ],
        projektverfasser=_person_adresse("Verfasser", "Peter"),
        rechnungsempfaenger=_person_adresse("Empfaenger", "Rita"),
        grundeigentuemer=_person_adresse("Eigentuemer", "Greta"),
        bauprojekt={
            "beschreibung": "Neubau Mehrfamilienhaus mit Tiefgarage",
            "bauwerk_art": ["Hochbaute", "Tiefbaute"],
            "nutzungszweck": ["Wohnen", "Arbeiten (Gewerbebetrieb)"],
            "bauwerke": [
                {
                    "bezeichnung": "MFH A",
                    "bauwerk_typ": (
                        "Mehrfamilienhaus (reines Wohngebäude mit mehreren Wohnungen)"
                    ),
                    "egid": 123456,
                    "arbeiten_art": ["Neubau", "Umbau", "Abbruch"],
                    "gebaeudekategorie": "Gebäude mit ausschliesslicher Wohnnutzung",
                },
                {
                    "bezeichnung": "Garage",
                    "bauwerk_typ": (
                        "Garage / Einstellhallen im Zusammenhang mit Wohngebäuden"
                    ),
                    "egid": None,
                    "arbeiten_art": ["Neubau"],
                    "gebaeudekategorie": "Gebäude ohne Wohnnutzung",
                },
            ],
        },
        # Only the four form decisions that have an INTERLIS equivalent.
        entscheid={"entscheid": "Teilzustimmung", "datum": "2026-05-01"},
        auflage={"startdatum": "2026-05-01", "enddatum": "2026-05-31"},
        zirkulation=[
            {"slug": "afu", "name": None, "abteilung": "Amt fuer Umwelt"},
            {"slug": "arp", "name": None, "abteilung": "Amt fuer Raumplanung"},
        ],
        zustaendige_person={
            "group_slug": "municipality",
            "name": "Hans Muster",
            "abteilung": "Bauverwaltung Solothurn",
        },
        grundstuecke=[
            {"nummer": "1234", "egrid": "CH807306613464"},
            {"nummer": "5678", "egrid": "CH119325434847"},
        ],
    )


def _validated(xml: str) -> str:
    """Validate against the schema, then canonicalize for the snapshot.

    A snapshot alone would happily record malformed output, and PyXB orders
    the xmlns declarations differently on every run.
    """
    INTERLIS.CreateFromDocument(xml.encode("utf-8"))

    return minidom.parseString(ET.canonicalize(xml)).toprettyxml(indent="  ")


def _unserialized(xml: str) -> set[str]:
    """Attributes the .ili declares that never made it into the document."""
    emitted = set(MODEL_TAG.findall(xml))

    return {name.localName() for name in so_schema.GeschaeftType._ElementMap} - emitted


def test_build_sogis_transfer_xml_with_mandatory_fields_only(snapshot):
    exports = [_mandatory_export(1), _mandatory_export(2), _mandatory_export(3)]

    xml = build_sogis_transfer_xml(exports).xml

    snapshot.assert_match(_validated(xml))


def test_build_sogis_transfer_xml_with_all_fields(snapshot):
    exports = [_full_export(1), _full_export(2)]

    xml = build_sogis_transfer_xml(exports).xml

    snapshot.assert_match(_validated(xml))

    # This dossier carries a point, so the line and polygon variants are absent.
    assert _unserialized(xml) == {
        "Geometrie_Linie",
        "Geometrie_Flaeche",
    }


def _build(**overrides) -> None:
    _validate(_mandatory_export(1, **overrides))


POINTS = [
    {"ost": "2607000.5", "nord": "1228500.5"},
    {"ost": "2607100.5", "nord": "1228500.5"},
    {"ost": "2607100.5", "nord": "1228600.5"},
]


def test_validate_requires_at_least_one_geometry():
    with pytest.raises(ExportValidationError, match="no usable geometry"):
        _build(plot_point=None)


@pytest.mark.parametrize(
    ("geometry_type", "points"),
    [("LINESTRING", POINTS[:2]), ("POLYGON", POINTS)],
)
def test_validate_accepts_a_geometry_other_than_punkt(geometry_type, points):
    _build(plot_point=None, gis_geometry=_drawn(geometry_type, points))


@pytest.mark.parametrize(
    ("geometry_type", "points"),
    [
        # Too few points to form a line or a ring.
        ("LINESTRING", POINTS[:1]),
        ("POLYGON", POINTS[:2]),
        # Enough points, but one is unusable. Dropping it would silently
        # reshape the geometry, so the whole dossier has to be reported.
        ("LINESTRING", [POINTS[0], {"ost": "2607100.5", "nord": None}]),
        ("POLYGON", [*POINTS[:2], {"ost": "abc", "nord": "def"}]),
    ],
)
def test_validate_rejects_an_unusable_geometry(geometry_type, points):
    with pytest.raises(ExportValidationError, match="no usable geometry"):
        _build(plot_point=None, gis_geometry=_drawn(geometry_type, points))


@pytest.mark.parametrize(
    "gis_geometry",
    [
        "not json at all",
        '{"markers": null, "geometry": "POINT"}',
        '{"markers": [], "geometry": "POLYGON"}',
        '{"markers": [{"x": 1, "y": 2}], "geometry": "MULTIPOLYGON"}',
        "123",
        "[1, 2]",
        '{"markers": 5, "geometry": "POINT"}',
        '{"markers": [7], "geometry": "POINT"}',
    ],
)
def test_validate_rejects_an_unreadable_map_answer(gis_geometry):
    """A damaged answer is this dossier's problem, not the whole batch's."""
    with pytest.raises(ExportValidationError, match="no usable geometry"):
        _build(plot_point=None, gis_geometry=gis_geometry)


@pytest.mark.parametrize(
    "plot_point",
    [
        {"ost": 2607000.5, "nord": ""},
        {"ost": "", "nord": 1228500.5},
        {"ost": 2607000.5},
        {"ost": 2607000.5, "nord": None},
        # A text answer where a number is expected is a data problem, not a
        # bug, so it has to be reported like any other invalid dossier.
        {"ost": "abc", "nord": "def"},
        {"ost": 2607000.5, "nord": "1'228'500"},
        # LV03, the old Swiss grid - the realistic operator mistake.
        {"ost": 600000, "nord": 200000},
        # East and north swapped.
        {"ost": 1228500.5, "nord": 2607000.5},
    ],
)
def test_validate_rejects_an_unusable_punkt(plot_point):
    with pytest.raises(ExportValidationError, match="no usable geometry"):
        _build(plot_point=plot_point)


def test_drawn_geometry_wins_over_the_plot_point():
    export = _mandatory_export(
        1,
        plot_point={"ost": 1.0, "nord": 2.0},
        gis_geometry=_drawn("LINESTRING", POINTS[:2]),
    )

    assert _geometrie(export)[0] == "Geometrie_Linie"


@pytest.mark.parametrize(
    "status",
    [
        "not-a-status",
        None,  # an instance state _map_status does not map
        "",
        "Pruefung",  # only the leaves of the nested enum are valid values
    ],
)
def test_validate_rejects_unknown_status(status):
    with pytest.raises(ExportValidationError, match="is not a Status_Geschaeft value"):
        _build(status=status)


@pytest.mark.parametrize("status", sorted(STATUS_VALUES))
def test_validate_accepts_every_status_value(status):
    _build(status=status)


@pytest.mark.parametrize("state", sorted(STATUS_BY_STATE))
def test_map_status_maps_every_instance_state_to_an_enum_value(state):
    assert _map_status(state) in STATUS_VALUES


def test_map_status_returns_unknown_states_unchanged():
    assert _map_status("not-a-state") == "not-a-state"
    assert _map_status(None) is None


@pytest.mark.parametrize(
    "entscheid",
    [
        "Teilrueckzug",
        "beschwerde-bestaetigt",
    ],
)
def test_validate_rejects_unknown_entscheid(entscheid):
    with pytest.raises(ExportValidationError, match="is not an Entscheid value"):
        _build(entscheid={"entscheid": entscheid, "datum": "2026-05-01"})


@pytest.mark.parametrize("entscheid", [None, {}])
def test_validate_ignores_absent_entscheid(entscheid):
    _build(entscheid=entscheid)


@pytest.mark.parametrize("entscheid", sorted(ENTSCHEID_VALUES))
def test_validate_accepts_every_entscheid_value(entscheid):
    _build(entscheid={"entscheid": entscheid, "datum": "2026-05-01"})


@pytest.mark.parametrize(
    "service",
    [
        {"slug": "afu"},
        {"parent_slug": "afu"},
        {"slug": "arp"},
        {"slug": "arp-leitbehoerde"},
        {"group_slug": "municipality"},
        {"group_slug": "service-extra-cantonal"},
        {"slug": "sgv"},
    ],
)
def test_fachstelle_maps_known_services(service):
    assert _map_fachstelle(service) in FACHSTELLEN_VALUES


@pytest.mark.parametrize("service", [{"slug": "not-a-service"}, {"slug": None}, {}])
def test_fachstelle_does_not_map_unknown_services(service):
    assert _map_fachstelle(service) is None


@pytest.mark.parametrize("service", [{"slug": "not-a-service"}, {"slug": None}])
def test_validate_rejects_unmappable_fachstelle_in_zirkulation(service):
    with pytest.raises(ExportValidationError, match="is not a Fachstellen value"):
        _build(zirkulation=[{**service, "abteilung": "Amt"}])


@pytest.mark.parametrize("service", [{"slug": "not-a-service"}, {"slug": None}])
def test_validate_rejects_unmappable_fachstelle_in_zustaendige_person(service):
    with pytest.raises(ExportValidationError, match="is not a Fachstellen value"):
        _build(zustaendige_person={**service, "name": "Hans"})


def test_validate_reports_every_violation_at_once():
    with pytest.raises(ExportValidationError) as exc_info:
        _build(
            plot_point=None,
            status="not-a-status",
            entscheid={"entscheid": "Teilrueckzug"},
            zirkulation=[{"slug": "not-a-service"}],
            zustaendige_person={"slug": "also-not-a-service"},
        )

    message = str(exc_info.value)

    assert message.startswith("Export '2601-2026-1': ")
    assert message.count(";") == 4
    for expected in (
        "no usable geometry",
        "Status 'not-a-status'",
        "Entscheid 'Teilrueckzug'",
        "service 'not-a-service'",
        "service 'also-not-a-service'",
    ):
        assert expected in message


def test_geometrie_punkt_skips_incomplete_coordinates():
    assert _geometrie_punkt({"ost": "2600000", "nord": ""}) is None
    assert _geometrie_punkt({"ost": "", "nord": "1200000"}) is None
    assert _geometrie_punkt(None) is None


def _coord_pairs(xml: str) -> list[tuple[str, str]]:
    c1 = re.findall(r"<\w+:c1>([^<]+)</\w+:c1>", xml)
    c2 = re.findall(r"<\w+:c2>([^<]+)</\w+:c2>", xml)

    return list(zip(c1, c2, strict=True))


def test_serializes_a_drawn_line():
    export = _mandatory_export(
        1,
        plot_point=None,
        gis_geometry=_drawn(
            "LINESTRING",
            [
                {"ost": "2607000.5", "nord": "1228500.5"},
                {"ost": "2607100.5", "nord": "1228600.5"},
            ],
        ),
    )

    xml = build_sogis_transfer_xml([export]).xml
    _validated(xml)

    assert "Geometrie_Linie" in xml
    assert "Geometrie_Punkt" not in xml
    assert _coord_pairs(xml) == [
        ("2607000.5", "1228500.5"),
        ("2607100.5", "1228600.5"),
    ]


def test_serializes_a_drawn_polygon_with_a_closed_ring():
    export = _mandatory_export(
        1,
        plot_point=None,
        gis_geometry=_drawn(
            "POLYGON",
            [
                {"ost": "2607000.5", "nord": "1228500.5"},
                {"ost": "2607100.5", "nord": "1228500.5"},
                {"ost": "2607100.5", "nord": "1228600.5"},
            ],
        ),
    )

    xml = build_sogis_transfer_xml([export]).xml
    _validated(xml)

    assert "Geometrie_Flaeche" in xml
    # The ring returns to its first point.
    assert _coord_pairs(xml) == [
        ("2607000.5", "1228500.5"),
        ("2607100.5", "1228500.5"),
        ("2607100.5", "1228600.5"),
        ("2607000.5", "1228500.5"),
    ]


@pytest.mark.parametrize(
    ("serialize", "too_few"),
    [(_geometrie_linie, POINTS[:1]), (_geometrie_flaeche, POINTS[:2])],
)
def test_a_geometry_needs_enough_usable_points(serialize, too_few):
    """That the dossier is then reported is `test_validate_rejects_an_unusable_geometry`."""
    unusable = [*too_few, {"ost": "2607100.5", "nord": ""}]

    assert serialize(too_few) is None
    assert serialize(unusable) is None
    assert serialize(None) is None


def test_grundstuecke_of_an_export_without_parcels_is_empty():
    assert _grundstuecke(None) == []
    assert _grundstuecke([]) == []


def test_child_type_reports_the_available_elements():
    with pytest.raises(KeyError, match="has no child element 'Nope'"):
        _child_type(so_schema.GeschaeftType, so_schema.Namespace, "Nope")


def test_build_lets_an_unhandled_shape_surface_as_a_bug():
    """An input the builders do not handle is a bug, not an invalid dossier."""
    # A gesuchsteller entry must be a mapping; a bare string is a shape no
    # annotation produces.
    with pytest.raises(AttributeError):
        build_sogis_transfer_xml([_mandatory_export(1, gesuchsteller=["Muster"])])
