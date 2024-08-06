import datetime
from dataclasses import dataclass, field
from typing import List, Optional, Union
from typing.io import IO

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
    street: Optional[str]
    street_number: Optional[str]
    city: Optional[str]


@dataclass
class Person:
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]
    street: Optional[str]
    street_number: Optional[str]
    zip: Optional[int]
    town: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    is_juristic_person: Optional[bool] = False

    def __post_init__(self):
        self.is_juristic_person = bool(self.company)


@dataclass
class Attachment:
    file_accessor: IO
    name: str


@dataclass
class Dossier:
    id: str
    proposal: str
    cantonal_id: Optional[str] = None
    plot_data: Optional[Union[List[PlotData], str]] = None
    coordinates: Optional[Union[List[Coordinates], str]] = None
    street: Optional[str] = None
    street_number: Optional[str] = None
    city: Optional[str] = None
    usage: Optional[str] = None
    application_type: Optional[str] = None
    submit_date: Optional[Union[datetime.datetime, str]] = None
    publication_date: Optional[Union[datetime.datetime, str]] = None
    decision_date: Optional[Union[datetime.datetime, str]] = None
    construction_start_date: Optional[Union[datetime.datetime, str]] = None
    profile_approval_date: Optional[Union[datetime.datetime, str]] = None
    final_approval_date: Optional[Union[datetime.datetime, str]] = None
    completion_date: Optional[Union[datetime.datetime, str]] = None
    link: Optional[str] = None
    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    applicant: Optional[Union[List[Person], str]] = None
    landowner: Optional[Union[List[Person], str]] = None
    project_author: Optional[Union[List[Person], str]] = None
    attachments: Optional[Union[List[Attachment], str]] = None
    responsible: Optional[str] = field(default=None)

    @dataclass
    class Meta:
        target_state: str
        workflow: Optional[str] = None
        instance: Optional[Instance] = None
        missing: Optional[List] = field(default_factory=list)
        errors: Optional[List] = field(default_factory=list)
        warnings: Optional[List] = field(default_factory=list)
