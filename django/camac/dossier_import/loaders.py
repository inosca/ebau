from dataclasses import fields
from enum import Enum

import pyexcel

from camac.dossier_import.dossier_classes import (
    Coordinates,
    Dossier,
    Person,
    SiteAddress,
)


class DossierLoader:
    dossier_class = Dossier


class XlsxFileDossierLoader(DossierLoader):
    path_to_dossiers_file: str
    simple_fields = [
        "id",
        "proposal",
        "cantonal_id",
        "parcel",
        "egrid",
        "usage",
        "type",
        "publication_date",
        "decision_date",
        "construction_start_date",
        "profile_approval_date",
        "completion_date",
        "link",
    ]

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

    def __init__(self, filepath: str):
        self.path_to_dossiers_file = filepath

    def _get_data_dict(self):
        pass

    def _load_dossier(self, dossier_row: dict) -> Dossier:
        """Read one line and handle each column.

        Based on the instance of the importer instanciate an ImportCaseData. Loading
        the dossier knows of every column value where to store it.
        """
        dossier = Dossier(
            **{
                key: dossier_row.get(getattr(Dossier.Meta.ListField, key).value)
                for key in self.simple_fields
            },
            coordinates=Coordinates(
                n=dossier_row[Dossier.Meta.ListField.coordinate_n.value],
                e=dossier_row[Dossier.Meta.ListField.coordinate_e.value],
            ),
            address=SiteAddress(
                **{
                    key: dossier_row.get(
                        getattr(Dossier.Meta.ListField, f"address_{key}").value
                    )
                    for key in SiteAddress.__annotations__.keys()
                }
            ),
            applicant=[
                Person(
                    **{
                        field.name: dossier_row.get(
                            getattr(
                                Dossier.Meta.ListField, f"applicant_{field.name}"
                            ).value
                        )
                        for field in fields(Person)
                    }
                )
            ],
            landowner=[
                Person(
                    **{
                        key: dossier_row.get(
                            getattr(Dossier.Meta.ListField, f"landowner_{key}").value
                        )
                        for key in Person.__annotations__.keys()
                    }
                )
            ],
            project_author=[
                Person(
                    **{
                        key: dossier_row.get(
                            getattr(
                                Dossier.Meta.ListField, f"projectauthor_{key}"
                            ).value
                        )
                        for key in Person.__annotations__.keys()
                    }
                )
            ],
        )
        dossier.Meta.target_state = dossier_row.get(Dossier.Meta.ListField.status.value)
        dossier.Meta.workflow = dossier_row.get(Dossier.Meta.ListField.workflow.value)
        return dossier

    def load(self):
        records = pyexcel.iget_records(file_name=self.path_to_dossiers_file)
        dossiers = []
        for record in records:
            dossiers.append(self._load_dossier(record))
        return dossiers
