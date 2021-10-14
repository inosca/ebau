from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

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

    @dataclass
    class Meta:
        TARGET_STATUS_CHOICES = ["SUBMITTED", "APPROVED", "DONE"]
        WORKFLOW_CHOICES = ["BUILDINGPERMIT", "PRELIMINARY"]

        target_state: str
        workflow: Optional[str] = None
        instance: Optional[Instance] = None
        missing: Optional[List] = list

        class ListField(Enum):
            id = "ID"
            cantonal_id = "CANTONAL-ID"
            status = "STATUS"
            workflow = "WORKFLOW"
            parcel = "PARCEL"
            egrid = "EGRID"
            coordinate_n = "COORDINATE-N"
            coordinate_e = "COORDINATE-E"
            proposal = "PROPOSAL"
            address_street = "ADDRESS-STREET"
            address_street_nr = "ADDRESS-STREET-NR"
            address_city = "ADDRESS-CITY"
            usage = "USAGE"
            type = "TYPE"
            submit_date = "SUBMIT-DATE"
            publication_date = "PUBLICATION-DATE"
            decision_date = "DECISION-DATE"
            construction_start_date = "CONSTRUCTION-START-DATE"
            profile_approval_date = "PROFILE_APPROVAL-DATE"
            final_approval_date = "FINAL-APPROVAL-DATE"
            completion_date = "COMPLETION-DATE"
            custom_1 = "CUSTOM-1"
            custom_2 = "CUSTOM-2"
            link = "LINK"
            applicant_first_name = "APPLICANT-FIRST-NAME"
            applicant_last_name = "APPLICANT-LAST-NAME"
            applicant_company = "APPLICANT-COMPANY"
            applicant_street = "APPLICANT-STREET"
            applicant_street_number = "APPLICANT-STREET-NUMBER"
            applicant_city = "APPLICANT-CITY"
            applicant_phone = "APPLICANT-PHONE"
            applicant_email = "APPLICANT-EMAIL"
            landowner_first_name = "LANDOWNER-FIRST-NAME"
            landowner_last_name = "LANDOWNER-LAST-NAME"
            landowner_company = "LANDOWNER-COMPANY"
            landowner_street = "LANDOWNER-STREET"
            landowner_street_number = "LANDOWNER-STREET-NUMBER"
            landowner_city = "LANDOWNER-CITY"
            landowner_phone = "LANDOWNER-PHONE"
            landowner_email = "LANDOWNER-EMAIL"
            projectauthor_first_name = "PROJECTAUTHOR-FIRST-NAME"
            projectauthor_last_name = "PROJECTAUTHOR-LAST-NAME"
            projectauthor_company = "PROJECTAUTHOR-COMPANY"
            projectauthor_street = "PROJECTAUTHOR-STREET"
            projectauthor_street_number = "PROJECTAUTHOR-STREET-NUMBER"
            projectauthor_city = "PROJECTAUTHOR-CITY"
            projectauthor_phone = "PROJECTAUTHOR-PHONE"
            projectauthor_email = "PROJECTAUTHOR-EMAIL"
