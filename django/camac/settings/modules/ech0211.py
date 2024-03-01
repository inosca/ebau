from django.utils.translation import gettext_lazy as _

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_BEILAGEN_GESUCH,
    ATTACHMENT_SECTION_BEILAGEN_SB1,
    ATTACHMENT_SECTION_BEILAGEN_SB2,
    ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG,
    ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
    ECH_STATUS_NOTIFICATION_IN_KOORDINATION,
    ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND,
    ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
    ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN,
    ECH_TASK_SB1_SUBMITTED,
    ECH_TASK_SB2_SUBMITTED,
    ECH_TASK_STELLUNGNAHME,
)
from camac.settings.env import env

ECH0211 = {
    "default": {
        "API_LEVEL": "full",
    },
    "test": {
        "ENABLED": True,
    },
    "kt_schwyz": {
        "ENABLED": env.bool("ECH0211_API_ACTIVE", default=False),
        "API_LEVEL": "basic",
    },
    "kt_bern": {
        "ENABLED": True,
        "STATUS_NOTIFICATION_TYPES": [
            {
                "new_state": "circulation_init",
                "type": ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
            },
            {
                "new_state": "circulation",
                "type": ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
            },
            {
                # cancel rejection must result in start circulation status notification
                "prev_state": "rejected",
                "type": ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
            },
            {
                "new_state": "sb1",
                "type": ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND,
            },
            {
                "new_state": ["evaluated", "finished"],
                "type": ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
            },
            {
                "new_state": "rejected",
                "type": ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN,
            },
            {
                "new_state": "coordination",
                "type": ECH_STATUS_NOTIFICATION_IN_KOORDINATION,
            },
        ],
        "TASK_MAP": {
            "circulation": {
                "message_type": ECH_TASK_STELLUNGNAHME,
                "comment": _("Inquiry sent"),
                "attachment_section": ATTACHMENT_SECTION_BEILAGEN_GESUCH,
            },
            "sb2": {
                "message_type": ECH_TASK_SB1_SUBMITTED,
                "comment": _("SB1 submitted"),
                "attachment_section": ATTACHMENT_SECTION_BEILAGEN_SB1,
            },
            "conclusion": {
                "message_type": ECH_TASK_SB2_SUBMITTED,
                "comment": _("SB2 submitted"),
                "attachment_section": ATTACHMENT_SECTION_BEILAGEN_SB2,
            },
        },
        "REDIRECTS": {
            r"instance/<int:instance_id>/": "/page/index/instance-resource-id/20074/instance-id/%(instance_id)i",
            r"ebau-number/<int:instance_id>/": "/taskform/taskform/index/instance-resource-id/12000002/instance-id/%(instance_id)i",
            r"claim/<int:instance_id>/": "/claim/claim/index/instance-resource-id/150000/instance-id/%(instance_id)i",
            r"dossier-check/<int:instance_id>/": "/page/index/instance-resource-id/150009/instance-id/%(instance_id)i",
            r"revision-history/<int:instance_id>/": "/revisionhistory/revisionhistory/index/instance-resource-id/150004/instance-id/%(instance_id)i",
        },
        "NOTICE_RULING": {
            "ALLOWED_STATES": ["coordination", "circulation"],
            "ONLY_DECLINE": ["circulation_init"],
        },
    },
    "kt_gr": {
        "ENABLED": True,
        "ALLOW_SUBMIT_BY_MUNICIPALITY": True,
        "STATUS_NOTIFICATION_TYPES": [
            {
                "new_state": "init-distribution",
                "type": ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN,
            },
            {
                "new_state": "circulation",
                "type": ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
            },
            {
                # cancel rejection must result in start circulation status notification
                "prev_state": "rejected",
                "type": ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
            },
            {
                "new_state": "construction-acceptance",
                "type": ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG,
            },
            {
                "new_state": "finished",
                "type": ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
            },
            {
                "new_state": "rejected",
                "type": ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN,
            },
            {
                "new_state": "decision",
                "type": ECH_STATUS_NOTIFICATION_IN_KOORDINATION,
            },
        ],
        "TASK_MAP": {
            "circulation": {
                "message_type": ECH_TASK_STELLUNGNAHME,
                "comment": _("Inquiry sent"),
                "category": "beilagen-zum-gesuch",
            },
        },
        "REDIRECTS": {
            r"instance/<int:instance_id>/": "/cases/%(instance_id)i",
            r"claim/<int:instance_id>/": "/cases/%(instance_id)i/additional-demand",
            r"dossier-check/<int:instance_id>/": "/cases/%(instance_id)i/task-form/formal-exam",
        },
        "ALLOWED_CATEGORIES": ["beteiligte-behörden", "intern"],
        "NOTICE_RULING": {
            "ALLOWED_STATES": ["decision", "circulation"],
            "ONLY_DECLINE": ["distribution-init"],
        },
    },
}
