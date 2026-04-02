from django.utils.translation import gettext_lazy as _

from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.statistics_schema import (
    ExportColumnsConfig,
    StatisticsConfig,
)

DEFAULT_DOSSIER_COLUMNS = [
    ("dossier_number", _("Instance number")),
    ("form_name", _("Application Type")),
    ("parcels", _("Parcels")),
    ("submit_date", _("Submission Date")),
    ("responsible_user", _("Responsible")),
    ("municipality", _("Municipality")),
]

DEFAULT_WORK_ITEM_COLUMNS = [
    ("task_name", _("Task name")),
    ("wi_created_at", _("Created at")),
    ("wi_deadline", _("Deadline")),
    ("wi_closed_at", _("Closed at")),
    ("wi_assigned_user", _("Assigned user")),
    ("wi_addressed_group", _("Addressed group")),
    ("wi_status", _("Status")),
    ("wi_processing_time", _("Processing time")),
    ("wi_on_time", _("On time")),
]

AG_SERVICE_COLUMN_CONFIG = ExportColumnsConfig(
    dossiers=[
        *DEFAULT_DOSSIER_COLUMNS,
        ("processing_time", _("Processing time")),
        ("first_inquiry_date", _("First inquiry date")),
        ("completing_date", _("Completing date")),
        ("on_time", _("On time")),
    ],
    work_items=[
        *DEFAULT_DOSSIER_COLUMNS,
        *DEFAULT_WORK_ITEM_COLUMNS,
    ],
)

STATISTICS = ModuleConfig[StatisticsConfig](
    default=StatisticsConfig(
        enabled=False,
    ),
    kt_ag=StatisticsConfig(
        enabled=True,
        by_service_group={
            "service-afb": AG_SERVICE_COLUMN_CONFIG,
            "service-external": AG_SERVICE_COLUMN_CONFIG,
            "service-cantonal": AG_SERVICE_COLUMN_CONFIG,
            "municipality": ExportColumnsConfig(
                dossiers=[
                    *DEFAULT_DOSSIER_COLUMNS,
                    ("processing_time", _("Processing time")),
                ],
            ),
        },
    ),
)
