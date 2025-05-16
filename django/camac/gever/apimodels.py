from __future__ import annotations

import datetime
import importlib
import typing
import uuid
from dataclasses import dataclass, field
from enum import Enum
from typing import Generic, Optional, TypeVar

from dataclasses_json import CatchAll, Undefined, config, dataclass_json
from marshmallow import fields

if typing.TYPE_CHECKING:  # pragma: no cover
    from camac.gever.client import GEVERClient

"""
Data models for dealing with the CMI REST API.

These are the data models that we use to represent data on the API.
The GEVERClient method return these models, or lists thereof.

Note: The naming of attributes and classes strictly matches the API,
to avoid any unneccessary intermediate translations. The one exception is the
"reference", which in that form doesn't exist in their API.
"""

# Note: This looks a bit more complex, because we're configuring
# dataclasses_json such that it correctly deals with incomplete data, such
# as missing date fields and so on. Because dataclass_json uses Marshmallow
# behind the scenes, some of that abstraction is leaking into here.

# TODO: Many of these fields are marked "optional", because they're configurable
# in CMI API admin. However they should actually all be there. Sadly, the Admin
# kinda loses the config sometimes, and breaks everything.
# We need to figure out why/when it breaks, and also probably just YEET if
# something fails, instead of trying to accomodate this as "optional" (dvo)


ModelType = TypeVar("ModelType", bound="BaseCMIObject")


def guid_field():
    """Build a GUID (or rather UUID) field that works with Marshmallow."""

    def encode_uuid(val):
        return None if val is None else str(val)

    return field(
        metadata=config(
            decoder=uuid.UUID,
            encoder=encode_uuid,
            mm_field=fields.UUID(),
        )
    )


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class BaseCMIObject:
    guid: uuid.UUID = guid_field()

    # other_attributes will get all the attrs from the API that aren't
    # explicitly mapped (yet)
    other_attributes: CatchAll = field(metadata=config(mm_field=fields.Dict()))

    def ref(self) -> Reference[ModelType]:
        """Return a reference to this current object."""
        return Reference.make_ref(self)


def optional_date_field():
    """Configure an optional Date field.

    Configure Marshmallow to correctly decode and encode the field, and also
    deal with missing data when parsing.
    """
    date_config = config(
        encoder=lambda d: d.strftime("%d.%m.%Y") if d else None,
        mm_field=fields.Date("%d.%m.%Y", required=False, load_default=None),
    )
    return field(
        metadata=date_config,
        default=None,
    )


def optional_field(type_):
    if isinstance(type_, str):  # pragma: no cover
        # regarding the coverage: This was used previously, but is not
        # actually used right now - might be needed again later
        mod, name = type_.rsplit(".", 1)
        type_ = getattr(importlib.import_module(mod), name)
        pass
    return field(
        metadata=config(mm_field=type_(required=False, allow_none=True)),
        default=None,
    )


def enum_field(enum_type, required=True, **kwargs):
    def _decode(val):
        # Deal with some specialities of the CMI API: Enum values might
        # be received with spaces, but for consistency, we'll need them
        # to be CamelCase instead
        val = val.replace(" ", "")
        return enum_type(val)

    def _encode(val):
        if isinstance(val, str):
            # Should not happen - our internal representation should be
            # enum instances
            return val
        elif val:
            return val.value
        # else: no valid value
        return None  # pragma: no cover (we could also just drop the line)

    return field(
        metadata=config(
            mm_field=fields.Str(required=required, allow_none=(not required)),
            decoder=_decode,
            encoder=_encode,
        ),
        **kwargs,
    )


class LifecycleStatus(Enum):
    IN_BEARBEITUNG = "InBearbeitung"
    ABGESCHLOSSEN = "Abgeschlossen"
    PASSIV = "Passiv"
    ANGEBOTEN = "Angeboten"
    ZUR_KASSATION_VORGESEHEN = "ZurKassationVorgesehen"
    SAMPLING = "Sampling"
    ABGELIEFERT = "Abgeliefert"
    KASSIERT = "Kassiert"
    ZUR_AUFBEWAHRUNG_VORGESEHEN = "ZurAufbewahrungVorgesehen"
    AUFBEWAHRT = "Aufbewahrt"
    ZUR_KASSATION_FREIGEGEBEN = "ZurKassationFreigegeben"
    ARCHIVIERT = "Archiviert"
    KASSIERT_AUFBEWAHRT = "KassiertAufbewahrt"


class GeschaeftsStatus(Enum):
    IN_BEARBEITUNG = "InBearbeitung"
    STORNIERT = "Storniert"
    ZUSAMMENGEFUEHRT = "Zusammengefuehrt"
    ABGESCHLOSSEN = "Abgeschlossen"


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class CustomRegistraturplan(BaseCMIObject):
    version: int = field(metadata=config(mm_field=fields.Integer()))
    aktenzeichen: str = field(metadata=config(mm_field=fields.Str()))
    begriff: str = field(metadata=config(mm_field=fields.Str()))
    inaktiv: Optional[bool] = optional_field(fields.Bool)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Benutzer(BaseCMIObject):
    benutzerID: str = field(metadata=config(mm_field=fields.Str()))
    email: Optional[str] = optional_field(fields.Str)
    vorname: Optional[str] = optional_field(fields.Str)
    name: Optional[str] = optional_field(fields.Str)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Gemeinde(BaseCMIObject):
    bezeichnung: Optional[str] = optional_field(fields.Str)
    name: Optional[str] = optional_field(fields.Str)
    strasse: Optional[str] = optional_field(fields.Str)
    plz: Optional[int] = optional_field(fields.Int)
    inaktiv: bool = field(default=False)
    bfsNummer: Optional[int] = optional_field(fields.Int)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class CustomHerkunft(BaseCMIObject):
    bezeichnung: Optional[str] = optional_field(fields.Str)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class CustomVerfahrensstand(BaseCMIObject):
    bezeichnung: str = field(metadata=config(mm_field=fields.Str()))
    inaktiv: bool = field(default=False)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class CustomErledigungsart(BaseCMIObject):
    bezeichnung: str = field(metadata=config(mm_field=fields.Str()))
    inaktiv: bool = field(default=False)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Geschaeft(BaseCMIObject):
    typeName: str = field(metadata=config(mm_field=fields.Str()))
    version: int = field(metadata=config(mm_field=fields.Integer()))
    customArchiviert: Optional[bool] = optional_field(fields.Bool)
    bemerkung: Optional[str] = optional_field(fields.Str)
    customGrundbucheintrag: Optional[bool] = optional_field(fields.Bool)
    customOrdnungsgemaess: Optional[bool] = optional_field(fields.Bool)

    customVerfahrensstand: Optional[Reference[CustomVerfahrensstand]] = field(
        default=None
    )

    customSachbearbeiter: Optional[Reference[Benutzer]] = field(default=None)
    customGeschaeftsverantwortung: Optional[Reference[Benutzer]] = field(default=None)
    customGemeinde: Optional[Reference[Gemeinde]] = field(default=None)
    customErledigungsart: Optional[Reference[CustomErledigungsart]] = field(
        default=None
    )
    customKoordinatenX: Optional[float] = field(default=None)
    customKoordinatenY: Optional[float] = field(default=None)

    customHerkunftsNummer: Optional[str] = optional_field(fields.Str)

    # parentkey is what we use for a back-reference. For Geschaeft, it's a
    # comma-separated list of instance ids, prefixed with "ebaube". Example:
    # "ebaube:1234,9992"
    parentkey: Optional[str] = optional_field(fields.Str)

    # registraturplan = "Ordnungssystem". Required, but filled by template (normally)
    customRegistraturplan: Optional[Reference[CustomRegistraturplan]] = field(
        default=None
    )
    customVerfahrenseingang: Optional[datetime.date] = optional_date_field()
    customVerfahrensende: Optional[datetime.date] = optional_date_field()
    customPoststempel: Optional[datetime.date] = optional_date_field()
    customWiedereingang: Optional[datetime.date] = optional_date_field()
    beginn: Optional[datetime.date] = optional_date_field()
    titel: Optional[str] = optional_field(fields.Str)
    laufnummer: Optional[str] = optional_field(fields.Str)
    lifecycleStatus: LifecycleStatus = enum_field(LifecycleStatus)
    geschaeftsstatus: GeschaeftsStatus = enum_field(GeschaeftsStatus)

    geschaeftseigner: Optional[Reference[Organisationseinheit]] = field(default=None)
    customFederfuehrendesAmt: Optional[Reference[CustomAmt]] = field(default=None)
    customHerkunft: Optional[Reference[CustomHerkunft]] = field(default=None)

    dokumenteExplorer: Optional[list[Reference[Ordner]]] = field(default_factory=list)

    def get_linked_instance_ids(self) -> list[int]:
        """Return a list of instance IDs that this Geschaeft is linked to.

        A Geschaeft is linked to one eBau-NR, but an eBau-NR can contain
        multiple dossiers (instance ids). We therefore should link all instance
        IDs to a Geschaeft so we're able to correctly match them later on
        """
        if not self.parentkey:
            return []  # pragma: no cover
        assert self.parentkey.startswith("ebaube:")
        key, instance_ids_str = self.parentkey.split(":")
        return [int(x) for x in instance_ids_str.split(",")]

    def set_linked_instance_ids(self, new_instance_ids: list[int]) -> None:
        """Set a list of instance IDs that this Geschaeft is linked to.

        A Geschaeft is linked to one eBau-NR, but an eBau-NR can contain
        multiple dossiers (instance ids). We therefore should link all instance
        IDs to a Geschaeft so we're able to correctly match them later on
        """
        instance_ids_str = ",".join(sorted(str(iid) for iid in new_instance_ids))

        self.parentkey = f"ebaube:{instance_ids_str}"

    def link_new_instance_id(self, instance_id: int) -> None:
        """Add given instance ID to this Geschaeft.

        A Geschaeft is linked to one eBau-NR, but an eBau-NR can contain
        multiple dossiers (instance ids). We therefore should link all instance
        IDs to a Geschaeft so we're able to correctly match them later on
        """

        self.set_linked_instance_ids(self.get_linked_instance_ids() + [instance_id])

    def get_folders(self, client: GEVERClient) -> list[Ordner]:
        """Return fully-loaded folder objects for this Geschaeft."""
        return [
            ref.resolve(client)
            for ref in self.dokumenteExplorer
            if ref.url.startswith("/Ordner")
        ]


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Reference(Generic[ModelType], BaseCMIObject):
    url: str

    def resolve(self, client: GEVERClient) -> ModelType:
        typename, guid_str = self.url.strip("/").split("/")
        return client.get_endpoint(typename).by_guid(guid_str)

    @classmethod
    def make_ref(cls, obj: ModelType) -> Reference[ModelType]:
        """Create a new "reference" to the given API object."""
        # The URL is always type/guid. And because we're naming our apimodel
        # classes strictly by their api names, we can directly translate it.
        return cls(
            guid=obj.guid,
            url=f"/{type(obj).__name__}/{obj.guid}",
        )


@dataclass_json()
@dataclass(kw_only=True)
class Rendition:
    """Document rendition, or "version".

    Each rendition represents a version of a document.
    """

    file: str
    fileName: str
    version: float


@dataclass_json()
@dataclass(kw_only=True)
class EDokument:
    """Checked in document."""

    inBearbeitungBei: str
    renditions: list[Rendition]


class DocStatus(Enum):
    ZWISCHENVERSION = "Zwischenversion"
    HAUPTVERSION = "Hauptversion"
    SCHLUSSVERSION = "Schlussversion"


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Dokument(BaseCMIObject):
    titel: Optional[str] = optional_field(fields.Str)
    displayName: Optional[str] = optional_field(fields.Str)
    url: Optional[str] = optional_field(fields.Str)
    eDokument: Optional[EDokument] = field(default=None)
    geschaeft: Reference[Geschaeft]

    # parentkey is what we use for a back-reference
    parentkey: Optional[str] = optional_field(fields.Str)

    # if a document is in a folder, it's this
    geschaeftPosteingangExplorer: Optional[Reference[Ordner]] = field(default=None)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Ordner(BaseCMIObject):
    """Folder representation.

    Used to structure documents
    """

    titel: Optional[str] = optional_field(fields.Str)
    children: Optional[list[Reference[Ordner | Dokument]]] = field(default_factory=list)
    parent: Optional[Reference[Ordner | Geschaeft]] = field(default=None)
    geschaeft: Optional[Reference[Geschaeft]] = field(default=None)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class Organisationseinheit(BaseCMIObject):
    displayName: Optional[str] = optional_field(fields.Str)


@dataclass_json(undefined=Undefined.INCLUDE)
@dataclass(kw_only=True)
class CustomAmt(BaseCMIObject):
    displayName: Optional[str] = optional_field(fields.Str)
