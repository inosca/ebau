from camac.settings.modules.caluma_simple_workflow_schema import (
    CalumaSimpleWorkflowConfig,
    EventConfig,
    NotificationConfig,
)
from camac.utils import (
    not_send_for_migrated_publications,
    send_only_for_einfache_anfrage,
)

UR_CALUMA_SIMPLE_WORKFLOW_SETTINGS = CalumaSimpleWorkflowConfig(
    enabled=True,
    events={
        "complete-check": {
            "completed": [
                EventConfig(
                    next_instance_state="comm",
                ),
            ],
        },
        "init-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="circ",
                    notifications=[
                        NotificationConfig(
                            template_slug="4-zirkulation-gestartet-gesuchsteller",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "complete-distribution": {
            "completed": [
                EventConfig(
                    next_instance_state="done",
                    notifications=[
                        NotificationConfig(
                            template_slug="4-3-zirkulation-abgeschlossen",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "decision": {
            "completed": [
                EventConfig(
                    next_instance_state="control",
                    notifications=[
                        NotificationConfig(
                            template_slug="5-eroeffnung-stellungnahme-vorentscheid",
                            recipient_types=["applicant"],
                        ),
                        NotificationConfig(
                            template_slug="5-11-eroeffnung-stellungnahme-vorentscheid-intern",
                            recipient_types=["involved_in_distribution"],
                        ),
                    ],
                ),
                EventConfig(
                    condition=lambda work_item: send_only_for_einfache_anfrage(
                        work_item
                    ),
                    notifications=[
                        NotificationConfig(
                            template_slug="5-eroeffnung-stellungnahme-vorentscheid",
                            recipient_types=["municipality_users"],
                        ),
                    ],
                ),
            ],
        },
        "send-additional-demand": {
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="2-1-nachforderung-eingegangen",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "fill-additional-demand": {
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="2-2-nachforderung-beantwortet",
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
                            template_slug="5-1-av-projektiert-pruefen",
                            recipient_types=["geometer_uri"],
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
                            template_slug="6-2-baubeginn-melden",
                            recipient_types=["applicant"],
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
                            template_slug="6-baufreigabe-beantragen",
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
                            template_slug="6-1-baufreigabe-entscheiden",
                            recipient_types=["work_item_addressed"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-gebaeudeabbruch-melden": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-21-gebaeudeabbruch",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-av-status-demolition": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-22-meldung-gebaeudeabbruch-av-pruefen",
                            recipient_types=["municipality_users", "geometer_uri"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-gwr-state-demolition": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-221-gwr-status-nachfuehren-gebaeudeabbruch",
                            recipient_types=["municipality_users"],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-gwr-state-construction-start": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-222-gwr-status-nachfuehren-baubeginn",
                            recipient_types=["municipality_users"],
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
                            template_slug="6-31-kanalisation-kontrollieren",
                            recipient_types=["abwasser_uri"],
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
                            template_slug="6-3-kanalisationsabnahme-melden",
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
                            template_slug="6-5-rohbauabnahme-melden",
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
                            template_slug="6-51-rohbaukontrolle-durchfuehren",
                            recipient_types=["work_item_addressed"],
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
                            template_slug="6-7-schlussabnahme-melden",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-72-meldung-bereit-zur-schlussabnahme-gebaeude",
                            recipient_types=["municipality_users"],
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
                            template_slug="6-73-meldung-bereit-zur-schlussabnahme-gesamtprojekt",
                            recipient_types=["applicant"],
                        ),
                    ],
                ),
            ],
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-71-schlussabnahme-projekt-melden",
                            recipient_types=["municipality_users"],
                        ),
                        NotificationConfig(
                            template_slug="7-1-av-definitiv-durchfuehren",
                            recipient_types=["geometer_uri"],
                        ),
                        NotificationConfig(
                            template_slug="7-11-av-definitiv-nachfuehren",
                            recipient_types=["applicant"],
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
                            template_slug="6-4-schnurgeruestabnahme-melden",
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
                            template_slug="6-41-schnurgeruestabnahme-planen",
                            recipient_types=["schnurgeruestabnahme_uri"],
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
                            template_slug="6-42-schnurgeruest-kontrollieren",
                            recipient_types=["municipality_users"],
                        ),
                    ],
                ),
            ],
        },
        "zs-ersatzbeitrag-pruefen": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="6-411-schnurgeruestabnahme-erfolgt",
                            recipient_types=["abm_zs_uri"],
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
                            template_slug="6-6-zwischenkontrolle-melden",
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
                            template_slug="6-61-zwischenkontrolle-durchfuehren",
                            recipient_types=["work_item_addressed"],
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
                            template_slug="7-bau-beendet",
                            recipient_types=[
                                "liegenschaftsschaetzung_uri",
                                "geometer_uri",
                            ],
                        ),
                    ],
                ),
            ],
        },
        "construction-step-schlussabnahme-projekt-planen": {
            "completed": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="7-2-einladung-endabnahme",
                            recipient_types=["invited_to_schlussabnahme_projekt"],
                        ),
                    ],
                ),
            ],
        },
        "liegenschaftsschaetzung": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="7-bau-beendet",
                            recipient_types=["liegenschaftsschaetzung_uri"],
                        ),
                        NotificationConfig(
                            template_slug="7-bau-beendet",
                            recipient_types=["fgs_uri"],
                        ),
                        NotificationConfig(
                            template_slug="7-bau-beendet",
                            recipient_types=["geometer_uri"],
                        ),
                    ],
                ),
            ],
        },
        "rpg": {
            "created": [
                EventConfig(
                    notifications=[
                        NotificationConfig(
                            template_slug="8-1-neue-aufgabe-rpg",
                            recipient_types=["koor_np_users"],
                        ),
                    ],
                ),
            ],
        },
        "fill-publication": {
            "completed": [
                EventConfig(
                    condition=lambda work_item: not_send_for_migrated_publications(
                        work_item
                    ),
                    notifications=[
                        NotificationConfig(
                            template_slug="9-nachricht-an-amtsblatt",
                            recipient_types=["amtsblatt_uri"],
                        ),
                    ],
                ),
            ],
        },
    },
)
