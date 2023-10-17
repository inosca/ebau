from django.utils.translation import gettext_lazy as _

ADDITIONAL_DEMAND = {
    "default": {
        "WORKFLOW": "additional-demand",
        "TASK": "additional-demand",
        "CREATE_TASK": "init-additional-demand",
        "FILL_TASK": "fill-additional-demand",
        "CHECK_TASK": "check-additional-demand",
        "SEND_TASK": "send-additional-demand",
        "DECISION_QUESTION": "additional-demand-decision",
        "DECISION_REJECT": "additional-demand-decision-reject",
        "CHECK_NOTIFICATON": {
            "additional-demand-decision-reject": {
                "notification_recipients": ["applicant"],
                "history_text": _("Additional demand rejected"),
            },
            "additional-demand-decision-accept": {
                "notification_recipients": ["additional_demand_inviter"],
                "history_text": _("Additional demand accepted"),
            },
        },
    },
    "kt_gr": {
        "ENABLED": True,
    },
    "kt_so": {
        "ENABLED": True,
    },
}
