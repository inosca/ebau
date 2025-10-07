from camac.settings.ebau_schema import ModuleConfig
from camac.settings.modules.work_item_list_schema import (
    AnnotationsConfig,
    WorkItemListConfig,
)

WORK_ITEM_LIST = ModuleConfig[WorkItemListConfig](
    default=WorkItemListConfig(),
    kt_ag=WorkItemListConfig(
        enabled=True,
        available_tasks_include_count=True,
        available_tasks_include_templates=True,
        available_tasks_for_role={
            "municipality": [
                "formal-exam",
                "publication",
                "information-of-neighbors",
                "init-distribution",
                "check-inquiries",
                "decision",
                "check-distribution",
                "init-construction-monitoring",
                "withdrawal-check",
            ],
            "service": ["inquiry", "check-inquiries"],
            "subservice": ["inquiry"],
        },
        available_tasks_for_service_group={
            "service-afb": [
                "check-pa",
                "cantonal-exam",
                "check-document-supplement",
                "trigger-billing",
            ],
        },
    ),
    kt_so=WorkItemListConfig(
        enabled=True,
        annotations=AnnotationsConfig(
            description="umschreibung-bauprojekt",
            applicants=None,
        ),
    ),
    kt_gr=WorkItemListConfig(
        enabled=True,
        available_tasks_for_role={
            "municipality": [
                "formal-exam",
                "publication",
                "init-distribution",
                "check-inquiries",
                "decision",
                "construction-acceptance",
            ],
            "service": ["inquiry", "check-inquiries", "check-additional-demand"],
            "subservice": ["inquiry"],
            "uso": ["inquiry"],
        },
    ),
)
