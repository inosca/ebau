import zipfile
from dataclasses import fields
from enum import Enum
from typing import Generator, Iterable, List, Optional, Tuple, Union

import openpyxl
from pyproj import Transformer

from camac.dossier_import.dossier_classes import (
    Attachment,
    Coordinates,
    Dossier,
    Person,
    PlotData,
)
from camac.dossier_import.messages import (
    LOG_LEVEL_ERROR,
    LOG_LEVEL_WARNING,
    FieldValidationMessage,
    Message,
    MessageCodes,
)


def numbers(string):
    return int("".join(char for char in str(string) if char.isdigit()) or 0)


def transform_coordinates(n, e):
    return Transformer.from_crs("epsg:2056", "epsg:4326").transform(n, e)


def safe_join(elements: Iterable, separator=" "):
    """Concatenate elements separated by a given separator.

    Avoid element `None` and allow all types that can be cast to `str`.
    """
    return separator.join(map(str, filter(None, elements))).strip()


class DossierLoader:
    """Dossier loader base class.

    In order to use DossierLoader classes add them to the settings.DOSSIER_IMPORT_LOADER_CLASSES.
    """

    dossier_class = Dossier


class XlsxFileDossierLoader(DossierLoader):
    """Load dossiers from xlsx in a zip archive with attachment directories.

    The expected zip file needs to comply with the following:
     - dossiers.xlsx file with column names as defined in this classes.Meta.Columns
     - every directory with a name equal to a dossier's ID will be searched for files
       that then are appended as attachments to the dossier's instance

    Validation and messaging is performed on loading data to the Dossier class.

    The dossier class has simple fields (mandatory and optional) and compound fields (usually
    non-standard objects defined as Dataclass or list thereof).

    Compound fields should provide their loading method that returns the loaded data object plus
    a Message, if validation is required.

    Simple fields should be validiated by the type definition of the Dossier dataclass and be added
    to the Loaders.simple_fields list.

    Any errors are added to the `dossiers._meta.errors` list.

    """

    path_to_dossiers_file: str
    simple_fields = [
        "address_city",
        "cantonal_id",
        "id",
        "link",
        "procedure_type",
        "proposal",
        "usage",
        "completion_date",
        "construction_start_date",
        "decision_date",
        "final_approval_date",
        "profile_approval_date",
        "publication_date",
        "submit_date",
    ]

    required_fields = ("id", "status", "proposal")

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
        procedure_type = "TYPE"
        submit_date = "SUBMIT-DATE"
        publication_date = "PUBLICATION-DATE"
        decision_date = "DECISION-DATE"
        construction_start_date = "CONSTRUCTION-START-DATE"
        profile_approval_date = "PROFILE-APPROVAL-DATE"
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

    def _load_dossier(self, dossier_row: dict) -> Dossier:
        """Read one line and handle each column.

        Based on the instance of the importer instanciate an ImportCaseData. Loading
        the dossier knows of every column value where to store it.
        """
        dossier = Dossier(
            **{
                key: dossier_row.get(getattr(XlsxFileDossierLoader.Column, key).value)
                for key in self.required_fields
                if key in self.simple_fields
            }
        )
        dossier._meta = Dossier.Meta(
            target_state=dossier_row.get(XlsxFileDossierLoader.Column.status.value),
            workflow=dossier_row.get(XlsxFileDossierLoader.Column.workflow.value),
            missing=[],
            errors=[],
        )

        for field in self.required_fields:
            if not dossier_row.get(getattr(XlsxFileDossierLoader.Column, field).value):
                dossier._meta.missing.append(field)

        for key in self.simple_fields:
            setattr(
                dossier,
                key,
                dossier_row.get(getattr(XlsxFileDossierLoader.Column, key).value),
            )

        dossier.plot_data, load_plot_data_errors = self.load_plot_data(dossier_row)
        if load_plot_data_errors:  # pragma: no cover
            dossier._meta.errors.append(load_plot_data_errors)

        dossier.coordinates, load_coordinates_errors = self.load_coordinates(
            dossier_row
        )
        if load_coordinates_errors:  # pragma: no cover
            dossier._meta.errors.append(load_coordinates_errors)

        dossier.address_location = safe_join(
            (
                dossier_row.get(XlsxFileDossierLoader.Column.address_street.value),
                dossier_row.get(XlsxFileDossierLoader.Column.address_street_nr.value),
            )
        )

        dossier.applicant = [
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
        ]
        dossier.landowner = [
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
        ]
        dossier.project_author = [
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
        ]
        return self.validate_fields(dossier)

    def validate_fields(self, dossier):
        for field in fields(dossier):
            if field.name not in self.simple_fields:
                continue
            field_name_snake = field.name.replace("_", "-")
            value = getattr(dossier, field.name)
            if hasattr(field.type, "__origin__") and field.type.__origin__ == Union:
                if not isinstance(value, field.type.__args__):
                    dossier._meta.errors.append(
                        FieldValidationMessage(
                            level=LOG_LEVEL_WARNING,
                            field=field_name_snake,
                            code=(
                                field.name in self.required_fields
                                and MessageCodes.REQUIRED_VALUES_MISSING.value
                            )
                            or MessageCodes.FIELD_VALIDATION_ERROR.value,
                            detail=f"Failed to load valid data for field `{field_name_snake}`. Value: `{value}` of type: `{type(value).__name__}`. Allowed: {', '.join([f'`{typ.__name__}`' for typ in field.type.__args__])}.",
                        )
                    )
                continue

            if not isinstance(value, field.type):
                dossier._meta.errors.append(
                    FieldValidationMessage(
                        level=(field.name in self.required_fields and LOG_LEVEL_ERROR)
                        or LOG_LEVEL_WARNING,
                        field=field_name_snake,
                        code=(
                            field.name in self.required_fields
                            and MessageCodes.REQUIRED_VALUES_MISSING.value
                        )
                        or MessageCodes.FIELD_VALIDATION_ERROR.value,
                        detail=f"Failed to load valid data for field `{field_name_snake}. Value: `{value}` of type: `{type(value).__name__}`. Allowed: `{field.type.__name__}`.",
                    )
                )

        return dossier

    def load_coordinates(
        self, dossier_row
    ) -> Tuple[List[Coordinates], Optional[List[Message]]]:
        out = []
        messages = []
        epoints = dossier_row[XlsxFileDossierLoader.Column.coordinate_e.value]
        npoints = dossier_row[XlsxFileDossierLoader.Column.coordinate_n.value]
        epoints = epoints.split(",") if type(epoints) == str else [epoints]
        npoints = npoints.split(",") if type(npoints) == str else [npoints]
        for e, n in zip(epoints, npoints):
            try:
                e, n = transform_coordinates(numbers(e), numbers(n))
            except ValueError:  # pragma: no cover
                messages.append(
                    FieldValidationMessage(
                        code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                        field="coordinates",
                        detail=f"Failed to load and transform coordinates from E: {e} and N: {n}",
                    )
                )
            out.append(Coordinates(e=e, n=n))
        return out, messages

    def load_plot_data(
        self, dossier_row
    ) -> Tuple[List[PlotData], Optional[List[Message]]]:
        out = []
        messages = []
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
                    PlotData(
                        number=number and int(number),
                        egrid=egrid,
                        municipality=municipality,
                    )
                )
        except ValueError:  # pragma: no cover
            messages.append(
                FieldValidationMessage(
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    field="plot-data",
                    detail=f"Failed to load parcels with numbers {numbers} and egrids {egrids}",
                )
            )
        return out, messages

    def load_dossiers(self, path_to_archive: str) -> Generator:
        archive = zipfile.ZipFile(path_to_archive, "r")
        data_file = archive.open("dossiers.xlsx")
        try:
            work_book = openpyxl.load_workbook(data_file)
        except zipfile.BadZipfile:
            raise InvalidImportDataError(
                "Meta data file in archive is corrupt or not a valid .xlsx file."
            )
        worksheet = work_book.worksheets[0]
        headings = worksheet[1]
        for row in worksheet.iter_rows(min_row=2):
            dossier = self._load_dossier(
                dict(
                    zip(
                        [heading.value for heading in headings],
                        [cell.value for cell in row],
                    )
                )
            )
            if dossier.id is None:  # pragma: no cover
                continue
            dossier = self._load_attachments(dossier, archive)
            yield dossier

    def _load_attachments(self, dossier, archive):
        for document_name in filter(
            lambda x: x.filename.startswith(f"{dossier.id}/"), archive.infolist()
        ):
            if document_name.filename.endswith("/"):
                continue
            if not dossier.attachments:
                dossier.attachments = []
            dossier.attachments.append(
                Attachment(
                    file_accessor=archive.open(document_name.filename, "r"),
                    name=document_name.filename,
                )
            )
        return dossier


class InvalidImportDataError(Exception):
    pass
