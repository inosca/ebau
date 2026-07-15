from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
    NotificationConfig,
)

SZ_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
    enabled=True,
    events={
        "formal-addition": {
            "completed": [
                EventConfig(
                    next_instance_state="subm",
                ),
            ],
        },
        "complete-check": {
            "completed": [
                EventConfig(
                    next_instance_state="comm",
                    history_text="Dossier angenommen",
                    notifications=[
                        NotificationConfig(
                            template_slug="bewilligungsprozess-gestartet",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "reject-form": {
            "completed": [
                EventConfig(
                    next_instance_state="rejected",
                    history_text="Dossier zurückgewiesen",
                    notifications=[
                        NotificationConfig(
                            template_slug="ruckweisung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "make-decision": {
            "completed": [
                EventConfig(
                    next_instance_state="done",
                    history_text="Bewilligung erteilt",
                    notifications=[
                        NotificationConfig(
                            template_slug="complete-make-decision",
                            recipient_types=["geometer", "tax_administration"],
                        ),
                    ],
                ),
            ],
        },
        "archive-instance": {
            "completed": [
                EventConfig(
                    next_instance_state="arch",
                    history_text="Dossier archiviert",
                ),
            ],
        },
        "depreciate-case": {
            "completed": [
                EventConfig(
                    next_instance_state="stopped",
                    history_text="Dossier abgeschrieben",
                ),
            ],
        },
        "additional-demand": {
            "completed": [
                EventConfig(
                    next_instance_state="nfd",
                    history_text="Nachforderung gestartet",
                    notifications=[
                        NotificationConfig(
                            template_slug="nachforderung",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "init-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="circ",
                    history_text="Zirkulation gestartet",
                ),
            ],
        },
        "complete-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="redac",
                ),
            ],
        },
        "complete-instance": {
            "completed": [
                EventConfig(
                    next_instance_state="instance-completed",
                    history_text="Verfahren abgeschlossen",
                ),
            ],
        },
        "construction-step-baufreigabe-beantragen": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="construction-step-notify-baufreigabe-beantragen",
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
                            template_slug="construction-step-notify-baufreigabe",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-baubeginn-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="construction-step-notify-baubeginn-melden",
                            recipient_types=["applicant"],
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
                            template_slug="construction-step-notify-kanalisationsabnahme-melden",
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
                            template_slug="construction-step-notify-kanalisation-kontrollieren",
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
                            template_slug="construction-step-notify-schnurgeruestabnahme-melden",
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
                            template_slug="construction-step-notify-schnurgeruestabnahme-planen",
                            recipient_types=["leitbehoerde"],
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
                            template_slug="construction-step-notify-rohbauabnahme-melden",
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
                            template_slug="construction-step-notify-rohbau-kontrollieren",
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
                            template_slug="construction-step-notify-zwischenkontrolle-melden",
                            recipient_types=["applicant"],
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
                            template_slug="construction-step-notify-zwischenkontrolle",
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
                            template_slug="construction-step-notify-schlussabnahme-gebaeude-melden",
                            recipient_types=["applicant"],
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
                            template_slug="construction-step-notify-schlussabnahme-gebaeude",
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
                            template_slug="construction-step-notify-schlussabnahme-projekt-melden",
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
                            template_slug="construction-step-notify-schlussabnahme-projekt-planen",
                            recipient_types=["leitbehoerde"],
                        ),
                    ],
                ),
            ],
        },
    },
)
