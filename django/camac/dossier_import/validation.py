import zipfile
from enum import Enum
from typing import List

from django.conf import settings
from django.utils import timezone
from django.utils.module_loading import import_string
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from camac.dossier_import import messages
from camac.dossier_import.loaders import InvalidImportDataError
from camac.dossier_import.models import DossierImport
from camac.dossier_import.utils import get_worksheet_headings_and_rows

from .config.common import mimetypes
from .loaders import XlsxFileDossierLoader
from .messages import MessageCodes


class TargetStatus(Enum):
    SUBMITTED = "SUBMITTED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    WRITTEN_OFF = "WRITTEN OFF"
    DONE = "DONE"


REQUIRED_COLUMNS = ["proposal", "status", "submit-date"]


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
        zipfile.ZipFile(metadata, "r")
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


def get_dossier_cell_by_column(dossier_id, col_name, rows):
    row = next((row for row in rows if row.get("ID") == dossier_id), None)

    if not row:  # pragma: no cover
        return None

    return row.get(col_name.upper(), None)


def _validate_date_fields(
    dossier_id, dossier_messages, headings, rows, allow_delete=False
) -> bool:
    # pyexcel-xlsx may provide data from cells based on the cell formatting.
    # Specs define that we accept values in the XlsxFileDossierLoader.date_format.
    # something similar to "03.04.2001".
    # Uplodaded documents can feature those columns formatted as datetime as well as
    # strings with correctly entered data. In that case we should try to parse that
    # value or return instructions.
    valid = True
    for date_column in [heading for heading in headings if heading.endswith("-DATE")]:
        if date := get_dossier_cell_by_column(dossier_id, date_column, rows):
            # We'll use these for handling messages below repeatedly.
            # Individual messages require `code`, `detail` and `level`
            # set separately.
            message_defaults = {
                "dossier_id": dossier_id,
                "field_name": date_column,
                "messages": dossier_messages,
            }

            if date == settings.DOSSIER_IMPORT["DELETE_KEYWORD"]:
                if allow_delete:
                    messages.append_or_update_dossier_message(
                        code=MessageCodes.VALUE_DELETED,
                        detail="Date will be deleted",
                        level=messages.Severity.INFO.value,
                        **message_defaults,
                    )

                else:
                    messages.append_or_update_dossier_message(
                        code=MessageCodes.FIELD_VALIDATION_ERROR,
                        detail=_(
                            "The value %(value)s will be ignored because deletion is not supported for new dossiers."
                        )
                        % {"value": date},
                        level=messages.Severity.WARNING.value,
                        **message_defaults,
                    )

                continue

            if not isinstance(date, timezone.datetime):
                try:
                    date = timezone.datetime.strptime(
                        date, XlsxFileDossierLoader.date_format
                    )
                except ValueError:
                    messages.append_or_update_dossier_message(
                        detail=str(date),
                        code=MessageCodes.DATE_FIELD_VALIDATION_ERROR.value,
                        level=messages.Severity.ERROR.value,
                        **message_defaults,
                    )
                    valid = False
    return valid


def _validate_existing_dossier(dossier_id, dossier_msgs, headings, rows):
    messages.append_or_update_dossier_message(
        dossier_id=dossier_id,
        field_name="ID",
        detail=dossier_id,
        code=MessageCodes.UPDATE_DOSSIER.value,
        messages=dossier_msgs,
        level=messages.Severity.WARNING.value,
    )
    # reimporting does not require the "STATUS" column to be present, therefore
    # we ignore that column
    if status := get_dossier_cell_by_column(dossier_id, "status", rows):
        messages.append_or_update_dossier_message(
            dossier_id=dossier_id,
            field_name="STATUS",
            detail=_("The value %(value)s will be ignored when updating the dossier.")
            % {"value": status},
            code=MessageCodes.UPDATE_DOSSIER.value,
            messages=dossier_msgs,
            level=messages.Severity.INFO.value,
        )

    _validate_date_fields(dossier_id, dossier_msgs, headings, rows, allow_delete=True)
    return True


def _validate_new_dossier(dossier_id, dossier_msgs, headings, rows):
    # New dossiers require additional columns to the `ID` column.
    # If we encounter this we rather immediately raise to avoid complex
    # communication.
    _raise_for_missing_columns(
        headings, *[col_name.upper() for col_name in REQUIRED_COLUMNS]
    )
    valid = True
    # check that status is not empty and also valid
    status = get_dossier_cell_by_column(dossier_id, "status", rows)
    if not status:
        messages.append_or_update_dossier_message(
            dossier_id=dossier_id,
            field_name="STATUS",
            detail=None,
            code=MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
            messages=dossier_msgs,
            level=messages.Severity.ERROR.value,
        )
        valid = False
    elif status not in [e.value for e in TargetStatus]:
        messages.append_or_update_dossier_message(
            dossier_id=dossier_id,
            field_name="STATUS",
            detail=status,
            code=MessageCodes.STATUS_CHOICE_VALIDATION_ERROR.value,
            messages=dossier_msgs,
            level=messages.Severity.ERROR.value,
        )
        valid = False

    # check submit date exists in newly imported dossiers
    if not get_dossier_cell_by_column(dossier_id, "submit-date", rows):
        messages.append_or_update_dossier_message(
            dossier_id=dossier_id,
            field_name="SUBMIT-DATE",
            detail=None,
            code=MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value,
            messages=dossier_msgs,
            level=messages.Severity.ERROR.value,
        )
        valid = False
    valid = _validate_date_fields(
        dossier_id, dossier_msgs, headings, rows, allow_delete=False
    )
    return valid


def _raise_for_missing_columns(headings, *columns):
    if any((missing_columns := [col for col in columns if col not in headings])):
        raise InvalidImportDataError(
            _(
                "Meta data file in archive is missing required columns %(missing)s. Required columns %(required)s"
            )
            % dict(
                required=", ".join(columns),
                missing=", ".join([col for col in missing_columns]),
            )
        )


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

    archive = dossier_import.get_archive()
    data_file = archive.open("dossiers.xlsx")

    try:
        headings, rows = get_worksheet_headings_and_rows(data_file)
    except zipfile.BadZipfile:
        raise InvalidImportDataError(
            _("Meta data file in archive is corrupt or not a valid .xlsx file.")
        )

    if extra := set(headings) - set([e.value for e in XlsxFileDossierLoader.Column]):
        sorted_missing_columns = [str(x) for x in (extra - set(["None", None]))]
        dossier_import.messages["validation"]["summary"]["warning"].append(
            _("Found unknown columns which will be ignored while importing:\n%(extra)s")
            % dict(extra="\n".join(sorted_missing_columns))
        )

    # collect all messages for every dossier in a list
    dossier_msgs = []

    _raise_for_missing_columns(headings, "ID")

    # get the list of IDs in the file
    dossier_ids = [row["ID"] for row in rows if row.get("ID")]

    # exclude and report duplicate IDs
    dupes = set([d for d in dossier_ids if dossier_ids.count(d) > 1])
    for dupe in dupes:
        messages.append_or_update_dossier_message(
            dossier_id=dupe,
            field_name="ID",
            detail=_("%(count)d rows with this ID will be ignored.")
            % {"count": dossier_ids.count(dupe)},
            code=MessageCodes.DUPLICATE_IDENTFIER_ERROR.value,
            messages=dossier_msgs,
        )
        dossier_ids.remove(dupe)

    # Each dossier ID may be discarded for various reasons and based on
    # different criteria depending on the import status as a new or reimported
    # dossier.
    valid_dossier_ids = []
    existing_dossier_ids = set(writer.get_existing_dossier_ids(dossier_ids))
    new_dossier_ids = set(dossier_ids) - existing_dossier_ids

    for dossier_id in new_dossier_ids:
        valid = _validate_new_dossier(dossier_id, dossier_msgs, headings, rows)
        if valid:
            valid_dossier_ids.append(dossier_id)

    for dossier_id in existing_dossier_ids:
        valid = _validate_existing_dossier(
            dossier_id,
            dossier_msgs,
            headings,
            rows,
        )
        if valid:
            valid_dossier_ids.append(dossier_id)

    # handle messages collected while validating the rows for the details
    # section.
    for msg in dossier_msgs:
        messages.update_messages_section_detail(
            message=msg, section="validation", dossier_import=dossier_import
        )

    dossier_import = messages.update_summary(dossier_import)
    dossier_import.messages["validation"]["summary"]["warning"] += validate_attachments(
        archive, valid_dossier_ids
    )
    dossier_import.messages["validation"]["summary"]["stats"] = {
        "attachments": get_attachment_validation_stats(archive, dossier_ids),
        "dossiers": len(valid_dossier_ids),
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
