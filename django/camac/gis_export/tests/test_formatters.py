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
        "geometrie_punkt": {"ost": 2607000.5, "nord": 1228500.5},
        "gesuchsteller": {
            "natuerliche_person": {"name": "Muster", "vorname": "Reto"},
            "adresse": {"plz": "4500", "ortschaft": "Solothurn"},
        },
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
        gesuchsteller_vertretung=_person_adresse("Vertretung", "Vera"),
        projektverfasser=_person_adresse("Verfasser", "Peter"),
        rechnungsempfaenger=_person_adresse("Empfaenger", "Rita"),
        grundeigentuemer=_person_adresse("Eigentuemer", "Greta"),
        bauprojekt={
            "beschreibung": "Neubau Mehrfamilienhaus mit Tiefgarage",
            "bauwerk_art": ["Hochbaute", "Tiefbaute"],
            "nutzungszweck": "Wohnen, Arbeiten (Gewerbebetrieb)",
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
        publikation={"startdatum": "2026-05-01", "enddatum": "2026-05-31"},
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

    # Fields never implemented are asserted here as missing.
    assert _unserialized(xml) == {"Geometrie_Linie", "Geometrie_Flaeche"}


def _build(**overrides) -> None:
    _validate(_mandatory_export(1, **overrides))


def test_validate_requires_at_least_one_geometry():
    with pytest.raises(ExportValidationError, match="no geometry set"):
        _build(geometrie_punkt=None)


@pytest.mark.parametrize("field", ["geometrie_linie", "geometrie_flaeche"])
def test_validate_accepts_a_geometry_other_than_punkt(field):
    # Neither is serialized yet, but either satisfies the MANDATORY CONSTRAINT.
    _build(geometrie_punkt=None, **{field: {"any": "value"}})


@pytest.mark.parametrize(
    "geometrie_punkt",
    [
        {"ost": 2607000.5, "nord": ""},
        {"ost": "", "nord": 1228500.5},
        {"ost": 2607000.5},
        {"ost": 2607000.5, "nord": None},
        # A text answer where a number is expected is a data problem, not a
        # bug, so it has to be reported like any other invalid dossier.
        {"ost": "abc", "nord": "def"},
        {"ost": 2607000.5, "nord": "1'228'500"},
    ],
)
def test_validate_rejects_an_unusable_punkt(geometrie_punkt):
    with pytest.raises(ExportValidationError, match="has no usable coordinates"):
        _build(geometrie_punkt=geometrie_punkt)


def test_validate_rejects_a_half_set_punkt_even_with_another_geometry():
    # The point would otherwise vanish from the export unnoticed.
    with pytest.raises(ExportValidationError, match="has no usable coordinates"):
        _build(
            geometrie_punkt={"ost": 2607000.5, "nord": ""},
            geometrie_linie={"any": "value"},
        )


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
        # Form decisions without an INTERLIS counterpart.
        "negativ",
        "positiv",
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
            geometrie_punkt=None,
            status="not-a-status",
            entscheid={"entscheid": "positiv"},
            zirkulation=[{"slug": "not-a-service"}],
            zustaendige_person={"slug": "also-not-a-service"},
        )

    message = str(exc_info.value)

    assert message.startswith("Export '2601-2026-1': ")
    assert message.count(";") == 4
    for expected in (
        "no geometry set",
        "Status 'not-a-status'",
        "Entscheid 'positiv'",
        "service 'not-a-service'",
        "service 'also-not-a-service'",
    ):
        assert expected in message


def test_geometrie_punkt_skips_incomplete_coordinates():
    assert _geometrie_punkt({"ost": "2600000", "nord": ""}) is None
    assert _geometrie_punkt({"ost": "", "nord": "1200000"}) is None
    assert _geometrie_punkt(None) is None


def test_grundstuecke_of_an_export_without_parcels_is_empty():
    assert _grundstuecke(None) == []
    assert _grundstuecke([]) == []


def test_child_type_reports_the_available_elements():
    with pytest.raises(KeyError, match="has no child element 'Nope'"):
        _child_type(so_schema.GeschaeftType, so_schema.Namespace, "Nope")


def test_build_lets_an_unhandled_shape_surface_as_a_bug():
    """An input the builders do not handle is a bug, not an invalid dossier."""
    # `gesuchsteller` as a list is a shape no annotation should produce.
    with pytest.raises(AttributeError):
        build_sogis_transfer_xml([_mandatory_export(1, gesuchsteller=["Muster"])])
