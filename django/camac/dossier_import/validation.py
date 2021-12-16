import datetime
import zipfile
from typing import List

import openpyxl
from django.utils import timezone, translation
from django.utils.translation import gettext as _

from camac.dossier_import import messages
from camac.dossier_import.loaders import InvalidImportDataError
from camac.dossier_import.models import DossierImport

from .config.common import mimetypes
from .messages import (
    BadXlsxFileError,
    InvalidZipFileError,
    MessageCodes,
    MissingArchiveFileError,
    MissingMetadataFileError,
)
from rest_framework.exceptions import ValidationError


def verify_source_file(source_file: str) -> str:
    """
    Verify source file is valid archive and has content.

    Verfication here goes pretty far. But since it's about rather big archive files
    we do not want to store any file that is not going to survive the first
    step of processing anyway.

    Failing to validate source_file results in an APIError i. e. bad request

    The following steps are required:
     - archive must be a ZIP file
     - the archive must contain a dossiers.xlsx
     - the dossiers.xlsx must in fact be a XLSX file
    """
    if source_file is None:
        raise MissingArchiveFileError(_("To start an import please upload a file."))

    try:
        archive = zipfile.ZipFile(source_file)
    except zipfile.BadZipfile:
        raise InvalidZipFileError(_("Uploaded file is not a valid .zip file"))
    try:
        metadata = archive.open("dossiers.xlsx")
    except KeyError:
        raise MissingMetadataFileError(
            _("No metadata file 'dossiers.xlsx' found in uploaded archive.")
        )
    try:
        openpyxl.load_workbook(metadata)
    except zipfile.BadZipfile:
        raise ValidationError(
            _("Metadata file `dossiers.xlsx` is not a valid .xlsx file.")
        )
    return source_file


def validate_attachments(archive: zipfile.ZipFile, dossier_ids: List[str]):
    dirs = {
        zipinfo.filename.split("/")[0]
        for zipinfo in archive.filelist
        if zipinfo.filename.endswith("/") and len(zipinfo.filename.split("/")) < 3
    }
    orphan_dirs = sorted(list(dirs - set(dossier_ids)))
    result = []
    if orphan_dirs:
        result.append(
            _(
                "%(count)i document folders were not found in the metadata file and will not be imported:\n%(entries)s"
            )
            % dict(count=len(orphan_dirs), entries=", ".join(orphan_dirs))
        )
    dossiers_without_documents = list(set(dossier_ids) - dirs)
    if dossiers_without_documents:
        result.append(
            _("%(count)i dossiers have no document folder.")
            % dict(count=len(dossiers_without_documents))
        )
    return result


def get_attachment_validation_stats(archive: zipfile.ZipFile, dossier_ids: List[str]):
    return sum(
        [
            1
            for url in archive.filelist
            if url.filename.split("/")[0] in dossier_ids
            and not url.filename.endswith("/")
            and mimetypes.guess_type(url.filename)
        ]
    )


# flake8: noqa: C901
def validate_zip_archive_structure(instance_pk, clean_on_fail=True) -> DossierImport:
    """
    ZIP archive validation.

    scans the archive and best guesses the outcome of actually importing it.
    """
    dossier_import = DossierImport.objects.get(pk=instance_pk)

    archive = zipfile.ZipFile(dossier_import.source_file.path, "r")
    data_file = archive.open("dossiers.xlsx")
    try:
        work_book = openpyxl.load_workbook(data_file)
    except zipfile.BadZipfile:
        raise InvalidImportDataError(
            _("Meta data file in archive is corrupt or not a valid .xlsx file.")
        )
    worksheet = work_book.worksheets[0]
    headings = worksheet[1]

    required_columns = ["ID", "STATUS", "PROPOSAL", "SUBMIT-DATE"]
    heading_values = [col.value for col in headings]
    missing = set(required_columns) - set(heading_values)
    if missing:
        raise InvalidImportDataError(
            _("Meta data file in archive is missing required columns %(missing)s.")
            % dict(missing=missing)
        )

    status_column = next((col for col in headings if col.value == "STATUS"))
    submit_date_column = next((col for col in headings if col.value == "SUBMIT-DATE"))
    id_column = next((col for col in headings if col.value == "ID"))

    dossier_msgs = []
    deleted_rows = 0
    for cell in worksheet[id_column.column_letter]:
        if cell.value is not None:
            continue
        worksheet.delete_rows(cell.row, 1)
        deleted_rows += 1

    dossier_ids = [cell.value for cell in worksheet[id_column.column_letter][1:]]

    dupes = set([d for d in dossier_ids if dossier_ids.count(d) > 1])

    for dupe in dupes:
        messages.append_or_update_dossier_message(
            dupe,
            "id",
            f"{dupe} is not unique.",
            MessageCodes.DUPLICATE_IDENTFIER_ERROR.value,
            dossier_msgs,
        )

    dossiers_success = list(set(dossier_ids))

    for date_column in [col for col in headings if col.value.endswith("-DATE")]:
        for cell in worksheet[date_column.column_letter][1:]:
            dossier_id = worksheet[f"A{cell.row}"].value
            field_name = worksheet[f"{cell.column_letter}1"].value.lower()
            try:
                assert cell.value is None or type(cell.value) == datetime.datetime
            except AssertionError:
                messages.append_or_update_dossier_message(
                    dossier_id,
                    field_name,
                    str(cell.value),
                    MessageCodes.DATE_FIELD_VALIDATION_ERROR.value,
                    dossier_msgs,
                )
                try:
                    dossiers_success.remove(dossier_id)
                except ValueError:
                    pass
                continue

    status_choices = ["SUBMITTED", "APPROVED", "DONE"]

    if status_column:
        for cell in worksheet[status_column.column_letter][1:]:
            dossier_id = worksheet[f"A{cell.row}"].value
            if cell.value not in status_choices:
                if cell.value is None:
                    messages.append_or_update_dossier_message(
                        dossier_id,
                        "status",
                        None,
                        MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                        dossier_msgs,
                        level=messages.LOG_LEVEL_ERROR,
                    )
                    try:
                        dossiers_success.remove(dossier_id)
                    except ValueError:  # pragma: no cover
                        pass
                    continue

                messages.append_or_update_dossier_message(
                    dossier_id,
                    "status",
                    cell.value,
                    MessageCodes.STATUS_CHOICE_VALIDATION_ERROR.value,
                    dossier_msgs,
                    level=messages.LOG_LEVEL_ERROR,
                )
                try:
                    dossiers_success.remove(dossier_id)
                except ValueError:  # pragma: no cover
                    pass

    if submit_date_column:
        for cell in worksheet[submit_date_column.column_letter][1:]:
            dossier_id = worksheet[f"A{cell.row}"].value
            if not cell.value:
                messages.append_or_update_dossier_message(
                    dossier_id,
                    "submit_date",
                    None,
                    MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                    dossier_msgs,
                    level=messages.LOG_LEVEL_ERROR,
                )
                try:
                    dossiers_success.remove(dossier_id)
                except ValueError:  # pragma: no cover
                    pass

    for msg in dossier_msgs:
        messages.update_messages_section_detail(
            msg, dossier_import, section="validation"
        )

    dossier_import = messages.update_summary(dossier_import)
    dossier_import.messages["validation"]["summary"]["warning"] += validate_attachments(
        archive, dossier_ids
    )
    dossier_import.messages["validation"]["summary"]["stats"] = {
        "attachments": get_attachment_validation_stats(archive, dossier_ids),
        "dossiers": len(dossiers_success),
    }

    dossier_import.messages["validation"]["completed"] = timezone.localtime().strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )
    dossier_import.save()

    dossier_import.status = dossier_import.IMPORT_STATUS_VALIDATION_SUCCESSFUL
    if dossier_import.messages["validation"]["summary"]["error"]:
        dossier_import.status = dossier_import.IMPORT_STATUS_VALIDATION_FAILED
        if clean_on_fail:
            dossier_import.source_file.delete()
    dossier_import.save()

    return dossier_import
