from django.utils.translation import gettext_lazy as _

from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
    NotificationConfig,
)

AG_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
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
                            template_slug="send-additional-demand",
                            recipient_types=["applicant", "additional_demand_inviter"],
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
                            template_slug="fill-additional-demand",
                            recipient_types=["work_item_controlling"],
                        ),
                    ],
                ),
            ],
        },
        "complete-construction-monitoring": {
            "completed": [
                EventConfig(
                    next_instance_state="to-finish",
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
        "construction-step-baubeginn-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-baufreigabe": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-baufreigabe-beantragen": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-kanalisation-kontrollieren": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-kanalisationsabnahme-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-rohbauabnahme-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-rohbau-kontrollieren": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schlussabnahme-gebaeude": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schlussabnahme-gebaeude-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schlussabnahme-projekt": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schlussabnahme-projekt-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schlussabnahme-projekt-planen": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schnurgeruestabnahme-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schnurgeruestabnahme-planen": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schnurgeruest-kontrollieren": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-zwischenkontrolle": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung-leitbehoerde",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-zwischenkontrolle-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="baubegleitung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
    },
)
