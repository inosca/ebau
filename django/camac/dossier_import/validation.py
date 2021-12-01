import copy
import datetime
import zipfile
from typing import List

import openpyxl
from django.utils import timezone
from django.utils.translation import gettext as _

from camac.dossier_import import messages
from camac.dossier_import.loaders import InvalidImportDataError
from camac.dossier_import.models import DossierImport

from .config.common import mimetypes
from .messages import (
    BadXlsxFileError,
    InvalidZipFileError,
    MissingArchiveFileError,
    MissingMetadataFileError,
)


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
        raise MissingArchiveFileError

    try:
        archive = zipfile.ZipFile(source_file)
    except zipfile.BadZipfile:
        raise InvalidZipFileError(detail=_("Uploaded file is not a valid .zip file"))
    try:
        metadata = archive.open("dossiers.xlsx")
    except KeyError:
        raise MissingMetadataFileError
    try:
        openpyxl.load_workbook(metadata)
    except zipfile.BadZipfile:
        raise BadXlsxFileError
    return source_file


def validate_attachments(archive: zipfile.ZipFile, dossier_ids: List[str]):
    dirs = {
        zipinfo.filename.split("/")[0]
        for zipinfo in archive.filelist
        if zipinfo.filename.endswith("/") and len(zipinfo.filename.split("/")) < 3
    }

    return {
        "missing_metadata": list(dirs - set(dossier_ids)),
        "dossiers_without_attachments": len(list(set(dossier_ids) - dirs)),
        "num_documents": sum(
            [
                1
                for url in archive.filelist
                if url.filename.split("/")[0] in dossier_ids
                and not url.filename.endswith("/")
                and mimetypes.guess_type(url.filename)
            ]
        ),
    }


# flake8: noqa: C901
def validate_zip_archive_structure(
    instance_pk,
) -> messages.FormattedListMessage:
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
            "Meta data file in archive is corrupt or not a valid .xlsx file."
        )
    worksheet = work_book.worksheets[0]
    headings = worksheet[1]

    try:
        status_column = next((col for col in headings if col.value == "STATUS"))
    except StopIteration:
        raise InvalidImportDataError(
            "Meta data file in archive has no column 'STATUS'."
        )

    dossier_msgs = []
    id_column = next((col for col in headings if col.value == "ID"))

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
            dupe, "id", f"{dupe} is not unique.", dossier_msgs
        )

    dossiers_success = copy.deepcopy(list(set(dossier_ids)))

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
                    f"{cell.value} could not be parsed as date. Allowed format: dd.mm.YYYY",
                    dossier_msgs,
                )
                try:
                    dossiers_success.remove(dossier_id)
                except ValueError:
                    pass
                continue

    status_choices = ["SUBMITTED", "APPROVED", "DONE"]

    for cell in worksheet[status_column.column_letter][1:]:
        dossier_id = worksheet[f"A{cell.row}"].value
        if cell.value not in status_choices:
            messages.append_or_update_dossier_message(
                dossier_id,
                "status",
                f"{cell.value} is not one of {status_choices}",
                dossier_msgs,
            )
            try:
                dossiers_success.remove(dossier_id)
            except ValueError:  # pragma: no cover
                pass
            continue

    for msg in dossier_msgs:
        messages.update_messages_section_detail(
            msg, dossier_import, section="validation"
        )

    dossier_import = messages.update_summary(dossier_import)
    attachment_summary = validate_attachments(archive, dossier_ids)
    dossier_import.messages["validation"]["summary"].update(attachment_summary)
    dossier_import.messages["validation"]["completed"] = timezone.localtime().strftime(
        "%Y-%m-%dT%H:%M:%S%z"
    )
    dossier_import.save()

    dossier_import.status = dossier_import.IMPORT_STATUS_VALIDATION_SUCCESSFUL
    if (
        dossier_import.messages["validation"]["summary"]["errors"]
        or dossier_import.messages["validation"]["summary"]["dossiers_error"]
        or dossier_import.messages["validation"]["summary"]["dossiers_warning"]
    ):
        dossier_import.status = dossier_import.IMPORT_STATUS_VALIDATION_FAILED
    dossier_import.messages["validation"]["summary"]["dossiers_success"] = len(
        set(dossiers_success)
    )
    dossier_import.save()

    return dossier_import
