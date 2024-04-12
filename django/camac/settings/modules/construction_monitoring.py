CONSTRUCTION_MONITORING = {
    "default": {
        "INIT_CONSTRUCTION_MONITORING_TASK": "init-construction-monitoring",
        "CONSTRUCTION_STAGE_WORKFLOW": "construction-stage",
        "CONSTRUCTION_STAGE_TASK": "construction-stage",
        "COMPLETE_CONSTRUCTION_MONITORING_TASK": "complete-construction-monitoring",
        "COMPLETE_INSTANCE_TASK": "complete-instance",
        "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK": "construction-step-plan-construction-stage",
        "CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_FORM": "construction-step-plan-construction-stage",
    },
    "kt_schwyz": {
        "ENABLED": True,
        "PREVIOUS_INSTANCE_STATE": "done",
        "CONSTRUCTION_MONITORING_INSTANCE_STATE": "construction-monitoring",
        "ALLOW_FORMS": [
            "baugesuch-reklamegesuch",
            "projektanderung",
            "technische-bewilligung",
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
                        # TODO: "localized_geometer",
                    ],
                },
            ],
            "complete-instance": [
                {
                    "template_slug": "notify-complete-instance",
                    "recipient_types": [
                        "involved_in_construction_step",
                        # TODO: "localized_geometer",
                    ],
                },
            ],
        },
        "NOTIFICATION_RECIPIENTS": {
            "construction-step-baufreigabe": [
                10,  # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                79,  # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
            ],
            "construction-step-schnurgeruest-kontrollieren": [
                10,  # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                79,  # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
            ],
            "construction-stage": [
                10,  # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                79,  # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
                4,  # Amt für Arbeit
                22,  # Laboratorium der Urkantone
                # TODO: Amt für Finanzen (Gebäudeschatzer)?
            ],
            "complete-instance": [
                10,  # Amt für Militär, Feuer- und Zivilschutz (Brandschutz)
                79,  # Amt für Militär, Feuer- und Zivilschutz (Schutzbauten)
                4,  # Amt für Arbeit
                22,  # Laboratorium der Urkantone
                # TODO: Amt für Finanzen (Gebäudeschatzer)?
            ],
        },
    },
    "kt_uri": {
        "ENABLED": True,
        "PREVIOUS_INSTANCE_STATE": "done",
        "CONSTRUCTION_MONITORING_INSTANCE_STATE": "control",
        "NOTIFICATIONS": {},
        "NOTIFICATION_RECIPIENTS": {},
    },
    "demo": {
        "ENABLED": True,
    },
}
