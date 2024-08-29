"""WARNING: Any key that is either "TASK or ends with "_TASK" will be picked up by the visibilty filter for work items (see django/camac/extensions/visibilities.py)."""

CONSTRUCTION_MONITORING = {
    "default": {
        "INIT_CONSTRUCTION_MONITORING_TASK": "init-construction-monitoring",
        "CONSTRUCTION_STAGE_WORKFLOW": "construction-stage",
        "CONSTRUCTION_STAGE_TASK": "construction-stage",
        "COMPLETE_CONSTRUCTION_MONITORING_TASK": "complete-construction-monitoring",
        "COMPLETE_INSTANCE_TASK": "complete-instance",
        "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK": "construction-step-plan-construction-stage",
        "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_FORM": "construction-step-plan-construction-stage",
        "CONSTRUCTION_STEP_PLAN_SCHLUSSABNAHME_PROJEKT_TASK": "construction-step-schlussabnahme-projekt-planen",
    },
    "kt_schwyz": {
        "ENABLED": True,
        "PREVIOUS_INSTANCE_STATE": "done",
        "CONSTRUCTION_MONITORING_INSTANCE_STATE": "construction-monitoring",
        "ALLOW_FORMS": [
            "baugesuch-reklamegesuch",
            "projektanderung",
            "technische-bewilligung",
            "baumeldung-fur-geringfugiges-vorhaben",
        ],
        "NOTIFICATIONS": {
            # construction-step tasks/workflow: notification config
            "construction-step-baufreigabe": [
                {
                    "template_slug": "complete-construction-step-baufreigabe",
                    "recipient_types": ["involved_in_construction_step"],
                }
            ],
            "construction-step-schnurgeruest-kontrollieren": [
                {
                    "template_slug": "complete-construction-step-schnurgeruestabnahme",
                    "recipient_types": ["involved_in_construction_step"],
                }
            ],
            "construction-stage": [
                {
                    "template_slug": "complete-construction-step-schlussabnahme",
                    "recipient_types": [
                        "involved_in_construction_step",
                        # TODO: "localized_geometer"
                        # Always send notification regardless of involvement (?)
                    ],
                },
            ],
            "complete-instance": [
                {
                    "template_slug": "notify-complete-instance",
                    "recipient_types": [
                        "involved_in_construction_step",
                        # TODO: "localized_geometer"
                        # Always send notification regardless of involvement (?)
                    ],
                },
            ],
        },
        "NOTIFICATION_RECIPIENTS": {
            "construction-step-baufreigabe": [
                # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                {
                    "service_id": 10,
                    "require_involvement": True,
                },
                # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
                {
                    "service_id": 79,
                    "require_involvement": True,
                },
            ],
            "construction-step-schnurgeruest-kontrollieren": [
                # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                {
                    "service_id": 10,
                    "require_involvement": True,
                },
                # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
                {
                    "service_id": 79,
                    "require_involvement": True,
                },
            ],
            "construction-stage": [
                # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                {
                    "service_id": 10,
                    "require_involvement": True,
                },
                # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
                {
                    "service_id": 79,
                    "require_involvement": True,
                },
                # Amt für Arbeit
                {"service_id": 4, "require_involvement": True},
                # Laboratorium der Urkantone
                {
                    "service_id": 22,
                    "require_involvement": True,
                },
                # TODO: Amt für Finanzen (Gebäudeschatzer)?
                # Always send notification regardless of involvement
            ],
            "complete-instance": [
                # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                {
                    "service_id": 10,
                    "require_involvement": True,
                },
                # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
                {
                    "service_id": 79,
                    "require_involvement": True,
                },
                # Amt für Arbeit # Nur involviert in Zirkulation
                {
                    "service_id": 4,
                    "require_involvement": True,
                },
                # Laboratorium der Urkantone
                {
                    "service_id": 22,
                    "require_involvement": True,
                },
                # TODO: Amt für Finanzen (Gebäudeschatzer)?
                # Always send notification regardless of involvement
            ],
        },
    },
    "kt_uri": {
        "ENABLED": True,
        "CONSTRUCTION_CONTROL_TASK": "construction-control",
        "PREVIOUS_INSTANCE_STATE": "done",
        "AFTER_INSTANCE_STATE": "arch",
        "CONSTRUCTION_MONITORING_INSTANCE_STATE": "control",
        "NOTIFICATIONS": {},
        "NOTIFICATION_RECIPIENTS": {},
    },
    "kt_so": {
        "ENABLED": True,
        "PREVIOUS_INSTANCE_STATE": "decided",
        "CONSTRUCTION_MONITORING_INSTANCE_STATE": "construction-monitoring",
        "NOTIFICATIONS": {},
        "NOTIFICATION_RECIPIENTS": {},
    },
    "demo": {
        "ENABLED": True,
    },
}
