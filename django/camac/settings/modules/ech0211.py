from django.utils.translation import gettext_lazy as _

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_BEILAGEN_GESUCH,
    ATTACHMENT_SECTION_BEILAGEN_SB1,
    ATTACHMENT_SECTION_BEILAGEN_SB2,
    ECH_ACCOMPANYING_REPORT,
    ECH_BASE_DELIVERY,
    ECH_CHANGE_RESPONSIBILITY,
    ECH_CLAIM,
    ECH_FILE_SUBSEQUENTLY,
    ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG,
    ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
    ECH_STATUS_NOTIFICATION_ENTSCHIEDEN,
    ECH_STATUS_NOTIFICATION_IN_KOORDINATION,
    ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND,
    ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
    ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN,
    ECH_SUBMIT,
    ECH_TASK_SB1_SUBMITTED,
    ECH_TASK_SB2_SUBMITTED,
    ECH_TASK_STELLUNGNAHME,
    ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION,
)
from camac.settings.env import env

ECH0211 = {
    "default": {
        "API_LEVEL": "full",
        "DOCS": {
            "TABLE_HEADERS": [
                "Typ",
                "Beschreibung",
                "Kapitel in Spezifikation",
                "messageType",
                "Beispiel",
            ],
            "GET_TABLE_DATA_BASIC": {
                ECH_BASE_DELIVERY: {
                    "type": "BaseDelivery",
                    "desc": "Gesamtdatenlieferung",
                    "spec": "3.3.3",
                    "example": ("base_delivery", "xml/get/base_delivery.xml"),
                },
            },
            "GET_TABLE_DATA_FULL": {
                ECH_SUBMIT: {
                    "type": "Submit",
                    "desc": "Baugesuch zustellen",
                    "spec": "3.1",
                    "example": (
                        "submit",
                        "xml/get/submit_planning_permission_application.xml",
                    ),
                },
                ECH_FILE_SUBSEQUENTLY: {
                    "type": "FileSubsequently",
                    "desc": "Nachforderung beantworten",
                    "spec": "3.1",
                    "example": ("file_subsequently", "xml/get/file_subsequently.xml"),
                },
                ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION: {
                    "type": "WithdrawPlanningPermissionApplication",
                    "desc": "Rückzug des Baugesuchs melden",
                    "spec": "3.3.7",
                    "example": (
                        "withdraw_planning_permission_application",
                        "xml/get/withdraw_planning_permission_application.xml",
                    ),
                },
                ECH_CLAIM: {
                    "type": "Claim",
                    "desc": "Nachforderungen durch Fachstelle",
                    "spec": "3.3.2",
                    "example": ("claim", "xml/get/claim.xml"),
                },
                ECH_ACCOMPANYING_REPORT: {
                    "type": "AccompanyingReport",
                    "desc": "Stellungnahme abgeben",
                    "spec": "3.2",
                    "example": (
                        "accompanying_report",
                        "xml/get/accompanying_report.xml",
                    ),
                },
                ECH_CHANGE_RESPONSIBILITY: {
                    "type": "ChangeResponsibility",
                    "desc": "Wechsel der Zuständigkeit melden",
                    "spec": "3.3.8",
                    "example": (
                        "change_responsibility",
                        "xml/get/change_responsibility.xml",
                    ),
                },
                ECH_TASK_STELLUNGNAHME: {
                    "type": "Task",
                    "desc": "Baugesuch zustellen",
                    "spec": "5.1",
                    "example": ("task_stellungnahme", "xml/get/task_stellungnahme.xml"),
                },
                ECH_TASK_SB1_SUBMITTED: {
                    "type": "Task",
                    "desc": "SB1 eingereicht",
                    "spec": "4.1",
                    "example": (
                        "task_sb1_eingereicht",
                        "xml/get/task_sb1_eingereicht.xml",
                    ),
                },
                ECH_TASK_SB2_SUBMITTED: {
                    "type": "Task",
                    "desc": "SB2 eingereicht",
                    "spec": "4.1",
                    "example": (
                        "task_sb2_eingereicht",
                        "xml/get/task_sb2_eingereicht.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN: {
                    "type": "StatusNotification",
                    "desc": "eBau-Nummer vergeben melden",
                    "spec": "3.1",
                    "example": (
                        "status_notification_ebau_nr_vergeben",
                        "xml/get/status_notification_ebau_nr_vergeben.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET: {
                    "type": "StatusNotification",
                    "desc": "Zirkulation gestartet melden",
                    "spec": "3.2",
                    "example": (
                        "status_notification_start_zirkulation",
                        "xml/get/status_notification_start_zirkulation.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND: {
                    "type": "StatusNotification",
                    "desc": "Selbstdeklaration 1 ausstehend melden",
                    "spec": "4.1",
                    "example": (
                        "status_notification_sebstdeklaration_1_ausstehend",
                        "xml/get/status_notification_sebstdeklaration_1_ausstehend.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN: {
                    "type": "StatusNotification",
                    "desc": "Abgeschlossen melden",
                    "spec": "4.2",
                    "example": (
                        "status_notification_abgeschlossen",
                        "xml/get/status_notification_abgeschlossen.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN: {
                    "type": "StatusNotification",
                    "desc": "Zurückgewiesen melden",
                    "spec": "3.1",
                    "example": (
                        "status_notification_zurueckgewiesen",
                        "xml/get/status_notification_zurueckgewiesen.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_IN_KOORDINATION: {
                    "type": "StatusNotification",
                    "desc": "In Koordination melden",
                    "spec": "3.1",
                    "example": (
                        "status_notification_in_koordination",
                        "xml/get/status_notification_in_koordination.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ENTSCHIEDEN: {
                    "type": "StatusNotification",
                    "desc": "Entschieden melden",
                    "spec": "",
                    "example": None,
                },
                ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG: {
                    "type": "StatusNotification",
                    "desc": "Baubegleitung gestartet melden",
                    "spec": "",
                    "example": None,
                },
                ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN: {
                    "type": "StatusNotification",
                    "desc": "Prüfung abgeschlossen melden",
                    "spec": "",
                    "example": None,
                },
            },
            "POST_TABLE_DATA": {
                "5200113": {
                    "type": "NoticeRuling",
                    "desc": "Entscheid zurückweisen fällen",
                    "spec": "3.1",
                    "example": ("notice_ruling", "xml/post/notice_ruling.xml"),
                },
                "5100039": {
                    "type": "NoticeRuling",
                    "desc": "Entscheid verfügen",
                    "spec": "3.2",
                    "example": ("notice_ruling", "xml/post/notice_ruling_2.xml"),
                },
                "5100008": {
                    "type": "NoticeRuling",
                    "desc": "Rückzugsverfügung durch Gemeinde (identisch 'Entscheid zurückweisen fällen')",
                    "spec": "3.3.7",
                    "example": ("notice_ruling", "xml/post/notice_ruling.xml"),
                },
                "5100011": {
                    "type": "ChangeResponsibility",
                    "desc": "Zuständige Behörde melden",
                    "spec": "3.1",
                    "example": (
                        "change_responsibility",
                        "xml/post/change_responsibility.xml",
                    ),
                },
                "5200110": {
                    "type": "KindOfProceedings",
                    "desc": "Verfahrensprogramm erstellen",
                    "spec": "3.2",
                    "example": (
                        "kind_of_proceedings",
                        "xml/post/kind_of_proceedings.xml",
                    ),
                },
                "5200111": {
                    "type": "Task",
                    "desc": "Stellungnahme anfordern",
                    "spec": "3.2",
                    "example": ("task", "xml/post/task.xml"),
                },
                "5100013": {
                    "type": "CloseDossier",
                    "desc": "Abschluss melden",
                    "spec": "4.2",
                    "example": ("close_dossier", "xml/post/close_dossier.xml"),
                },
                "5200112": {
                    "type": "AccompanyingReport",
                    "desc": "Stellungnahme abgeben",
                    "spec": "5.1",
                    "example": (
                        "accompanying_report",
                        "xml/post/accompanying_report.xml",
                    ),
                },
            },
            "POST_SUBMIT": {
                "5200113": {
                    "type": "Submit",
                    "desc": "Dossier einreichen",
                    "spec": "-",
                    "example": (
                        "submit",
                        "xml/post/submit_planning_permission_application.xml",
                    ),
                },
            },
        },
        "ALEXANDRIA_MARKS_STATUS_MAP": {
            # order is precedence
            "void": "invalidated",
            "decision": "approved",
        },
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
        "DOCS": {
            "GET_TABLE_DATA_FULL": {
                ECH_STATUS_NOTIFICATION_ENTSCHIEDEN: {"disabled": True},
                ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG: {"disabled": True},
                ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN: {"disabled": True},
            },
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
            {
                "new_state": "withdrawn",
                "type": ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION,
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
            "ALEXANDRIA_CATEGORY": "alle-beteiligten",
            "ALEXANDRIA_MARK": "decision",
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
        "KIND_OF_PROCEEDINGS": {
            "ALEXANDRIA_CATEGORY": "alle-beteiligten",
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
        "DOCS": {
            "GET_TABLE_DATA_FULL": {
                ECH_STATUS_NOTIFICATION_ENTSCHIEDEN: {"disabled": True}
            },
        },
        "GEOFENCE": {"ENABLE": True, "REGIONS": ["CH"]},
    },
    "kt_so": {
        "ENABLED": True,
        "STATUS_NOTIFICATION_TYPES": [
            {
                "new_state": "init-distribution",
                "type": ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN,
            },
            {
                "new_state": "distribution",
                "type": ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
            },
            {
                "new_state": "construction-monitoring",
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
            {
                "new_state": "decided",
                "type": ECH_STATUS_NOTIFICATION_ENTSCHIEDEN,
            },
            {
                "new_state": "withdrawn",
                "type": ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION,
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
        "ALLOWED_CATEGORIES": [
            "beteiligte-behoerden",
            "intern",
            "intern-mit-unterfachstellen",
        ],
        "NOTICE_RULING": {
            "ALLOWED_STATES": ["decision", "circulation"],
            "ONLY_DECLINE": ["distribution-init"],
            "ALEXANDRIA_CATEGORY": "beteiligte-behoerden",
            "ALEXANDRIA_MARK": "decision",
        },
        "JUDGEMENT_MAPPING": {
            "inquiry-answer-status-positive": 1,
            "inquiry-answer-status-negative": 4,
            "inquiry-answer-status-additional-demand": 4,
            "inquiry-answer-status-rejection": 4,
            "inquiry-answer-status-no-comment": None,
        },
        "KIND_OF_PROCEEDINGS": {
            "ALEXANDRIA_CATEGORY": "beteiligte-behoerden",
        },
        "DOCS": {
            "GET_TABLE_DATA_FULL": {
                ECH_STATUS_NOTIFICATION_IN_KOORDINATION: {
                    "desc": "Zirkulation abgeschlossen melden",
                },
                ECH_CHANGE_RESPONSIBILITY: {"disabled": True},
                ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN: {"disabled": True},
                ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND: {"disabled": True},
                ECH_TASK_SB1_SUBMITTED: {"disabled": True},
                ECH_TASK_SB2_SUBMITTED: {"disabled": True},
            },
            "POST_TABLE_DATA": {
                "5100011": {"disabled": True},  # Change responsibility
            },
        },
    },
}
