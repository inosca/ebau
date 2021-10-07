from dataclasses import dataclass
from typing import Optional

from camac.instance.models import Instance


@dataclass
class Coordinates:
    n: int
    e: int


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
class Dossier:
    id: str
    proposal: str
    cantonal_id: Optional[str] = None
    parcel: Optional[str] = None
    egrid: Optional[str] = None
    coordinates: Optional[Coordinates] = None
    address: Optional[SiteAddress] = None
    usage: Optional[str] = None
    type: Optional[str] = None
    publication_date: Optional[str] = None
    decision_date: Optional[str] = None
    construction_start_date: Optional[str] = None
    profile_approval_date: Optional[str] = None
    completion_date: Optional[str] = None
    link: Optional[str] = None
    applicant: Optional[Person] = None
    landowner: Optional[Person] = None
    project_author: Optional[Person] = None

    class Meta:
        TARGET_STATUS_CHOICES = ["SUBMITTED", "APPROVED", "DONE"]
        WORKFLOW_CHOICES = ["BUILDINGPERMIT", "PRELIMINARY"]

        target_state: str
        workflow: Optional[str]
        instance: Optional[Instance]
