import datetime
import zipfile
from enum import Enum
from typing import List

import openpyxl
from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from camac.dossier_import import messages
from camac.dossier_import.loaders import InvalidImportDataError
from camac.dossier_import.models import DossierImport

from .config.common import mimetypes
from .loaders import XlsxFileDossierLoader
from .messages import MessageCodes


class TargetStatus(Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WRITTEN_OFF = "WRITTEN OFF"
    DONE = "DONE"


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
        raise ValidationError(_("To start an import please upload a file."))

    try:
        archive = zipfile.ZipFile(source_file)
    except zipfile.BadZipfile:
        raise ValidationError(_("Uploaded file is not a valid .zip file"))
    try:
        metadata = archive.open("dossiers.xlsx")
    except KeyError:
        raise ValidationError(
            _("No metadata file 'dossiers.xlsx' found in uploaded archive.")
        )
    try:
        openpyxl.load_workbook(metadata, data_only=True)
    except zipfile.BadZipfile:
        raise ValidationError(
            _("Metadata file `dossiers.xlsx` is not a valid .xlsx file.")
        )
    return source_file


def validate_attachments(archive: zipfile.ZipFile, dossier_ids: List[str]):
    dirs = {
        filename.split("/")[0]
        for filename in archive.namelist()
        if "/" in filename and len(filename.split("/")) < 3
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
            for filename in archive.namelist()
            if filename.split("/")[0] in dossier_ids
            and not filename.endswith("/")
            and mimetypes.guess_type(filename)
        ]
    )


# flake8: noqa: C901
def validate_zip_archive_structure(instance_pk, clean_on_fail=True) -> DossierImport:
    """
    ZIP archive validation.

    scans the archive and best guesses the outcome of actually importing it.
    """
    dossier_import = DossierImport.objects.get(pk=instance_pk)

    configured_writer_cls = import_string(settings.DOSSIER_IMPORT["WRITER_CLASS"])
    writer = configured_writer_cls(
        user_id=dossier_import.user.pk,
        group_id=dossier_import.group.pk,
        location_id=dossier_import.location and dossier_import.location.pk,
    )

    archive = zipfile.ZipFile(dossier_import.source_file.path, "r")
    data_file = archive.open("dossiers.xlsx")
    try:
        work_book = openpyxl.load_workbook(data_file, data_only=True)
    except zipfile.BadZipfile:
        raise InvalidImportDataError(
            _("Meta data file in archive is corrupt or not a valid .xlsx file.")
        )
    worksheet = work_book.worksheets[0]
    headings = [h for h in worksheet[1] if h.value is not None]

    required_columns = ["ID", "STATUS", "PROPOSAL", "SUBMIT-DATE"]
    heading_values = [cell.value for cell in headings]
    missing = set(required_columns) - set(heading_values)
    if missing:
        raise InvalidImportDataError(
            _(
                "Meta data file in archive is missing required columns %(missing)s. Found %(found)s"
            )
            % dict(missing=missing, found=heading_values)
        )
    extra = set(heading_values) - set([e.value for e in XlsxFileDossierLoader.Column])
    if extra:
        dossier_import.messages["validation"]["summary"]["warning"].append(
            _(
                "Found unknown columns: %(extra)s. Those columns will be ignored while importing."
            )
            % dict(extra=extra)
        )

    status_column = next((col for col in headings if col.value == "STATUS")).col_idx - 1
    submit_date_column = (
        next((col for col in headings if col.value == "SUBMIT-DATE")).col_idx - 1
    )
    id_column = next((col for col in headings if col.value == "ID")).col_idx - 1

    dossier_msgs = []

    # read entired worksheet into python data structure, because case-by-case lookups
    # in openpyxl are slow
    rows = [r for r in worksheet.rows if r[id_column].value is not None]
    # skip header row
    rows = rows[1:]

    dossier_ids = [r[id_column].value for r in rows]
    dupes = set([d for d in dossier_ids if dossier_ids.count(d) > 1])

    for dupe in dupes:
        messages.append_or_update_dossier_message(
            dupe,
            "id",
            f"{dupe} is not unique.",
            MessageCodes.DUPLICATE_IDENTFIER_ERROR.value,
            dossier_msgs,
        )

    existing = [
        dossier_id
        for dossier_id in set(dossier_ids)
        if writer.existing_dossier(dossier_id)
    ]
    for dossier_id in existing:
        messages.append_or_update_dossier_message(
            dossier_id,
            "ID",
            f"Dossier with {dossier_id} already exists",
            MessageCodes.DUPLICATE_IDENTFIER_ERROR.value,
            dossier_msgs,
            level=messages.Severity.ERROR.value,
        )

    dossiers_success = list(set(dossier_ids))

    for date_column in [cell for cell in headings if cell.value.endswith("-DATE")]:
        for dossier_id, value in [
            (r[id_column].value, r[date_column.col_idx - 1].value) for r in rows
        ]:
            try:
                assert not value or type(value) == datetime.datetime
            except AssertionError:
                messages.append_or_update_dossier_message(
                    dossier_id,
                    date_column.value.lower(),
                    str(value),
                    MessageCodes.DATE_FIELD_VALIDATION_ERROR.value,
                    dossier_msgs,
                )

    if status_column:
        for dossier_id, status in [
            (r[id_column].value, r[status_column].value) for r in rows
        ]:
            if status not in [e.value for e in TargetStatus]:
                if not status:
                    messages.append_or_update_dossier_message(
                        dossier_id,
                        "status",
                        None,
                        MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                        dossier_msgs,
                        level=messages.Severity.ERROR.value,
                    )
                    try:
                        dossiers_success.remove(dossier_id)
                    except ValueError:  # pragma: no cover
                        pass
                    continue

                messages.append_or_update_dossier_message(
                    dossier_id,
                    "status",
                    status,
                    MessageCodes.STATUS_CHOICE_VALIDATION_ERROR.value,
                    dossier_msgs,
                    level=messages.Severity.ERROR.value,
                )
                try:
                    dossiers_success.remove(dossier_id)
                except ValueError:  # pragma: no cover
                    pass

    if submit_date_column:
        for dossier_id, submit_date in [
            (r[id_column].value, r[submit_date_column].value) for r in rows
        ]:
            if not submit_date:
                messages.append_or_update_dossier_message(
                    dossier_id,
                    "submit_date",
                    None,
                    MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
                    dossier_msgs,
                    level=messages.Severity.ERROR.value,
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
