from __future__ import annotations

from io import BytesIO
from typing import Any
from xml.etree import ElementTree as ET

from pyxb.namespace import ExpandedName

from camac.gis_export.models import SOGISExport
from camac.gis_export.so_schema import (
    GeometryCHLV95_V2,
    SO_DSBJD_eBauSO_Geschaefte_20250422 as so_schema,
    geometry,
)

MODEL_NAME = "SO_DSBJD_eBauSO_Geschaefte_20250422"
TOPIC_NAME = "Geschaefte"
CLASS_NAME = "Geschaeft"
BASKET_ID = f"{MODEL_NAME}.{TOPIC_NAME}"

ILI_NS = "http://www.interlis.ch/xtf/2.4/INTERLIS"
GEOM_NS = "http://www.interlis.ch/geometry/1.0"
MODEL_NS = f"http://www.interlis.ch/xtf/2.4/{MODEL_NAME}"

ET.register_namespace("ili", ILI_NS)
ET.register_namespace("geom", GEOM_NS)
ET.register_namespace(MODEL_NAME, MODEL_NS)

PERSON_ADRESSE_FIELD_MAP = {
    "gesuchssteller": "Gesuchsteller",
    "gesuchssteller_vertretung": "Gesuchsteller_Vertretung",
    "projektverfasser": "Projektverfasser",
    "rechnungsempfaenger": "Rechnungsempfaenger",
    "grundeigentuemer": "Grundeigentuemer",
}


def _ili_tag(tag: str) -> str:
    return f"{{{ILI_NS}}}{tag}"


def _model_tag(tag: str) -> str:
    return f"{{{MODEL_NS}}}{tag}"


def _xml_value(value: Any) -> str:
    if isinstance(value, bool):
        return str(value).lower()

    return str(value)


def _append_text(parent: ET.Element, tag: str, value: Any) -> None:
    if value in (None, "", [], {}):
        return

    ET.SubElement(parent, _model_tag(tag)).text = _xml_value(value)


def _schema_element(value: Any, element_name: str) -> ET.Element:
    xml = value.toxml(element_name=element_name)
    if isinstance(xml, bytes):
        xml = xml.decode()

    element = ET.fromstring(xml)
    element.tag = _model_tag(element_name)

    return element


def _schema_child_type(parent_type: type, local_name: str) -> type:
    use = parent_type._UseForTag(ExpandedName(so_schema.Namespace, local_name))
    return use.elementBinding().typeDefinition()


def _wrap(parent_type: type, field: str, inner: Any) -> Any:
    wrapper_type = _schema_child_type(parent_type, field)
    (child_id,) = [element.id() for element in wrapper_type._ElementMap.values()]

    return wrapper_type(**{child_id: inner})


def _natuerliche_person(data: dict[str, Any]) -> Any:
    return so_schema.Natuerliche_PersonType(
        Name=data.get("name"),
        Vorname=data.get("vorname"),
    )


def _juristische_person(data: dict[str, Any]) -> Any:
    return so_schema.Juristische_PersonType(Name=data.get("name"))


def _adresse(data: dict[str, Any]) -> Any:
    return so_schema.Adresse_Type(
        Strassenname=data.get("strassenname"),
        Hausnummer=data.get("hausnummer"),
        PLZ=data.get("plz"),
        Ortschaft=data.get("ortschaft"),
    )


def _has_content(value: Any) -> bool:
    if isinstance(value, dict):
        return any(_has_content(item) for item in value.values())

    if isinstance(value, list):
        return any(_has_content(item) for item in value)

    return value not in (None, "")


def _person_adresse(data: dict[str, Any] | None) -> Any | None:
    if not _has_content(data):
        return None

    person = so_schema.PersonAdresseType()

    if _has_content(data.get("natuerliche_person")):
        person.Natuerliche_Person = _wrap(
            so_schema.PersonAdresseType,
            "Natuerliche_Person",
            _natuerliche_person(data["natuerliche_person"]),
        )

    if _has_content(data.get("juristische_person")):
        person.Juristische_Person = _wrap(
            so_schema.PersonAdresseType,
            "Juristische_Person",
            _juristische_person(data["juristische_person"]),
        )

    if _has_content(data.get("adresse")):
        person.Adresse = _wrap(
            so_schema.PersonAdresseType,
            "Adresse",
            _adresse(data["adresse"]),
        )

    return person


def _geometrie_punkt(data: dict[str, Any] | None) -> Any | None:
    if not data:
        return None

    east = data.get("ost")
    north = data.get("nord")

    if east in (None, "") or north in (None, ""):
        return None

    coord = geometry.CoordType(c1=float(east), c2=float(north))

    return GeometryCHLV95_V2.MultiPoint(multicoord=geometry.MultiCoordType(coord=coord))


def _bauprojekt(data: dict[str, Any] | None) -> Any | None:
    if not _has_content(data):
        return None

    return so_schema.Bauprojekt_Type(
        Beschreibung=data.get("beschreibung"),
        Bauwerk_Art=data.get("bauwerk_art") or [],
        Nutzungszweck=data.get("nutzungszweck"),
    )


def _grundstuecke(data: list[dict[str, Any]] | None) -> list[Any]:
    if not data:
        return []

    return [
        _wrap(
            so_schema.GeschaeftType,
            "Grundstuecke",
            so_schema.GrundstueckType(
                Nummer=item.get("nummer"),
                EGRID=item.get("egrid"),
            ),
        )
        for item in data
    ]


def _build_geschaeft(export: SOGISExport, tid: str) -> Any:
    geschaeft = so_schema.GeschaeftType()

    geschaeft.tid = tid
    geschaeft.Identifikator = export.identifikator
    geschaeft.BFSNr = export.bfsnr
    geschaeft.Verfahrensart = export.verfahrensart

    geometrie_punkt = _geometrie_punkt(export.geometrie_punkt)
    if geometrie_punkt is not None:
        geschaeft.Geometrie_Punkt = geometrie_punkt

    geschaeft.Status = export.status

    for model_field, schema_field in PERSON_ADRESSE_FIELD_MAP.items():
        person = _person_adresse(getattr(export, model_field))
        if person is not None:
            setattr(
                geschaeft,
                schema_field,
                _wrap(so_schema.GeschaeftType, schema_field, person),
            )

    geschaeft.ausserhalb_Bauzone = export.ausserhalb_bauzone

    bauprojekt = _bauprojekt(export.bauprojekt)
    if bauprojekt is not None:
        geschaeft.Bauprojekt = _wrap(
            so_schema.GeschaeftType,
            "Bauprojekt",
            bauprojekt,
        )

    geschaeft.Grundstuecke.extend(_grundstuecke(export.grundstuecke))
    geschaeft.eBau_Link = export.ebau_link

    return geschaeft


def _build_basket(exports: list[SOGISExport]) -> Any:
    basket = so_schema.GeschaefteType()
    basket.bid = BASKET_ID

    for index, export in enumerate(exports, start=1):
        basket.Geschaeft.append(_build_geschaeft(export, str(export.pk or index)))

    return basket


def render_sogis_export_xml(exports: list[SOGISExport]) -> BytesIO:
    root = ET.Element(_ili_tag("transfer"))

    headersection = ET.SubElement(root, _ili_tag("headersection"))
    models = ET.SubElement(headersection, _ili_tag("models"))
    model = ET.SubElement(models, _ili_tag("model"))
    model.text = MODEL_NAME
    sender = ET.SubElement(headersection, _ili_tag("sender"))
    sender.text = "eBauSO"

    datasection = ET.SubElement(root, _ili_tag("datasection"))

    basket_xml = _build_basket(exports).toxml("utf-8", element_name=TOPIC_NAME)
    basket_element = ET.fromstring(basket_xml)
    basket_element.tag = _model_tag(TOPIC_NAME)
    datasection.append(basket_element)

    buffer = BytesIO()
    ET.ElementTree(root).write(buffer, encoding="utf-8", xml_declaration=True)
    buffer.seek(0)

    return buffer


def export_sogis_xml(exports: list[SOGISExport] | None = None) -> BytesIO | None:
    if exports is None:
        exports = list(
            SOGISExport.objects.filter(exported_at__isnull=True).order_by(
                "identifikator"
            )
        )
    else:
        exports = sorted(exports, key=lambda export: export.identifikator)

    if not exports:
        return None

    return render_sogis_export_xml(exports)
