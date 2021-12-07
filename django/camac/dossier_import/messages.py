from dataclasses import dataclass, field
from enum import Enum
from typing import List, Union

from dataclasses_json import dataclass_json
from django.utils.translation import gettext as _
from rest_framework import exceptions

from camac.document.models import Attachment
from camac.instance.models import Instance


@dataclass_json
@dataclass(order=True)
class Message:
    level: int
    code: str
    detail: Union[list, str, dict]


@dataclass_json
@dataclass
class FieldValidationMessage(Message):
    field: str


@dataclass_json
@dataclass
class DossierMessage:
    status: str  # one of success, warning, error
    dossier_id: str
    details: List[Message]


@dataclass_json
@dataclass
class Summary:
    stats: dict = field(default_factory=dict)
    warning: dict = field(default_factory=list)
    error: dict = field(default_factory=list)


LOG_LEVEL_DEBUG = 0
LOG_LEVEL_INFO = 1
LOG_LEVEL_WARNING = 2
LOG_LEVEL_ERROR = 3

# import status categories
DOSSIER_IMPORT_STATUS_SUCCESS = "success"
DOSSIER_IMPORT_STATUS_WARNING = "warning"
DOSSIER_IMPORT_STATUS_ERROR = "error"


class MessageCodes(str, Enum):
    """Message codes that are used for identifying messages.

    NOTE: Only codes listed here are included in summary reports.

    These listed here are for convenience and uniformity.

    Loaders may have further message codes that are dynamically
    constructed on field validation. E. g.:
     - "submit-date-validation-error" for Dossier.submit_date

    """

    # success
    INSTANCE_CREATED = "instance-created"
    FORM_DATA_WRITTEN = "form-data-written"
    ATTACHMENTS_WRITTEN = "attachments-written"
    SET_WORKFLOW_STATE = "workflow-state-set"

    # warnings
    DUPLICATE_DOSSIER = "duplicate-dossier"
    DATE_FIELD_VALIDATION_ERROR = "date-field-validation-error"
    STATUS_CHOICE_VALIDATION_ERROR = "status-choice-validation-error"
    MISSING_REQUIRED_VALUE_ERROR = "missing-required-field-error"
    DUPLICATE_IDENTFIER_ERROR = "duplicate-identifier-error"
    FIELD_VALIDATION_ERROR = "field-validation-error"
    MIME_TYPE_UNKNOWN = "mime-type-unknown"
    WORKFLOW_SKIP_ITEM_FAILED = "skip-workitem-failed"  # not user-facing


class MissingArchiveFileError(exceptions.ValidationError):
    default_code = "archive_file_missing"
    default_detail = _("To start an import please upload a file.")


class MissingMetadataFileError(exceptions.ValidationError):
    default_code = "metadata_file_missing"
    default_detail = _("No metadata file 'dossiers.xlsx' found in uploaded archive.")


class InvalidZipFileError(exceptions.ValidationError):
    default_code = "invalid_zip_file"


class MissingRequiredLocationError(exceptions.ValidationError):
    default_code = "required-location-missing"


class BadMimeType(exceptions.ParseError):
    default_code = "bad_mimetype"
    default_code = _(
        "Invalid mime type for dossier import archive. Allowed types are: zip"
    )


class BadXlsxFileError(exceptions.ParseError):
    default_code = "bad_xlsx_file"
    default_detail = _("Metadata file `dossiers.xlsx` is not a valid .xlsx file.")


def get_message_max_level(message_list: List[Message], default=LOG_LEVEL_DEBUG):
    return (
        message_list
        and max(
            list(sorted(message_list, key=lambda msg: msg.level, reverse=True))
        ).level
    ) or default


def aggregate_messages_by_level(message_object: dict, level: str) -> list:
    """Filter messages field section by message status.

    Message object is a dict:
    {
        "details": [
            {
                "dossier_id": 123,
                "status": "warning",
                "details": [
                    {
                        "code": "date-field-validation-error",
                        "detail": "not a date",
                        "field": "SUBMIT-DATE",
                        "level": 2,  # warning
                    }
                ]
            }
        ]
    }
    """
    result = []
    if message_object:
        for code in MessageCodes:
            filtered_summaries = []
            for dossier_detail in message_object["details"]:
                messages = list(
                    filter(
                        lambda x: x["level"] == level and x["code"] == code.value,
                        dossier_detail["details"],
                    )
                )
                if messages:
                    filtered_summaries.append(
                        {
                            "dossier_id": dossier_detail["dossier_id"],
                            "messages": messages,
                        }
                    )

            if filtered_summaries:
                result.append(compile_message_for_code(code, filtered_summaries))
    return result


def compile_message_for_code(code, filtered_summaries):
    """Return a formatted message for a given error code.

    Filtered messages is list of dictionaries:
    [{
      "dossier_id": 123,
      "messages": [
        "code": "date-field-validation-error",
        "detail": "not a date",
        "field": "SUBMIT-DATE",
        "level": 2,  # warning
      ]
    }]
    """
    messages = {
        MessageCodes.DUPLICATE_DOSSIER.value: "have the same ID",
        MessageCodes.DATE_FIELD_VALIDATION_ERROR.value: 'have an invalid value in date field. Please use the format "DD.MM.YYYY" (e.g. "13.04.2021")',
        MessageCodes.STATUS_CHOICE_VALIDATION_ERROR.value: "have an invalid status",
        MessageCodes.MISSING_REQUIRED_VALUE_ERROR.value: "miss a value in a required field",
        MessageCodes.DUPLICATE_IDENTFIER_ERROR.value: "have the same ID",
        MessageCodes.FIELD_VALIDATION_ERROR.value: "have an invalid value",
        MessageCodes.MIME_TYPE_UNKNOWN.value: "have at least one document with an unknown file type",
    }

    def format_summary(summary: dict) -> str:
        return "{dossier_id}: {entries}".format(
            dossier_id=summary["dossier_id"],
            entries=", ".join(
                [
                    f"'{message['detail']}' ({message.get('field')})"
                    if message["detail"]
                    else message.get("field")
                    for message in summary["messages"]
                ]
            ),
        )

    entries = [format_summary(summary) for summary in filtered_summaries]

    return _("{count} dossiers {message}. Affected dossiers:{entries}").format(
        count=len(filtered_summaries),
        message=messages[code],
        entries="\n" + ", ".join(entries),
    )


def update_summary(dossier_import):
    validation_message_object = dossier_import.messages.get("validation")
    if validation_message_object:
        data = dict(
            warning=aggregate_messages_by_level(
                validation_message_object, LOG_LEVEL_WARNING
            ),
            error=aggregate_messages_by_level(
                validation_message_object, LOG_LEVEL_ERROR
            ),
        )
        if not validation_message_object.get("summary"):  # pragma: no cover
            validation_message_object["summary"] = Summary().to_dict()
        validation_message_object["summary"].update(data)
        dossier_import.messages["validation"] = validation_message_object
        dossier_import.save()

    import_message_object = dossier_import.messages.get("import")
    if import_message_object:
        data = dict(
            warning=aggregate_messages_by_level(
                import_message_object, LOG_LEVEL_WARNING
            ),
            error=aggregate_messages_by_level(import_message_object, LOG_LEVEL_ERROR),
        )
        if not import_message_object.get("summary"):
            import_message_object["summary"] = Summary().to_dict()
        import_message_object["summary"].update(data)
        import_message_object["summary"]["stats"].update(
            {
                "dossiers": Instance.objects.filter(
                    **{"case__meta__import-id": str(dossier_import.pk)}
                ).count(),
                "documents": Attachment.objects.filter(
                    **{"instance__case__meta__import-id": str(dossier_import.pk)}
                ).count(),
            }
        )
        dossier_import.messages["import"] = import_message_object
        dossier_import.save()
    return dossier_import


def append_or_update_dossier_message(
    dossier_id, field_name, detail, code, messages, level=LOG_LEVEL_WARNING
):
    dossier_msg = next(
        (d for d in messages if d.dossier_id == dossier_id),
        None,
    )
    if not dossier_msg:
        dossier_msg = DossierMessage(
            status=DOSSIER_IMPORT_STATUS_ERROR,
            details=[],
            dossier_id=dossier_id,
        )
        messages.append(dossier_msg)
    dossier_msg.details.append(
        FieldValidationMessage(
            code=code,
            level=level,
            field=field_name,
            detail=detail,
        )
    )


def update_messages_section_detail(message: DossierMessage, dossier_import, section):
    """Update DossierImport.messages with dossier message detail.

    This is to avoid overwriting previous messages on the current dossier with new
    messages.

    message is an instance of DossierMessage.

    dossier_import is an instance of DossierImport

    section: str, one of "validation" or "import"

    Input message is transformed to dictionary that can be saved to the DossierImport.messages
    field
    """
    if section not in ["validation", "import"]:  # pragma: no cover
        raise ValueError(f"`section` must be one of {', '.join(section)}.")
    message_exists = next(
        (
            d
            for d in dossier_import.messages[section]["details"]
            if d["dossier_id"] == message.dossier_id
        ),
        None,
    )
    if not message_exists:
        message_exists = message.to_dict()
        dossier_import.messages["validation"]["details"].append(message_exists)
    message_exists.update(message.to_dict())


def default_messages_object():
    return {
        "import": {"details": [], "summary": Summary().to_dict(), "completed": None},
        "validation": {
            "details": [],
            "summary": Summary().to_dict(),
            "completed": None,
        },
    }
