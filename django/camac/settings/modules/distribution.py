from datetime import timedelta

from django.utils.translation import gettext_lazy as _

from camac.utils import (
    has_permission_for_inquiry_answer_document,
    has_permission_for_inquiry_document,
    is_lead_role,
)

from .distribution_suggestions.kt_bern import BE_DISTRIBUTION_SUGGESIONS
from .distribution_suggestions.kt_gr import GR_DISTRIBUTION_SUGGESIONS
from .distribution_suggestions.kt_schwyz import SZ_DISTRIBUTION_SUGGESIONS
from .distribution_suggestions.kt_so import SO_DISTRIBUTION_SUGGESIONS
from .distribution_suggestions.kt_uri import UR_DISTRIBUTION_SUGGESIONS

"""
WARNING: Any key that is either "TASK or ends with "_TASK" will be picked up by the visibilty filter for work items (see django/camac/extensions/visibilities.py).
"""
DISTRIBUTION = {
    "default": {
        "DEFAULT_DEADLINE_LEAD_TIME": 30,  # 30 days, needs to be the same as configured in the frontend
        "DISTRIBUTION_WORKFLOW": "distribution",
        "DISTRIBUTION_TASK": "distribution",
        "DISTRIBUTION_INIT_TASK": "init-distribution",
        "DISTRIBUTION_COMPLETE_TASK": "complete-distribution",
        "DISTRIBUTION_CHECK_TASK": "check-distribution",
        "INQUIRY_TASK": "inquiry",
        "INQUIRY_FORM": "inquiry",
        "INQUIRY_CREATE_TASK": "create-inquiry",
        "INQUIRY_CHECK_TASK": "check-inquiries",
        "INQUIRY_REDO_TASK": "redo-inquiry",
        "INQUIRY_WORKFLOW": "inquiry",
        "INQUIRY_ANSWER_FORM": "inquiry-answer",
        "INQUIRY_ANSWER_FILL_TASK": "fill-inquiry",
        "HISTORY": {},
        "REDO_INQUIRY": {},
        "REDO_DISTRIBUTION": {},
        "QUESTIONS": {
            "DEADLINE": "inquiry-deadline",
            "REMARK": "inquiry-remark",
            "STATUS": "inquiry-answer-status",
        },
        "ANSWERS": {},
        "NOTIFICATIONS": {},
        # For the suggestions services ids or slugs can be used but they shouldn't be mixed.
        "SUGGESTIONS": [],
        "DEFAULT_SUGGESTIONS": [],
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "DISTRIBUTION_COMPLETE_TASK": lambda group, *_: is_lead_role(group),
                "DISTRIBUTION_CHECK_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_CHECK_TASK": lambda group, *_: is_lead_role(group),
            },
            "ResumeWorkItem": {
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "CancelWorkItem": {
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "RedoWorkItem": {
                "DISTRIBUTION_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_TASK": lambda group, *_: is_lead_role(group),
            },
            "SaveDocumentAnswer": {
                "INQUIRY_FORM": lambda group, document, *_: is_lead_role(group)
                and has_permission_for_inquiry_document(group, document),
                "INQUIRY_ANSWER_FORM": lambda group,
                document,
                *_: has_permission_for_inquiry_answer_document(group, document),
            },
        },
    },
    "kt_bern": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circulation",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-statement",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
        },
        "ANSWERS": {
            "STATUS": {
                "POSITIVE": "inquiry-answer-status-positive",
                "NEGATIVE": "inquiry-answer-status-negative",
                "NOT_INVOLVED": "inquiry-answer-status-not-involved",
                "CLAIM": "inquiry-answer-status-claim",
                "UNKNOWN": "inquiry-answer-status-unknown",
            },
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "03-verfahrensablauf-fachstelle",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_ANSWERED": {
                "template_slug": "05-bericht-erstellt",
                "recipient_types": ["inquiry_controlling"],
            },
        },
        "SUGGESTIONS": BE_DISTRIBUTION_SUGGESIONS,
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "INQUIRY_ANSWER_FILL_TASK": lambda group, *_: is_lead_role(group),
            },
        },
    },
    "kt_schwyz": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circ",
        "INQUIRY_ANSWER_CHECK_TASK": "check-inquiry",
        "INQUIRY_ANSWER_REVISE_TASK": "revise-inquiry",
        "INQUIRY_ANSWER_ALTER_TASK": "alter-inquiry",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": "Zirkulationsentscheid gestartet",
            "SKIP_DISTRIBUTION": "Zirkulationsentscheid gestartet",
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["check-inquiry", "revise-inquiry"],
            "COMPLETE_TASKS": ["revise-inquiry"],
        },
        "REDO_DISTRIBUTION": {
            "CREATE_TASKS": ["additional-demand"],
        },
        "QUESTIONS": {
            "REQUEST": "inquiry-answer-request",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
            "REASON": "inquiry-answer-reason",
            "RECOMMENDATION": "inquiry-answer-recommendation",
            "HINT": "inquiry-answer-hint",
        },
        "DEFAULT_SUGGESTIONS": [7],  # Baugesuchszentrale
        "SUGGESTIONS": SZ_DISTRIBUTION_SUGGESIONS,
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "einladung-zur-stellungnahme",
                "recipient_types": ["inquiry_addressed"],
            },
        },
        "PERMISSIONS": {
            "CompleteWorkItem": {
                "INQUIRY_CREATE_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_ANSWER_CHECK_TASK": lambda group, *_: is_lead_role(group),
                "INQUIRY_ANSWER_REVISE_TASK": lambda group, *_: is_lead_role(group),
            },
        },
        "SYNC_INQUIRY_DEADLINE_TO_ANSWER_TASKS": {
            "fill-inquiry": {
                "TIME_DELTA": timedelta(days=-3)  # check-inquiry lead-time
            }
        },
    },
    "kt_gr": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circulation",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-assessment",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
            "DEADLINE": "inquiry-deadline",
        },
        "NOTIFY_ON_CANCELLATION": True,
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "verfahrensablauf-fachstelle",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_SENT_TO_USO": {
                "template_slug": "verfahrensablauf-uso",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_ANSWERED": {
                "template_slug": "bericht-erstellt",
                "recipient_types": ["inquiry_controlling"],
            },
            "CANCELED_DISTRIBUTION": {
                "template_slug": "zirkulation-abgebrochen",
                "recipient_types": ["services_with_incomplete_inquiries"],
            },
        },
        "INQUIRY_TASK": "inquiry",
        "DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICES": {
            "uso": 7,
            "authority-bab": 90,
        },
        "ANSWERS": {
            "STATUS": {
                "POSITIVE": "inquiry-answer-status-positive",
                "NEGATIVE": "inquiry-answer-status-negative",
                "NOT_INVOLVED": "inquiry-answer-status-not-involved",
                "CLAIM": "inquiry-answer-status-claim",
                "UNKNOWN": "inquiry-answer-status-unknown",
            },
        },
        "SUGGESTIONS": GR_DISTRIBUTION_SUGGESIONS,
    },
    "kt_so": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "distribution",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-positive-assessments",
            "ANCILLARY_CLAUSES": "inquiry-answer-notices-for-authority",
            "DIRECT": "inquiry-direct",
            # For placeholders
            "POSITIVE": "inquiry-answer-positive-assessments",
            "NEGATIVE": "inquiry-answer-negative-assessments",
            "ADDITIONAL_DEMAND": "inquiry-answer-rejection-additional-demand",
            "OBJECTIONS": "inquiry-answer-objections",
            "NOTICES_APPLICANT": "inquiry-answer-notices-for-applicant",
            "NOTICES_AUTHORITY": "inquiry-answer-notices-for-authority",
            "NOTICES_ARP": "inquiry-answer-notices-for-authority-arp",
            "FORWARD": "inquiry-answer-forward",
        },
        "ANSWERS": {
            "STATUS": {
                "POSITIVE": "inquiry-answer-status-positive",
                "NEGATIVE": "inquiry-answer-status-negative",
                "CLAIM": "inquiry-answer-status-additional-demand",
                "NO_COMMENT": "inquiry-answer-status-no-comment",
                "UNKNOWN": "inquiry-answer-status-unknown",
                "DIRECT": "inquiry-answer-status-direct",
            },
            "DIRECT": {
                "YES": "inquiry-direct-yes",
            },
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "stellungnahme-angefordert",
                "recipient_types": ["inquiry_addressed"],
            },
            "INQUIRY_ANSWERED": {
                "template_slug": "stellungnahme-beantwortet",
                "recipient_types": ["inquiry_controlling"],
            },
        },
        "SUGGESTIONS": SO_DISTRIBUTION_SUGGESIONS,
    },
    "kt_uri": {
        "ENABLED": True,
        "DEFAULT_DEADLINE_LEAD_TIME": 28,  # 28 days
        "INSTANCE_STATE_DISTRIBUTION": "comm",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["fill-inquiry"],
        },
        "QUESTIONS": {
            "STATEMENT": "inquiry-answer-statement",
            "ANCILLARY_CLAUSES": "inquiry-answer-ancillary-clauses",
        },
        "NOTIFICATIONS": {
            "INQUIRY_SENT": {
                "template_slug": "4-1-zirkulation-gemeinde-gestartet",
                "recipient_types": ["inquiry_addressed"],
            },
            "KOOR_INQUIRY_ANSWERED": {
                "template_slug": "4-2-kantonale-bearbeitung-abgeschlossen",
                "recipient_types": ["inquiry_controlling"],
            },
        },
        "DEFAULT_SUGGESTIONS": [1],  # KOOR BG
        "SUGGESTIONS": UR_DISTRIBUTION_SUGGESIONS,
    },
    "kt_ag": {
        "ENABLED": True,
        "INSTANCE_STATE_DISTRIBUTION": "circulation",
        "INQUIRY_ANSWER_CHECK_TASK": "check-inquiry",
        "INQUIRY_ANSWER_REVISE_TASK": "revise-inquiry",
        "INQUIRY_ANSWER_ALTER_TASK": "alter-inquiry",
        "HISTORY": {
            "COMPLETE_DISTRIBUTION": _("Circulation completed"),
            "SKIP_DISTRIBUTION": _("Circulation skipped"),
            "REDO_DISTRIBUTION": _("Circulation reopened"),
        },
        "REDO_INQUIRY": {
            "REOPEN_TASKS": ["check-inquiry", "revise-inquiry"],
            "COMPLETE_TASKS": ["revise-inquiry"],
        },
        "SYNC_INQUIRY_DEADLINE_TO_ANSWER_TASKS": {
            "fill-inquiry": {
                "TIME_DELTA": timedelta(days=-3)  # check-inquiry lead-time
            }
        },
        "DEADLINE_LEAD_TIME_FOR_ADDRESSED_SERVICES": {
            "service-afb": 60,
        },
        "AVAILABLE_SERVICES_FOR_INQUIRY": {
            "authority": {
                "service_groups": ["service-afb", "municipality"],
                "services": [
                    "agv-bs",
                    "agv-esp",
                    "bks-dp",
                    "bks-ka",
                    "dvi-awa-iga",
                    "amb",
                    "aew",
                    "axpo",
                    "gvm",
                ],
            },
            "service-afb": {
                "service_groups": ["service-cantonal", "service-external"],
            },
        },
    },
    "demo": {"ENABLED": True},
}
