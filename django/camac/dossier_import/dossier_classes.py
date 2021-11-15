from dataclasses import dataclass
from typing import List, Optional
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
class SiteAddress:
    street: Optional[str]
    street_nr: Optional[str]
    city: Optional[str]


@dataclass
class Person:
    first_name: Optional[str]
    last_name: Optional[str]
    company: Optional[str]
    street: Optional[str]
    street_number: Optional[str]
    city: Optional[str]
    phone: Optional[str]
    email: Optional[str]


@dataclass
class Attachment:
    file_accessor: IO
    name: str


@dataclass
class Dossier:
    id: str
    proposal: str
    cantonal_id: Optional[str] = None
    plot_data: Optional[List[PlotData]] = None
    coordinates: Optional[List[Coordinates]] = None
    address_location: Optional[str] = None
    address_city: Optional[str] = None
    usage: Optional[str] = None
    procedure_type: Optional[str] = None
    submit_date: Optional[str] = None
    publication_date: Optional[str] = None
    decision_date: Optional[str] = None
    construction_start_date: Optional[str] = None
    profile_approval_date: Optional[str] = None
    final_approval_date: Optional[str] = None
    completion_date: Optional[str] = None
    link: Optional[str] = None
    custom_1: Optional[str] = None
    custom_2: Optional[str] = None
    applicant: Optional[List[Person]] = None
    landowner: Optional[List[Person]] = None
    project_author: Optional[List[Person]] = None
    attachments: Optional[List[Attachment]] = None

    @dataclass
    class Meta:
        TARGET_STATUS_CHOICES = ["SUBMITTED", "APPROVED", "DONE"]
        WORKFLOW_CHOICES = ["BUILDINGPERMIT", "PRELIMINARY"]

        target_state: str
        workflow: Optional[str] = None
        instance: Optional[Instance] = None
        missing: Optional[List] = list
        errors: Optional[List] = list
