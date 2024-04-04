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
        "JUDGEMENT_MAPPING": {
            "inquiry-answer-status-positive": 1,
            "inquiry-answer-status-not-involved": 3,
            "inquiry-answer-status-claim": 4,
            "inquiry-answer-status-negative": 4,
            "inquiry-answer-status-unknown": None,
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
        "JUDGEMENT_MAPPING": {
            "inquiry-answer-status-approved": 1,
            "inquiry-answer-status-positive": 1,
            "inquiry-answer-status-not-involved": 3,
            "inquiry-answer-status-renounced": 3,
            "inquiry-answer-status-claim": 4,
            "inquiry-answer-status-rejected": 4,
            "inquiry-answer-status-negative": 4,
            "inquiry-answer-status-written-off": None,
            "inquiry-answer-status-not-following": None,
        },
        "SUBMIT_PLANNING_PERMISSION_APPLICATION": {
            "ENABLED": True,
            "ALLOWED_ROLES": ["municipality-lead"],
            "FORM_ID": 1,
            "WORKFLOW": "building-permit",
            "ALEXANDRIA_CATEGORY": "beilagen-zum-gesuch",
            "QUESTION_MAPPING": {
                "SIMPLE": {
                    # xpath: {question_slug, default}
                    "use-default": {
                        "question_slug": "vorhaben",
                        "default": ["vorhaben-andere"],
                    },
                    # "planningPermissionApplication.constructionProjectInformation.constructionProject.description": "beschreibung-bauvorhaben",
                    "ech0211:planningPermissionApplication/ech0211:description": {
                        "question_slug": "beschreibung-bauvorhaben",
                    },
                },
                "TABLE": {
                    # xpath
                    "ech0211:planningPermissionApplication/ech0211:realestateInformation": (
                        # row_form
                        "parzelle-tabelle",
                        # xpath: question_slug
                        {
                            "ech0211:realestate/ech0129:realestateIdentification/ech0129:number": {
                                "question_slug": "parzellennummer"
                            }
                        },
                        # table_question
                        "parzelle",
                    ),
                    "ech0211:relationshipToPerson[ech0211:role='applicant']": (
                        "personalien-tabelle",
                        {
                            "use-default": {
                                "question_slug": "juristische-person-gesuchstellerin",
                                "default": "juristische-person-gesuchstellerin-nein",
                            },
                            "ech0211:person/ech0129:identification/ech0129:personIdentification/ech0044:officialName": {
                                "question_slug": "name-gesuchstellerin",
                            },
                            "ech0211:person/ech0129:identification/ech0129:personIdentification/ech0044:firstName": {
                                "question_slug": "vorname-gesuchstellerin",
                            },
                            "ech0211:person/ech0129:address/ech0010:town": {
                                "question_slug": "ort-gesuchstellerin",
                                "default": "-",
                            },
                            "ech0211:person/ech0129:address/ech0010:swissZipCode": {
                                "question_slug": "plz-gesuchstellerin",
                                "default": 0000,
                            },
                            "ech0211:person/ech0129:address/ech0010:street": {
                                "question_slug": "strasse-gesuchstellerin",
                                "default": "-",
                            },
                            "ech0211:person/ech0129:phone/ech0129:phoneNumber": {
                                "question_slug": "telefon-oder-mobile-gesuchstellerin",
                                "default": "0000000000",
                            },
                            "ech0211:person/ech0129:email/ech0129:emailAddress": {
                                "question_slug": "e-mail-gesuchstellerin",
                                "default": "-@-.-",
                            },
                        },
                        "personalien-gesuchstellerin",
                    ),
                },
            },
        },
    },
}
