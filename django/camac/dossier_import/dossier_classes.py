import datetime
from dataclasses import dataclass, field
from typing import IO, Optional

from camac.instance.models import Instance


@dataclass
class Coordinates:
    n: float
    e: float


@dataclass
class PlotData:
    egrid: str
    number: int
    municipality: str


@dataclass
class CalumaPlotData:
    plot_number: str
    egrid_number: str
    coord_east: float
    coord_north: float


@dataclass
class SiteAddress:
    street: str | None
    street_number: str | None
    city: str | None


@dataclass
class Person:
    first_name: str | None
    last_name: str | None
    company: str | None
    street: str | None
    street_number: str | None
    street_and_number: str | None = field(init=False)
    zip: int | None
    town: str | None
    country: str | None
    phone: str | None
    email: str | None
    is_juristic_person: bool = field(init=False)

    def __post_init__(self):
        self.is_juristic_person = bool(self.company)
        self.street_and_number = (
            " ".join(str(part) for part in (self.street, self.street_number) if part)
            or None
        )


@dataclass
class Attachment:
    file_accessor: IO
    name: str


@dataclass
class Dossier:
    id: str
    proposal: str
    cantonal_id: str | None = None
    plot_data: list[PlotData] | str | None = None
    coordinates: list[Coordinates] | str | None = None
    street: str | None = None
    street_number: str | None = None
    zip: str | None = None
    city: str | None = None
    usage: str | None = None
    application_type: str | None = None
    submit_date: datetime.datetime | str | None = None
    publication_date: datetime.datetime | str | None = None
    decision_date: datetime.datetime | str | None = None
    construction_start_date: datetime.datetime | str | None = None
    profile_approval_date: datetime.datetime | str | None = None
    final_approval_date: datetime.datetime | str | None = None
    completion_date: datetime.datetime | str | None = None
    link: str | None = None
    custom_1: str | None = None
    custom_2: str | None = None
    project_cost: str | None = None
    applicant: list[Person] | str | None = None
    landowner: list[Person] | str | None = None
    project_author: list[Person] | str | None = None
    attachments: list[Attachment] | str | None = None
    responsible: str | None = field(default=None)
    is_paper: bool = False

    _meta: Optional["Dossier.Meta"] = field(
        default_factory=lambda: Dossier.Meta(target_state="DRAFT")
    )

    @dataclass
    class Meta:
        target_state: str
        workflow: str | None = None
        instance: Instance | None = None
        missing: list = field(default_factory=list)
        errors: list = field(default_factory=list)
        warnings: list = field(default_factory=list)
