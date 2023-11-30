from django.utils.translation import gettext_lazy as _

ADDITIONAL_DEMAND = {
    "default": {
        "ALLOW_SUBSERVICES": False,
        "WORKFLOW": "additional-demand",
        "TASK": "additional-demand",
        "CREATE_TASK": "init-additional-demand",
        "FILL_TASK": "fill-additional-demand",
        "CHECK_TASK": "check-additional-demand",
        "SEND_TASK": "send-additional-demand",
        "QUESTIONS": {
            "DECISION": "additional-demand-decision",
        },
        "ANSWERS": {
            "DECISION": {
                "REJECTED": "additional-demand-decision-reject",
                "ACCEPTED": "additional-demand-decision-accept",
            }
        },
        "HISTORY_ENTRIES": {},
        "NOTIFICATIONS": {"ACCEPTED": [], "REJECTED": []},
    },
    "kt_gr": {
        "ENABLED": True,
        "HISTORY_ENTRIES": {
            "ACCEPTED": _("Additional demand accepted"),
            "REJECTED": _("Additional demand rejected"),
        },
        "NOTIFICATIONS": {
            "ACCEPTED": [
                {
                    "recipient_types": ["additional_demand_inviter"],
                    "template_slug": "additional-demand-decision-accept",
                }
            ],
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "additional-demand-decision-reject",
                }
            ],
        },
    },
    "kt_so": {
        "ENABLED": True,
        "ALLOW_SUBSERVICES": True,
        "NOTIFICATIONS": {
            "ACCEPTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "nachforderung-akzeptiert",
                }
            ],
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "nachforderung-abgelehnt",
                }
            ],
        },
    },
}
