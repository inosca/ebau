import copy
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional, Union

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
class FormattedListMessage(Message):
    data: list


@dataclass_json
@dataclass
class DossierMessage:
    status: str  # one of success, warning, error
    dossier_id: str
    details: List[Message]
    instance_id: Optional[int] = None


@dataclass_json
@dataclass
class Summary:
    dossiers_written: int = 0
    dossiers_success: int = 0
    num_documents: int = 0
    dossiers_warning: dict = field(default_factory=dict)
    dossiers_error: dict = field(default_factory=dict)
    warnings: list = field(default_factory=list)
    errors: list = field(default_factory=list)


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

    INSTANCE_CREATED = "instance-created"
    DUPLICATE_DOSSIER = "duplicate-dossier"
    REQUIRED_VALUES_MISSING = "dossier-missing-required-values"
    FORM_DATA_WRITTEN = "form-data-written"
    ATTACHMENTS = "attach-documents"
    WORKFLOW = "set-workflow"
    WORKFLOW_SKIP_ITEM_FAILED = "skip-workitem-failed"
    SET_WORKFLOW_STATE = "workflow-state-set"
    FIELD_VALIDATION_ERROR = "field-validation-error"


class MissingArchiveFileError(exceptions.ValidationError):
    default_code = "archive_file_missing"
    default_detail = _("To start an import please upload a file.")


class MissingMetadataFileError(exceptions.ValidationError):
    default_code = "metadata_file_missing"
    default_detail = _("No metadata file 'dossiers.xlsx' found in uploaded archive.")


class InvalidZipFileError(exceptions.ValidationError):
    default_code = "invalid_zip_file"


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


def categorize_messages_by_level(dossier_summary_list: list, level: str) -> dict:
    """Filter messages field section by message status.

    available status values: 'success', 'warning', 'error'

    step_summary is the a dictionary of the form
        {
            'summary': Summary,
            'details': List[dossier-summary-dict]
        }

    """
    categorized = {}
    if dossier_summary_list:
        for code in MessageCodes:
            messages_by_category = FormattedListMessage(
                code=code.value, level=level, detail=[], data=[]
            )
            for dossier_detail in dossier_summary_list["details"]:
                messages = list(
                    filter(
                        lambda x: x["level"] == level and x["code"] == code.value,
                        dossier_detail["details"],
                    )
                )
                if messages:
                    filtered = copy.deepcopy(dossier_detail)
                    filtered["details"] = messages
                    messages_by_category.detail.append(filtered)
                    messages_by_category.data.append(filtered["dossier_id"])
            if messages_by_category.data:
                categorized[code.value] = messages_by_category.to_dict()
    return categorized


def update_summary(dossier_import):
    validation_messages = dossier_import.messages.get("validation")
    if validation_messages:
        data = dict(
            dossiers_warning=categorize_messages_by_level(
                validation_messages, LOG_LEVEL_WARNING
            ),
            dossiers_error=categorize_messages_by_level(
                validation_messages, LOG_LEVEL_ERROR
            ),
            dossiers_written=Instance.objects.filter(
                **{"case__meta__import-id": str(dossier_import.pk)}
            ).count(),
        )
        if not validation_messages.get("summary"):  # pragma: no cover
            validation_messages["summary"] = Summary().to_dict()
        validation_messages["summary"].update(data)
        dossier_import.messages["validation"] = validation_messages
        dossier_import.save()

    import_messages = dossier_import.messages.get("import")
    if import_messages:
        data = dict(
            dossiers_success=len(
                list(
                    filter(
                        lambda i: i["status"] == DOSSIER_IMPORT_STATUS_SUCCESS,
                        import_messages["details"],
                    )
                )
            ),
            dossiers_warning=categorize_messages_by_level(
                import_messages, LOG_LEVEL_WARNING
            ),
            dossiers_error=categorize_messages_by_level(
                import_messages, LOG_LEVEL_ERROR
            ),
            dossiers_written=Instance.objects.filter(
                **{"case__meta__import-id": str(dossier_import.pk)}
            ).count(),
            num_documents=Attachment.objects.filter(
                **{"instance__case__meta__import-id": str(dossier_import.pk)}
            ).count(),
        )
        if not import_messages.get("summary"):
            import_messages["summary"] = Summary().to_dict()
        import_messages["summary"].update(data)
        dossier_import.messages["import"] = import_messages
        dossier_import.save()
    return dossier_import


def append_or_update_dossier_message(dossier_id, field_name, detail, messages):
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
            code=MessageCodes.FIELD_VALIDATION_ERROR.value,
            level=LOG_LEVEL_WARNING,
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
        "import": {"details": [], "summary": Summary().to_dict()},
        "validation": {"details": [], "summary": Summary().to_dict()},
    }
