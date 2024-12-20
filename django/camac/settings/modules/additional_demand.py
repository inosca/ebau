from django.utils.translation import gettext_lazy as _

"""
WARNING: Any key that is either "TASK or ends with "_TASK" will be picked up by the visibilty filter for work items (see django/camac/extensions/visibilities.py).
"""
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
                    "template_slug": "nachforderung-akzeptiert-bauherrschaft",
                },
                {
                    "recipient_types": ["leitbehoerde"],
                    "template_slug": "nachforderung-akzeptiert-gemeinde",
                },
            ],
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "nachforderung-abgelehnt",
                }
            ],
        },
    },
    "kt_uri": {
        "ENABLED": True,
        "ALLOW_SUBSERVICES": True,
        "STATES": {
            "PENDING_ADDITIONAL_DEMANDS": "nfd",
        },
        "NOTIFICATIONS": {
            "ACCEPTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "2-3-nachforderung-akzeptiert",
                }
            ],
            "REJECTED": [
                {
                    "recipient_types": ["applicant"],
                    "template_slug": "2-5-nachforderung-abgelehnt",
                }
            ],
        },
    },
}
