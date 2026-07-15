from django.utils.translation import gettext_lazy as _

from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
    NotificationConfig,
)
from camac.utils import (
    should_notify_on_manual_workitems,
)

BE_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
    enabled=True,
    events={
        "init-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="circulation",
                    history_text=_("Circulation started"),
                    ech_event="camac.ech0211.signals.circulation_started",
                    notifications=[
                        NotificationConfig(
                            template_slug="03-verfahrensablauf-gesuchsteller",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "complete-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="coordination",
                    ech_event="camac.ech0211.signals.circulation_ended",
                    notifications=[
                        NotificationConfig(
                            template_slug="03-verfahren-vorzeitig-beendet",
                            recipient_types=["unanswered_inquiries"],
                        ),
                    ],
                ),
            ],
        },
        "send-additional-demand": {
            "completed": [
                EventConfig(
                    history_text=_("Additional demand sent"),
                    notifications=[
                        NotificationConfig(
                            template_slug="send-additional-demand-applicant",
                            recipient_types=["applicant"],
                        ),
                        NotificationConfig(
                            template_slug="03-zusaetzliche-unterlagen-notwendig-gemeinde",
                            recipient_types=["inactive_municipality"],
                        ),
                    ],
                ),
            ],
        },
        "fill-additional-demand": {
            "completed": [
                EventConfig(
                    history_text=_("Additional demand was answered"),
                    notifications=[
                        NotificationConfig(
                            template_slug="03-nachforderung-beantwortet-leitbehorde",
                            recipient_types=["leitbehoerde", "inactive_municipality"],
                        ),
                    ],
                ),
            ],
        },
        "complete": {
            "completed": [
                EventConfig(
                    next_instance_state="finished",
                    history_text=_("Procedure completed"),
                    ech_event="camac.ech0211.signals.finished",
                ),
            ],
        },
        "cadastral-survey": {
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="complete-cadastral-survey",
                            recipient_types=["work_item_controlling"],
                        ),
                    ],
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
        },
    },
)
