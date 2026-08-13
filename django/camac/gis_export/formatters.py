import json
from collections.abc import Iterable
from typing import Any, NamedTuple

import pyxb
from pyxb.namespace import ExpandedName, Namespace

from camac.gis_export.models import SOGISExport
from camac.gis_export.so_schema import (
    INTERLIS,
    GeometryCHLV95_V2,
    SO_DSBJD_eBauSO_Geschaefte_20250422 as so_schema,
    geometry,
)

MODEL_NAME = "SO_DSBJD_eBauSO_Geschaefte_20250422"
TOPIC_NAME = "Geschaefte"
BASKET_ID = f"{MODEL_NAME}.{TOPIC_NAME}"
SENDER = "eBauSO"

_SO = so_schema.Namespace
_ILI = INTERLIS.Namespace

# The LV95 extent of Switzerland. The generated XSD dropped the domain from
# `GeometryCHLV95_V2.coord` so the schema would serialize invalid coordinates.
LV95_EAST = (2460000, 2870000)
LV95_NORTH = (1045000, 1310000)


def _child_type(parent_type: type, namespace: Namespace, local_name: str) -> type:
    """Resolve anonymous complexTypes into usable python classes.

    The bindings generate anonymous types for complexTypes without a name.
    Those names shift whenever the bindings are regenerated.
    The XML element names used to look them up here do not, which keeps this
    resolution stable.
    """
    try:
        # Get full qualified name in `namespace` for `local_name` which could be ambiguous
        key = ExpandedName(namespace, local_name)
        # Get the element declaration for `key` but in the scope of `parent_type`
        declaration = parent_type._UseForTag(key)
    except KeyError:
        available = sorted(name.localName() for name in parent_type._ElementMap)
        raise KeyError(
            f"{parent_type.__name__} has no child element {local_name!r}. "
            f"Available: {', '.join(available)}"
        ) from None

    # Get the element binding from the declaration and then get the correct class with `typeDefinition`
    return declaration.elementBinding().typeDefinition()


# Resolved once at import, so a renamed element fails fast and loudly here
# instead of silently building the wrong structure.
HEADERSECTION_TYPE = _child_type(INTERLIS.TransferType, _ILI, "headersection")
MODELS_TYPE = _child_type(HEADERSECTION_TYPE, _ILI, "models")
DATASECTION_TYPE = _child_type(INTERLIS.TransferType, _ILI, "datasection")

NATUERLICHE_PERSON_WRAPPER = _child_type(
    so_schema.PersonAdresseType, _SO, "Natuerliche_Person"
)
JURISTISCHE_PERSON_WRAPPER = _child_type(
    so_schema.PersonAdresseType, _SO, "Juristische_Person"
)
ADRESSE_WRAPPER = _child_type(so_schema.PersonAdresseType, _SO, "Adresse")
GRUNDSTUECKE_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Grundstuecke")
LOKALISATION_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Lokalisation")
BAUPROJEKT_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Bauprojekt")
BAUWERKE_WRAPPER = _child_type(so_schema.Bauprojekt_Type, _SO, "Bauwerke")
ENTSCHEID_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Entscheid_Leitbehoerde")
AUFLAGE_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Auflage")
ZIRKULATION_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Zirkulation")
ZUSTAENDIGE_PERSONEN_WRAPPER = _child_type(
    so_schema.GeschaeftType, _SO, "Zustaendige_Personen"
)
GESUCHSTELLER_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Gesuchsteller")
GESUCHSTELLER_ADRESSE_WRAPPER = _child_type(
    so_schema.Gesuchsteller_Type, _SO, "Adresse"
)
GESUCHSTELLER_VERTRETUNG_WRAPPER = _child_type(
    so_schema.Gesuchsteller_Type, _SO, "Vertretung"
)
PROJEKTVERFASSER_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Projektverfasser")
RECHNUNGSEMPFAENGER_WRAPPER = _child_type(
    so_schema.GeschaeftType, _SO, "Rechnungsempfaenger"
)
GRUNDEIGENTUEMER_WRAPPER = _child_type(so_schema.GeschaeftType, _SO, "Grundeigentuemer")

# This needs to be updated if the Enums in the ILI change
STATUS_BY_STATE = {
    "subm": "Pruefung.formell",
    "material-exam": "Pruefung.materiell",
    "correction": "in_Korrektur",
    "reject": "zur_Rueckweisung",
    "rejected": "zurueckgewiesen",
    "withdrawal": "zum_Rueckzug",
    "withdrawn": "zurueckgezogen",
    "init-distribution": "Zirkulation_initialisieren",
    "distribution": "in_Zirkulation",
    "decision": "Entscheid",
    "decided": "entschieden",
    "construction-monitoring": "Baubegleitung",
    "finished": "abgeschlossen",
}
STATUS_VALUES = frozenset(STATUS_BY_STATE.values())


def _map_status(name: str | None) -> str | None:
    """Map an instance state onto its Status_Geschaeft enum.

    An unknown state (or a value already in enum form) is returned unchanged
    so _validate reports it per dossier instead of silently dropping it.
    """
    return STATUS_BY_STATE.get(name, name)


ENTSCHEID_BY_SLUG = {
    "entscheid-entscheid-ablehnung": "Ablehnung",
    "entscheid-entscheid-zustimmung": "Zustimmung",
    "entscheid-entscheid-teilzustimmung": "Teilzustimmung",
    "entscheid-entscheid-rueckzug": "Rueckzug",
    "entscheid-entscheid-positiv": "positiv",
    "entscheid-entscheid-negativ": "negativ",
}
ENTSCHEID_VALUES = frozenset(ENTSCHEID_BY_SLUG.values())


def _map_entscheid(data: str | None) -> str | None:
    """Map a decision slug onto its Entscheid enum, unchanged on a miss.

    An unmapped slug is returned as-is so _validate reports it per dossier.
    """
    return ENTSCHEID_BY_SLUG.get(data, data)


FACHSTELLE_BY_SLUG = {
    "afu": "AFU",
    "arp": "ARP",
    "arp-bab": "ARP",
    "arp-fuss-und-wanderwege": "ARP",
    "arp-heimatschutz": "ARP",
    "arp-leitbehoerde": "ARP",
    "arp-naturschutz": "ARP",
    "arp-nutzungsplanung": "ARP",
    "amb-zivilschutz-bauwesen": "AMB",
    "awa-arbeitsinspektorat": "AWA",
    "awa-energiefachstelle": "AWA",
    "awjf": "AWJF",
    "denkmalpflege": "ADA",
    "gesundheitsamt": "GESA",
    "sgv": "SGV",
    "alw": "ALW",
    "avt": "AVT",
}
FACHSTELLEN_VALUES = frozenset(
    {"Gemeinde", "ausserkantonale_Fachstelle", *FACHSTELLE_BY_SLUG.values()}
)


def _map_fachstelle(data: dict[str, Any]) -> str | None:
    """Map a service onto its Fachstellen enum, or None when it has no mapping.

    A service is matched by its own slug or, for sub-services that carry no
    slug of their own, by its parent's slug. An unmapped service is reported
    per dossier by `_validate` rather than silently defaulting.
    """
    if data.get("group_slug") == "municipality":
        return "Gemeinde"
    if data.get("group_slug") == "service-extra-cantonal":
        return "ausserkantonale_Fachstelle"

    return FACHSTELLE_BY_SLUG.get(data.get("slug")) or FACHSTELLE_BY_SLUG.get(
        data.get("parent_slug")
    )


class ExportValidationError(ValueError):
    """An export violates a model rule the generated XSD cannot express."""


class SOGISTransfer(NamedTuple):
    """The serialized transfer plus which exports it contains and which failed."""

    xml: str
    exported: list[SOGISExport]
    errors: list[ExportValidationError]


def _natuerliche_person(data: dict[str, Any]) -> so_schema.Natuerliche_PersonType:
    return so_schema.Natuerliche_PersonType(
        Name=data.get("name"),
        Vorname=data.get("vorname"),
    )


def _juristische_person(data: dict[str, Any]) -> so_schema.Juristische_PersonType:
    return so_schema.Juristische_PersonType(Name=data.get("name"))


def _adresse(data: dict[str, Any]) -> so_schema.Adresse_Type:
    return so_schema.Adresse_Type(
        Strassenname=data.get("strassenname"),
        Hausnummer=data.get("hausnummer"),
        PLZ=data.get("plz"),
        Ortschaft=data.get("ortschaft"),
    )


def _person(data: dict[str, Any] | None) -> so_schema.PersonAdresseType | None:
    if not data:
        return None

    person = so_schema.PersonAdresseType()

    if data.get("natuerliche_person"):
        person.Natuerliche_Person = NATUERLICHE_PERSON_WRAPPER(
            Natuerliche_Person=_natuerliche_person(data["natuerliche_person"])
        )

    if data.get("juristische_person"):
        person.Juristische_Person = JURISTISCHE_PERSON_WRAPPER(
            Juristische_Person=_juristische_person(data["juristische_person"])
        )

    if data.get("adresse"):
        person.Adresse = ADRESSE_WRAPPER(Adresse=_adresse(data["adresse"]))

    return person


def _person_adresse(wrapper: type, data: dict[str, Any] | None) -> Any | None:
    person = _person(data)
    if person is None:
        return None

    return wrapper(PersonAdresse=person)


def _gesuchsteller(
    adresse: dict[str, Any] | None, vertretung: dict[str, Any] | None
) -> Any | None:
    applicant = _person(adresse)
    if applicant is None:
        return None

    gesuchsteller = so_schema.Gesuchsteller_Type(
        Adresse=GESUCHSTELLER_ADRESSE_WRAPPER(PersonAdresse=applicant)
    )

    representation = _person(vertretung)
    if representation is not None:
        gesuchsteller.Vertretung = GESUCHSTELLER_VERTRETUNG_WRAPPER(
            PersonAdresse=representation
        )

    return GESUCHSTELLER_WRAPPER(Gesuchsteller=gesuchsteller)


def _coordinates(data: dict[str, Any] | None) -> tuple[float, float] | None:
    """Return the point as floats, or None when it cannot be used.

    The coordinates come from float questions, but nothing guarantees the
    stored JSON holds numbers, so a value that will not convert has to be
    reported per dossier rather than blow up mid-batch.
    """
    if not data:
        return None

    try:
        east, north = float(data["ost"]), float(data["nord"])
    except (KeyError, TypeError, ValueError):
        return None

    if not (
        LV95_EAST[0] <= east <= LV95_EAST[1] and LV95_NORTH[0] <= north <= LV95_NORTH[1]
    ):
        return None

    return east, north


def _drawn_geometry(
    export: SOGISExport,
) -> tuple[str | None, list[dict[str, Any]]] | None:
    """Return the geometry to export as `(type, points)`.

    This will be 1:1 the json from the `gis-karte` answer unless the dossier
    predates the multi point change. There, we return the annotated point
    from the first entry of `parzellen` table.

    Only a missing answer falls back that way. An answer that cannot be read is
    a data problem for this dossier, so it yields nothing and gets reported
    rather than exporting a point the user never drew.
    """
    if export.gis_geometry:
        try:
            drawn = json.loads(export.gis_geometry)
        except json.JSONDecodeError:
            return None

        markers = drawn.get("markers") if isinstance(drawn, dict) else None

        if not isinstance(markers, list) or not all(
            isinstance(marker, dict) for marker in markers
        ):
            return None

        return drawn.get("geometry"), [
            {"ost": marker.get("x"), "nord": marker.get("y")} for marker in markers
        ]

    if export.plot_point:
        return "POINT", [export.plot_point]

    return None


def _geometrie_punkt(
    data: dict[str, Any] | None,
) -> GeometryCHLV95_V2.MultiPoint | None:
    coordinates = _coordinates(data)
    if coordinates is None:
        return None

    east, north = coordinates
    coord = geometry.CoordType(c1=east, c2=north)

    return GeometryCHLV95_V2.MultiPoint(multicoord=geometry.MultiCoordType(coord=coord))


def _coord_pairs(
    data: list[dict[str, Any]] | None,
) -> list[tuple[float, float]] | None:
    """Return the points as float pairs, or None when any is unusable.

    One unusable point would silently reshape the line or polygon, so the
    whole geometry is dropped and reported rather than exported malformed.
    """
    if not data:
        return None

    pairs = []
    for point in data:
        coordinates = _coordinates(point)
        if coordinates is None:
            return None
        pairs.append(coordinates)

    return pairs


def _polyline(pairs: list[tuple[float, float]]) -> geometry.PolylineType:
    return geometry.PolylineType(
        coord=[geometry.CoordType(c1=east, c2=north) for east, north in pairs]
    )


def _geometrie_linie(
    data: list[dict[str, Any]] | None,
) -> GeometryCHLV95_V2.MultiLine | None:
    pairs = _coord_pairs(data)
    if pairs is None or len(pairs) < 2:
        return None

    return GeometryCHLV95_V2.MultiLine(
        multipolyline=geometry.MultiPolylineType(polyline=_polyline(pairs))
    )


def _geometrie_flaeche(
    data: list[dict[str, Any]] | None,
) -> GeometryCHLV95_V2.MultiSurface | None:
    pairs = _coord_pairs(data)
    if pairs is None or len(pairs) < 3:
        return None

    # An INTERLIS surface boundary is a closed ring, so the last coordinate has
    # to return to the first.
    ring = pairs if pairs[0] == pairs[-1] else [*pairs, pairs[0]]

    return GeometryCHLV95_V2.MultiSurface(
        multisurface=geometry.MultiSurfaceType(
            surface=geometry.SurfaceType(
                exterior=[geometry.BoundaryType(polyline=_polyline(ring))]
            )
        )
    )


def _grundstuecke(data: list[dict[str, Any]] | None) -> list[Any]:
    if not data:
        return []

    return [
        GRUNDSTUECKE_WRAPPER(
            Grundstueck=so_schema.GrundstueckType(
                Nummer=item.get("nummer"),
                EGRID=item.get("egrid"),
            )
        )
        for item in data
    ]


def _lokalisation(data: dict[str, Any] | None) -> Any | None:
    if not data:
        return None

    return LOKALISATION_WRAPPER(Adresse=_adresse(data))


def _bauwerk(data: dict[str, Any]) -> so_schema.BauwerkType:
    return so_schema.BauwerkType(
        Bezeichnung=data.get("bezeichnung"),
        Bauwerk_Typ=data.get("bauwerk_typ"),
        EGID=data.get("egid"),
        Arbeiten_Art=data.get("arbeiten_art") or [],
        Gebaeudekategorie=data.get("gebaeudekategorie"),
    )


def _bauprojekt(data: dict[str, Any] | None) -> Any | None:
    if not data:
        return None

    bauprojekt = so_schema.Bauprojekt_Type(
        Beschreibung=data.get("beschreibung"),
        Bauwerk_Art=data.get("bauwerk_art") or [],
        Nutzungszweck=data.get("nutzungszweck") or [],
    )
    bauprojekt.Bauwerke = [
        BAUWERKE_WRAPPER(Bauwerk=_bauwerk(item)) for item in data.get("bauwerke") or []
    ]

    return BAUPROJEKT_WRAPPER(Bauprojekt=bauprojekt)


def _entscheid(data: dict[str, Any] | None) -> Any | None:
    if not data:
        return None

    entscheid = _map_entscheid(data.get("entscheid"))

    return ENTSCHEID_WRAPPER(
        Entscheid=so_schema.Entscheid_Type(
            Entscheid=entscheid,
            Datum=data.get("datum"),
        )
    )


def _auflage(data: dict[str, Any] | None) -> Any | None:
    if not data:
        return None

    return AUFLAGE_WRAPPER(
        Auflage=so_schema.Auflage_Type(
            Startdatum=data.get("startdatum"),
            Enddatum=data.get("enddatum"),
        )
    )


def _zustaendigkeit(data: dict[str, Any]) -> so_schema.ZustaendigkeitType:
    return so_schema.ZustaendigkeitType(
        Fachstelle=_map_fachstelle(data),
        Name=data.get("name"),
        Abteilung=data.get("abteilung"),
    )


def _zirkulation(data: list[dict[str, Any]] | None) -> list[Any]:
    if not data:
        return []

    return [ZIRKULATION_WRAPPER(Zustaendigkeit=_zustaendigkeit(item)) for item in data]


def _zustaendige_personen(data: dict[str, Any] | None) -> Any | None:
    if not data:
        return None

    return ZUSTAENDIGE_PERSONEN_WRAPPER(Zustaendigkeit=_zustaendigkeit(data))


def _geometrie(export: SOGISExport) -> tuple[str, Any]:
    """Return the INTERLIS field and value for the dossier's geometry.

    Exactly one of the three can apply. Raises rather than returning nothing, so
    callers past `_validate` do not have to re-check what it already rejected.
    """
    match _drawn_geometry(export):
        case "POINT", [point, *_]:
            field, value = "Geometrie_Punkt", _geometrie_punkt(point)
        case "LINESTRING", points:
            field, value = "Geometrie_Linie", _geometrie_linie(points)
        case "POLYGON", points:
            field, value = "Geometrie_Flaeche", _geometrie_flaeche(points)
        case _:
            field, value = None, None

    if field is None or value is None:
        raise ExportValidationError(
            f"no usable geometry in {export.gis_geometry!r} / "
            f"{export.plot_point!r}, violating MANDATORY CONSTRAINT "
            "DEFINED(Geometrie_Punkt) OR DEFINED(Geometrie_Linie) "
            "OR DEFINED(Geometrie_Flaeche)"
        )

    return field, value


def _validate(export: SOGISExport) -> None:
    """Check the .ili rules the generated XSD cannot express.

    Covers the explicit ``MANDATORY CONSTRAINT`` and the three enumerations,
    which the XSD generator emitted as unconstrained strings.
    """
    errors = []

    try:
        _geometrie(export)
    except ExportValidationError as e:
        errors.append(str(e))

    if _map_status(export.status) not in STATUS_VALUES:
        errors.append(f"Status {export.status!r} is not a Status_Geschaeft value")

    entscheid = (export.entscheid or {}).get("entscheid")
    if entscheid is not None and _map_entscheid(entscheid) not in ENTSCHEID_VALUES:
        errors.append(f"Entscheid {entscheid!r} is not an Entscheid value")

    zustaendigkeiten = list(export.zirkulation or [])
    if export.zustaendige_person:
        zustaendigkeiten.append(export.zustaendige_person)

    errors.extend(
        f"service {item.get('slug')!r} is not a Fachstellen value"
        for item in zustaendigkeiten
        if _map_fachstelle(item) is None
    )

    if errors:
        raise ExportValidationError(
            f"Export {export.identifikator!r}: " + "; ".join(errors)
        )


def _build_geschaeft(export: SOGISExport, tid: str) -> so_schema.GeschaeftType:
    _validate(export)

    geschaeft = so_schema.Geschaeft(tid=tid)

    geschaeft.Identifikator = export.identifikator
    geschaeft.BFSNr = export.bfsnr
    geschaeft.Verfahrensart = export.verfahrensart
    geschaeft.Status = _map_status(export.status)
    geschaeft.eBau_Link = export.ebau_link
    geschaeft.ausserhalb_Bauzone = export.ausserhalb_bauzone

    for schema_field, value in (
        _geometrie(export),
        (
            "Gesuchsteller",
            _gesuchsteller(export.gesuchsteller, export.gesuchsteller_vertretung),
        ),
        (
            "Projektverfasser",
            _person_adresse(PROJEKTVERFASSER_WRAPPER, export.projektverfasser),
        ),
        (
            "Rechnungsempfaenger",
            _person_adresse(RECHNUNGSEMPFAENGER_WRAPPER, export.rechnungsempfaenger),
        ),
        (
            "Grundeigentuemer",
            _person_adresse(GRUNDEIGENTUEMER_WRAPPER, export.grundeigentuemer),
        ),
        ("Lokalisation", _lokalisation(export.lokalisation)),
        ("Bauprojekt", _bauprojekt(export.bauprojekt)),
        ("Entscheid_Leitbehoerde", _entscheid(export.entscheid)),
        ("Auflage", _auflage(export.auflage)),
        ("Zustaendige_Personen", _zustaendige_personen(export.zustaendige_person)),
    ):
        if value is not None:
            setattr(geschaeft, schema_field, value)

    geschaeft.Zirkulation = _zirkulation(export.zirkulation)
    geschaeft.Grundstuecke = _grundstuecke(export.grundstuecke)

    return geschaeft


# The bindings name inline types `STD_ANON*`/`CTD_ANON*`, which says nothing
# in an error message. Every one of them belongs to exactly one element, so the
# element it was declared for is the readable name.
ANONYMOUS_TYPE_NAMES = {
    declaration.elementBinding().typeDefinition(): (
        f"{owner.__name__}.{name.localName()}"
    )
    for owner in vars(so_schema).values()
    for name, declaration in (getattr(owner, "_ElementMap", None) or {}).items()
}


def _reason(error: pyxb.PyXBException) -> str:
    """Explain a schema violation without leaking generated type names."""
    field = ANONYMOUS_TYPE_NAMES.get(getattr(error, "type", None))
    if not field:
        # A content model failure already names the element it stopped at.
        return error.details() if hasattr(error, "details") else repr(error)

    return f"{field} does not accept {error.value!r}"


def build_sogis_transfer_xml(exports: Iterable[SOGISExport]) -> SOGISTransfer:
    """Serialize the exports into a schema-validated INTERLIS transfer document.

    Each Geschaeft is built and validated once. A dossier that fails will be
    returned as an error rather than raised, so one error won't stop the whole
    batch. Anything reported keeps its `exported_at` unset and is
    re-exported on the next run.

    Returns the XML, the exports it actually contains (to mark as delivered) and
    the errors.
    """
    basket = so_schema.Geschaefte(bid=BASKET_ID)
    exported = []
    errors = []

    for export in exports:
        try:
            geschaeft = _build_geschaeft(export, str(export.pk))
            geschaeft.validateBinding()
        except ExportValidationError as error:
            errors.append(error)
        except pyxb.PyXBException as error:
            # Only failures classified against a contract are collected: an
            # unexpected exception means the builders met input they do not
            # handle, which is a bug and has to surface as one.
            errors.append(
                ExportValidationError(
                    f"Export {export.identifikator!r}: {_reason(error)}"
                )
            )
        else:
            basket.Geschaeft.append(geschaeft)
            exported.append(export)

    datasection = DATASECTION_TYPE()
    datasection.append(basket)

    transfer = INTERLIS.transfer(
        headersection=HEADERSECTION_TYPE(
            models=MODELS_TYPE(model=[MODEL_NAME]),
            sender=SENDER,
        ),
        datasection=datasection,
    )

    return SOGISTransfer(
        xml=transfer.toxml("utf-8").decode("utf-8"),
        exported=exported,
        errors=errors,
    )
