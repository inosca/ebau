from xml.etree import ElementTree as ET

import pytest

from camac.gis_export.models import SOGISExport
from camac.gis_export.serializers import (
    _append_text,
    _geometrie_punkt,
    _schema_element,
    render_sogis_export_xml,
)


@pytest.mark.django_db
def test_render_sogis_export_xml(so_instance):
    export = SOGISExport.objects.create(
        instance=so_instance,
        hash="test-hash",
        identifikator="SO-2026-1",
        bfsnr=2601,
        verfahrensart="Baugesuch",
        status="Pruefung.formell",
        ausserhalb_bauzone=True,
        gesuchssteller={
            "natuerliche_person": {"name": "Muster", "vorname": "Ayla"},
            "adresse": {
                "strassenname": "Teststrasse",
                "hausnummer": None,
                "plz": 4500,
                "ortschaft": "Solothurn",
            },
        },
        geometrie_punkt={"ost": 2690970.9, "nord": 1192891.9},
        grundstuecke=[
            {"nummer": "123456", "egrid": "CH123456"},
            {"nummer": "789012", "egrid": "CH789012"},
        ],
        ebau_link="https://ebau.example/cases/1",
    )

    content = render_sogis_export_xml([export]).getvalue().decode()

    assert "<ili:transfer" in content
    assert "<ili:datasection>" in content
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Identifikator>SO-2026-1</SO_DSBJD_eBauSO_Geschaefte_20250422:Identifikator>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:BFSNr>2601</SO_DSBJD_eBauSO_Geschaefte_20250422:BFSNr>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Status>Pruefung.formell</SO_DSBJD_eBauSO_Geschaefte_20250422:Status>"
        in content
    )
    assert "<SO_DSBJD_eBauSO_Geschaefte_20250422:Gesuchsteller>" in content
    assert "<SO_DSBJD_eBauSO_Geschaefte_20250422:Natuerliche_Person>" in content
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Name>Muster</SO_DSBJD_eBauSO_Geschaefte_20250422:Name>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Vorname>Ayla</SO_DSBJD_eBauSO_Geschaefte_20250422:Vorname>"
        in content
    )
    assert "<SO_DSBJD_eBauSO_Geschaefte_20250422:Adresse>" in content
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:PLZ>4500</SO_DSBJD_eBauSO_Geschaefte_20250422:PLZ>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Ortschaft>Solothurn</SO_DSBJD_eBauSO_Geschaefte_20250422:Ortschaft>"
        in content
    )
    assert "<SO_DSBJD_eBauSO_Geschaefte_20250422:Geometrie_Punkt>" in content
    assert "<geom:c1>2690970.9</geom:c1>" in content
    assert "<geom:c2>1192891.9</geom:c2>" in content
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:ausserhalb_Bauzone>true</SO_DSBJD_eBauSO_Geschaefte_20250422:ausserhalb_Bauzone>"
        in content
    )
    assert "<SO_DSBJD_eBauSO_Geschaefte_20250422:Grundstuecke>" in content
    assert "<SO_DSBJD_eBauSO_Geschaefte_20250422:Grundstueck>" in content
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:Nummer>123456</SO_DSBJD_eBauSO_Geschaefte_20250422:Nummer>"
        in content
    )
    assert (
        "<SO_DSBJD_eBauSO_Geschaefte_20250422:EGRID>CH123456</SO_DSBJD_eBauSO_Geschaefte_20250422:EGRID>"
        in content
    )


@pytest.mark.django_db
def test_render_sogis_export_xml_is_well_formed(so_instance):
    export = SOGISExport.objects.create(
        instance=so_instance,
        hash="test-hash",
        identifikator="SO-2026-2",
        bfsnr=2601,
        verfahrensart="Baugesuch",
        status="Pruefung.formell",
        ausserhalb_bauzone=False,
        gesuchssteller={
            "natuerliche_person": {"name": "Muster", "vorname": "Ayla"},
            "adresse": {
                "strassenname": "Teststrasse",
                "hausnummer": None,
                "plz": 4500,
                "ortschaft": "Solothurn",
            },
        },
        geometrie_punkt={"ost": 2690970.9, "nord": 1192891.9},
        grundstuecke=[{"nummer": "123456", "egrid": "CH123456"}],
        ebau_link="https://ebau.example/cases/2",
    )

    content = render_sogis_export_xml([export]).getvalue()

    root = ET.fromstring(content)

    assert root.tag == "{http://www.interlis.ch/xtf/2.4/INTERLIS}transfer"


def test_geometrie_punkt_skips_incomplete_coordinates():
    assert _geometrie_punkt({"ost": "2600000", "nord": ""}) is None
    assert _geometrie_punkt({"ost": "", "nord": "1200000"}) is None
    assert _geometrie_punkt(None) is None


@pytest.mark.django_db
def test_export_sogis_xml_returns_none_without_exports():
    from camac.gis_export.models import SOGISExport
    from camac.gis_export.serializers import export_sogis_xml

    SOGISExport.objects.all().delete()

    assert export_sogis_xml() is None


def test_append_text_skips_empty_values():
    parent = ET.Element("parent")

    _append_text(parent, "empty", None)
    _append_text(parent, "empty", "")
    _append_text(parent, "empty", [])
    _append_text(parent, "empty", {})

    assert len(parent) == 0


def test_schema_element_decodes_bytes_xml():
    class BytesXML:
        def toxml(self, element_name):
            return b"<PersonAdresse><Name>Muster</Name></PersonAdresse>"

    element = _schema_element(BytesXML(), "PersonAdresse")

    assert element.tag.endswith("PersonAdresse")
    assert element.find("Name").text == "Muster"
