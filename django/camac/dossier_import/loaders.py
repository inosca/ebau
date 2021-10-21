import zipfile
from dataclasses import fields
from enum import Enum

import pyexcel
from pyproj import Transformer

from camac.dossier_import.dossier_classes import (
    Coordinates,
    Dossier,
    Parcel,
    Person,
    SiteAddress,
)


def numbers(string):
    return int("".join(char for char in str(string) if char.isdigit()) or 0)


def transform_coordinates(n, e):
    return Transformer.from_crs("epsg:2056", "epsg:4326").transform(n, e)


class DossierLoader:
    dossier_class = Dossier


class XlsxFileDossierLoader(DossierLoader):
    """Define the loader Excel file loader.

    The expected file needs to comply  with the column names
    and hold the data exactly as defined. This xlsx dossier loader
    is not generic.
    """

    path_to_dossiers_file: str
    simple_fields = [
        "id",
        "proposal",
        "cantonal_id",
        "usage",
        "type",
        "submit_date",
        "publication_date",
        "decision_date",
        "construction_start_date",
        "profile_approval_date",
        "completion_date",
        "link",
    ]

    required_fields = ("ID", "STATUS", "PROPOSAL")

    class Column(Enum):
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
        link = "LINK4"
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

    def _load_dossier(self, dossier_row: dict) -> Dossier:
        """Read one line and handle each column.

        Based on the instance of the importer instanciate an ImportCaseData. Loading
        the dossier knows of every column value where to store it.
        """
        dossier = Dossier(
            **{
                key: dossier_row.get(getattr(XlsxFileDossierLoader.Column, key).value)
                for key in self.simple_fields
            },
            parcel=self.load_parcels(dossier_row),
            coordinates=self.load_coordinates(dossier_row),
            address=SiteAddress(
                **{
                    field.name: dossier_row.get(
                        getattr(
                            XlsxFileDossierLoader.Column, f"address_{field.name}"
                        ).value
                    )
                    for field in fields(SiteAddress)
                }
            ),
            applicant=[
                Person(
                    **{
                        field.name: dossier_row.get(
                            getattr(
                                XlsxFileDossierLoader.Column, f"applicant_{field.name}"
                            ).value
                        )
                        for field in fields(Person)
                    }
                )
            ],
            landowner=[
                Person(
                    **{
                        field.name: dossier_row.get(
                            getattr(
                                XlsxFileDossierLoader.Column, f"landowner_{field.name}"
                            ).value
                        )
                        for field in fields(Person)
                    }
                )
            ],
            project_author=[
                Person(
                    **{
                        field.name: dossier_row.get(
                            getattr(
                                XlsxFileDossierLoader.Column,
                                f"projectauthor_{field.name}",
                            ).value
                        )
                        for field in fields(Person)
                    }
                )
            ],
        )
        # fixes
        for addr in ["applicant", "landowner", "project_author"]:
            addr_list = getattr(dossier, addr)
            addr_list[0].street = ", ".join(
                [addr_list[0].street, str(addr_list[0].street_number)]
            )
            setattr(dossier, addr, addr_list)
        dossier._meta = Dossier.Meta(
            target_state=dossier_row.get(XlsxFileDossierLoader.Column.status.value),
            workflow=dossier_row.get(XlsxFileDossierLoader.Column.workflow.value),
            missing=[],
        )
        for field in self.required_fields:
            if not dossier_row.get(field):
                dossier._meta.missing.append(field)
        return dossier

    def load_coordinates(self, dossier_row):
        out = []
        ee = dossier_row[XlsxFileDossierLoader.Column.coordinate_e.value]
        nn = dossier_row[XlsxFileDossierLoader.Column.coordinate_n.value]
        ee = ee.split(",") if type(ee) == str else [ee]
        nn = nn.split(",") if type(nn) == str else [nn]
        for e, n in zip(ee, nn):
            e, n = transform_coordinates(numbers(e), numbers(n))
            out.append(Coordinates(e=e, n=n))
        return out

    def load_parcels(self, dossier_row):
        out = []
        numbers = dossier_row[XlsxFileDossierLoader.Column.parcel.value]
        egrids = dossier_row[XlsxFileDossierLoader.Column.egrid.value]
        try:
            numbers = numbers.split(",") if type(numbers) == str else [numbers]
            egrids = egrids.split(",") if type(egrids) == str else [egrids]
            municipality = dossier_row[
                getattr(XlsxFileDossierLoader.Column, "address_city").value
            ]
            for number, egrid in zip(numbers, egrids):
                out.append(
                    Parcel(number=int(number), egrid=egrid, municipality=municipality)
                )
        except ValueError:  # pragma: no cover
            print(f"Failed to load parcels with numbers {numbers} and egrids {egrids}")
        return out

    def load(self):
        records = pyexcel.iget_records(file_name=self.path_to_dossiers_file)
        try:
            for record in records:
                yield self._load_dossier(record)
        except zipfile.BadZipfile:
            raise InvalidImportDataError(
                "Meta data file in archive is corrupt or not a valid .xlsx file."
            )


class InvalidImportDataError(Exception):
    pass
