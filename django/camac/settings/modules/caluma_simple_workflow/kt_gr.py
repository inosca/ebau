from django.utils.translation import gettext_lazy as _

from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
    NotificationConfig,
)
from camac.timelines.utils import is_additional_demand_with_changes
from camac.utils import (
    should_notify_on_manual_workitems,
)

GR_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
    enabled=True,
    events={
        "formal-exam": {
            "completed": [
                EventConfig(
                    next_instance_state="init-distribution",
                    history_text=_("Preliminary exam performed"),
                    ech_event="camac.ech0211.signals.exam_completed",
                ),
            ],
        },
        "init-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="circulation",
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
                    history_text=_("Additional demand sent"),
                    notifications=[
                        NotificationConfig(
                            template_slug="send-additional-demand-public",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
                EventConfig(
                    condition=lambda work_item: (
                        not is_additional_demand_with_changes(work_item)
                    ),
                    notifications=[
                        NotificationConfig(
                            template_slug="send-additional-demand-internal",
                            recipient_types=["additional_demand_send_gr"],
                        ),
                    ],
                ),
                EventConfig(
                    condition=lambda work_item: is_additional_demand_with_changes(
                        work_item
                    ),
                    notifications=[
                        NotificationConfig(
                            template_slug="send-additional-demand-internal-with-changes",
                            recipient_types=["additional_demand_send_gr"],
                        ),
                    ],
                ),
            ],
        },
        "fill-additional-demand": {
            "completed": [
                EventConfig(
                    history_text=_("Additional demand was answered"),
                    ech_event="camac.ech0211.signals.file_subsequently",
                    notifications=[
                        NotificationConfig(
                            template_slug="fill-additional-demand",
                            recipient_types=[
                                "additional_demand_reply_gr",
                                "work_item_controlling",
                            ],
                        ),
                    ],
                ),
            ],
        },
        "construction-acceptance": {
            "completed": [
                EventConfig(
                    history_text=_("Construction monitoring performed"),
                ),
            ],
        },
        "complete-construction-monitoring": {
            "completed": [
                EventConfig(
                    history_text=_("Construction monitoring performed"),
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
                        work_item, True
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
    },
)
