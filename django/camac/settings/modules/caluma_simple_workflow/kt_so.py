from django.utils.translation import gettext_lazy as _

from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
    NotificationConfig,
)
from camac.utils import (
    should_notify_on_manual_workitems,
)

SO_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
    enabled=True,
    events={
        "formal-exam": {
            "completed": [
                EventConfig(
                    next_instance_state="material-exam",
                    history_text=_("Formal exam performed"),
                ),
            ],
        },
        "material-exam": {
            "completed": [
                EventConfig(
                    next_instance_state="init-distribution",
                    history_text=_("Material exam performed"),
                    ech_event="camac.ech0211.signals.exam_completed",
                ),
            ],
        },
        "init-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="distribution",
                    history_text=_("Circulation started"),
                    ech_event="camac.ech0211.signals.circulation_started",
                ),
            ],
        },
        "complete-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="decision",
                    ech_event="camac.ech0211.signals.circulation_ended",
                ),
            ],
        },
        "send-additional-demand": {
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="nachforderung-neu",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "fill-additional-demand": {
            "completed": [
                EventConfig(
                    ech_event="camac.ech0211.signals.file_subsequently",
                    notifications=[
                        NotificationConfig(
                            template_slug="nachforderung-beantwortet",
                            recipient_types=["work_item_controlling"],
                        ),
                    ],
                ),
            ],
        },
        "complete-instance": {
            "completed": [
                EventConfig(
                    next_instance_state="finished",
                    history_text=_("Procedure completed"),
                    ech_event="camac.ech0211.signals.finished",
                ),
            ],
        },
        "create-manual-workitems": {
            "created": [
                EventConfig(
                    condition=lambda work_item: should_notify_on_manual_workitems(
                        work_item
                    ),
                    notifications=[
                        NotificationConfig(
                            template_slug="create-manual-work-item",
                            recipient_types=["work_item_addressed"],
                        ),
                    ],
                ),
            ],
            "completed": [
                EventConfig(
                    condition=lambda work_item: work_item.meta["notify-completed"],
                    notifications=[
                        NotificationConfig(
                            template_slug="complete-manual-work-item",
                            recipient_types=["work_item_controlling"],
                        ),
                    ],
                ),
            ],
        },
        "geometer": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="geometer-invited",
                            recipient_types=["work_item_addressed"],
                        ),
                    ],
                ),
            ],
        },
    },
)
