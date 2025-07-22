import itertools
import zipfile
from dataclasses import fields
from enum import Enum
from typing import Generator, Iterable, List, Optional, Tuple

from django.conf import settings
from django.utils.timezone import datetime
from django.utils.translation import gettext as _
from pyproj import Transformer

from camac.dossier_import.dossier_classes import (
    Attachment,
    Coordinates,
    Dossier,
    Person,
    PlotData,
)
from camac.dossier_import.messages import (
    FieldValidationMessage,
    Message,
    MessageCodes,
    Severity,
)
from camac.dossier_import.models import DossierImport
from camac.dossier_import.utils import get_worksheet_headings_and_rows


def numbers(string):
    if isinstance(string, float) or isinstance(string, int):
        return string

    return int("".join(char for char in str(string) if char.isdigit()) or 0)


def transform_coordinates(n, e, target="epsg:4326"):
    """Transform coordinates from the swiss format to something else."""
    return Transformer.from_crs("epsg:2056", target).transform(n, e)


def safe_join(elements: Iterable, separator=" "):
    """Concatenate elements separated by a given separator.

    Avoid element `None` and allow all types that can be cast to `str`.
    """
    return separator.join(map(str, filter(None, elements))).strip()


class DossierLoader:
    class ConfigurationError(Exception):
        pass

    def load_dossiers(self, param: DossierImport):
        raise DossierLoader.ConfigurationError  # pragma: no cover


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

    date_format = "%d.%m.%Y"

    dossier_class = Dossier
    path_to_dossiers_file: str
    simple_fields = [
        "id",
        "proposal",
        "cantonal_id",
        "street",
        "street_number",
        "city",
        "usage",
        "application_type",
        "custom_1",
        "custom_2",
        "link",
        "responsible",
    ]
    date_fields = [
        "submit_date",
        "publication_date",
        "decision_date",
        "construction_start_date",
        "completion_date",
        "decision_date",
        "final_approval_date",
        "profile_approval_date",
        "publication_date",
        "submit_date",
    ]

    required_fields = ("id", "status", "proposal", "submit_date")

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
        street = "ADDRESS-STREET"
        street_number = "ADDRESS-STREET-NR"
        city = "ADDRESS-CITY"
        usage = "USAGE"
        application_type = "TYPE"
        submit_date = "SUBMIT-DATE"
        publication_date = "PUBLICATION-DATE"
        decision_date = "DECISION-DATE"
        construction_start_date = "CONSTRUCTION-START-DATE"
        profile_approval_date = "PROFILE-APPROVAL-DATE"
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
        applicant_zip = "APPLICANT-ZIP"
        applicant_town = "APPLICANT-CITY"
        applicant_phone = "APPLICANT-PHONE"
        applicant_email = "APPLICANT-EMAIL"
        landowner_first_name = "LANDOWNER-FIRST-NAME"
        landowner_last_name = "LANDOWNER-LAST-NAME"
        landowner_company = "LANDOWNER-COMPANY"
        landowner_street = "LANDOWNER-STREET"
        landowner_street_number = "LANDOWNER-STREET-NUMBER"
        landowner_zip = "LANDOWNER-ZIP"
        landowner_town = "LANDOWNER-CITY"
        landowner_phone = "LANDOWNER-PHONE"
        landowner_email = "LANDOWNER-EMAIL"
        projectauthor_first_name = "PROJECTAUTHOR-FIRST-NAME"
        projectauthor_last_name = "PROJECTAUTHOR-LAST-NAME"
        projectauthor_company = "PROJECTAUTHOR-COMPANY"
        projectauthor_street = "PROJECTAUTHOR-STREET"
        projectauthor_street_number = "PROJECTAUTHOR-STREET-NUMBER"
        projectauthor_zip = "PROJECTAUTHOR-ZIP"
        projectauthor_town = "PROJECTAUTHOR-CITY"
        projectauthor_phone = "PROJECTAUTHOR-PHONE"
        projectauthor_email = "PROJECTAUTHOR-EMAIL"
        responsible = "RESPONSIBLE"

    def load_person(self, dossier_row, prefix):
        """Construct a Person object for a type if any value is given.

        prefix selects respective person properties, e. g. applicant
          `applicant_first_name`
          `applicant_town`
          ...

        """
        person = {
            field.name: dossier_row.get(
                getattr(XlsxFileDossierLoader.Column, f"{prefix}_{field.name}").value
            )
            for field in fields(Person)
            if hasattr(XlsxFileDossierLoader.Column, f"{prefix}_{field.name}")
        }
        if any(
            value == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]
            for value in person.values()
        ):
            return [settings.DOSSIER_IMPORT["DELETE_KEYWORD"]]
        if any(person.values()):
            return [Person(**person)]

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
            workflow=dossier_row.get(XlsxFileDossierLoader.Column.workflow.value)
            or "BUILDINGPERMIT",
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
        for key in self.date_fields:
            date = dossier_row.get(getattr(XlsxFileDossierLoader.Column, key).value)
            if not date:
                continue
            if not isinstance(date, datetime):
                if date == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]:
                    setattr(dossier, key, date)
                    continue
                try:
                    date = datetime.strptime(date, self.date_format)
                except (ValueError, TypeError):
                    dossier._meta.errors.append(
                        FieldValidationMessage(
                            level=Severity.ERROR.value,
                            field=key,
                            code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                            detail=(
                                f"{date} is not valid for field {key}. Allowed format: "
                                f"{datetime.strftime(datetime.now(), self.date_format)}"
                            ),
                        )
                    )
                    date = date
            setattr(dossier, key, date)

        dossier.plot_data, load_plot_data_errors = self.load_plot_data(dossier_row)
        if load_plot_data_errors:  # pragma: no cover
            dossier._meta.errors += load_plot_data_errors

        dossier.coordinates, load_coordinates_errors = self.load_coordinates(
            dossier_row
        )
        if load_coordinates_errors:  # pragma: no cover
            dossier._meta.errors += load_coordinates_errors

        dossier.applicant = self.load_person(dossier_row, prefix="applicant")
        dossier.landowner = self.load_person(dossier_row, prefix="landowner")
        dossier.project_author = self.load_person(dossier_row, prefix="projectauthor")

        return dossier

    def load_coordinates(
        self, dossier_row
    ) -> Tuple[List[Coordinates], Optional[List[Message]]]:
        out = []
        messages = []
        epoints = dossier_row.get(XlsxFileDossierLoader.Column.coordinate_e.value)
        npoints = dossier_row.get(XlsxFileDossierLoader.Column.coordinate_n.value)
        if not (epoints and npoints):
            return None, messages
        epoints = epoints.split(",") if isinstance(epoints, str) else [epoints]
        npoints = npoints.split(",") if isinstance(npoints, str) else [npoints]
        for e, n in zip(epoints, npoints):
            e, n = numbers(e), numbers(n)

            if any(
                val == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]
                for val in epoints + npoints
            ):
                return [settings.DOSSIER_IMPORT["DELETE_KEYWORD"]], messages
            if not (2480000 < e < 2840000.999) or not (1070000 < n < 1300000.999):
                messages.append(
                    FieldValidationMessage(
                        level=Severity.WARNING.value,
                        code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                        field="coordinates",
                        detail=_(
                            "The given coordinates (E: %(e)i and N: %(n)i) are not in Switzerland or are not using the Swiss coordinate system (epsg:2056)."
                        )
                        % dict(e=e, n=n),
                    )
                )
                continue

            target_coords = settings.DOSSIER_IMPORT.get("TRANSFORM_COORDINATE_SYSTEM")
            if target_coords:
                try:
                    e, n = transform_coordinates(e, n, target_coords)
                except ValueError:  # pragma: no cover
                    messages.append(
                        FieldValidationMessage(
                            level=Severity.WARNING.value,
                            code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                            field="coordinates",
                            detail=_(
                                "Failed to load and transform coordinates from E: %(e)i and N: %(n)i"
                            )
                            % dict(e=e, n=n),
                        )
                    )
                    continue
            out.append(Coordinates(e=e, n=n))
        return out, messages

    def load_plot_data(
        self, dossier_row
    ) -> Tuple[List[PlotData], Optional[List[Message]]]:
        out = []
        messages = []
        plot_numbers = dossier_row.get(XlsxFileDossierLoader.Column.parcel.value)
        egrids = dossier_row.get(XlsxFileDossierLoader.Column.egrid.value)
        if not (plot_numbers or egrids):
            return None, messages
        try:
            plot_numbers = (
                [p.strip() for p in plot_numbers.split(",")]
                if isinstance(plot_numbers, str)
                else [plot_numbers]
            )

            egrids = (
                [e.strip() for e in egrids.split(",")]
                if isinstance(egrids, str)
                else [egrids]
            )
            municipality = dossier_row.get(
                getattr(XlsxFileDossierLoader.Column, "city").value
            )

            # handle deletable value
            if any(
                val == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]
                for val in plot_numbers + egrids + [municipality]
            ):
                return [settings.DOSSIER_IMPORT["DELETE_KEYWORD"]], messages
            for number, egrid in itertools.zip_longest(plot_numbers, egrids):
                out.append(
                    PlotData(
                        number=str(number),
                        egrid=egrid,
                        municipality=municipality,
                    )
                )
        except ValueError:  # pragma: no cover
            messages.append(
                FieldValidationMessage(
                    level=Severity.WARNING.value,
                    code=MessageCodes.FIELD_VALIDATION_ERROR.value,
                    field="plot-data",
                    detail=_(
                        "Failed to load plot with numbers `%(plot_numbers)s` and egrid values `%(egrids)s`"
                    )
                    % dict(plot_numbers=plot_numbers, egrids=egrids),
                )
            )
        return out, messages

    def load_dossiers(
        self, dossier_import: DossierImport
    ) -> Generator[Dossier, None, None]:
        archive: zipfile.ZipFile = dossier_import.get_archive()
        data_file = archive.open("dossiers.xlsx")

        try:
            __, rows = get_worksheet_headings_and_rows(data_file)
        except zipfile.BadZipfile:
            raise InvalidImportDataError(
                _("Meta data file in archive is corrupt or not a valid .xlsx file.")
            )

        for row in rows:
            dossier = self._load_dossier(row)
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
