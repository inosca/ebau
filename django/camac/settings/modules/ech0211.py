import enum

from django.utils.translation import gettext_lazy as _

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_BEILAGEN_GESUCH,
    ATTACHMENT_SECTION_BEILAGEN_SB1,
    ATTACHMENT_SECTION_BEILAGEN_SB2,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
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


class DocumentAPIFeature(enum.Enum):
    FILES_UPLOAD = "file-upload"
    FILES_DELETE = "file-delete"
    FILES_DOWNLOAD = "file-download"
    FILES_MULTI_DOWNLOAD = "file-multi-download"
    DOCUMENTS_READ = "documents-read"
    DOCUMENTS_VOID_ADD = "documents-void-add"
    DOCUMENTS_VOID_REMOVE = "documents-void-remove"
    DOCUMENTS_DECISION_ADD = "documents-decision-add"
    DOCUMENTS_DECISION_REMOVE = "documents-decision-remove"
    DOCUMENTS_PUBLICATION_ADD = "documents-publication-add"
    DOCUMENTS_PUBLICATION_REMOVE = "documents-publication-remove"
    DOCUMENTS_SENSITIVE_ADD = "documents-sensitive-add"
    DOCUMENTS_SENSITIVE_REMOVE = "documents-sensitive-remove"
    DOCUMENTS_DELETE = "documents-delete"
    CATEGORIES_READ = "categories-read"

    @classmethod
    def can(cls, *required):
        """Return True if all the required features are enabled."""
        # lazy import to avoid circular dep
        from django.conf import settings

        feature_list = settings.ECH0211.get("DOCUMENT_API_FEATURES", [])
        return all(f in feature_list for f in required)


ECH0211 = {
    "default": {
        "API_LEVEL": "full",
        "DOCUMENT_API_FEATURES": [],
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
                    "desc": "Baugesuch zugestellt",
                    "spec": "3.1",
                    "example": (
                        "submit",
                        "xml/get/submit_planning_permission_application.xml",
                    ),
                },
                ECH_FILE_SUBSEQUENTLY: {
                    "type": "FileSubsequently",
                    "desc": "Nachforderung beantwortet",
                    "spec": "3.1",
                    "example": ("file_subsequently", "xml/get/file_subsequently.xml"),
                },
                ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION: {
                    "type": "WithdrawPlanningPermissionApplication",
                    "desc": "Baugesuch zurückgezogen",
                    "spec": "3.3.7",
                    "example": (
                        "withdraw_planning_permission_application",
                        "xml/get/withdraw_planning_permission_application.xml",
                    ),
                },
                ECH_CLAIM: {
                    "type": "Claim",
                    "desc": "Nachforderung",
                    "spec": "3.3.2",
                    "example": ("claim", "xml/get/claim.xml"),
                },
                ECH_ACCOMPANYING_REPORT: {
                    "type": "AccompanyingReport",
                    "desc": "Stellungnahme abgegeben",
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
                    "desc": "Stellungnahme angefordert",
                    "spec": "5.1",
                    "example": ("task_stellungnahme", "xml/get/task_stellungnahme.xml"),
                },
                ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET: {
                    "type": "StatusNotification",
                    "desc": "Zirkulation gestartet",
                    "spec": "3.2",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN: {
                    "type": "StatusNotification",
                    "desc": "Baugesuch abgeschlossen",
                    "spec": "4.2",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN: {
                    "type": "StatusNotification",
                    "desc": "Baugesuch zurückgewiesen",
                    "spec": "3.1",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_IN_KOORDINATION: {
                    "type": "StatusNotification",
                    "desc": "In Koordination",
                    "spec": "3.1",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_ENTSCHIEDEN: {
                    "type": "StatusNotification",
                    "desc": "Entschieden",
                    "spec": "",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG: {
                    "type": "StatusNotification",
                    "desc": "Baubegleitung gestartet",
                    "spec": "",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
                },
                ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN: {
                    "type": "StatusNotification",
                    "desc": "Prüfung abgeschlossen",
                    "spec": "",
                    "example": (
                        "status_notification",
                        "xml/get/status_notification.xml",
                    ),
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
                "5200111": {
                    "type": "Task",
                    "desc": "Stellungnahme anfordern",
                    "spec": "3.2",
                    "example": ("task", "xml/post/task.xml"),
                },
                "5200115": {
                    "type": "Claim",
                    "desc": "Nachforderung an Gesuchsteller stellen",
                    "spec": "5.2",
                    "example": (
                        "claim",
                        "xml/post/claim.xml",
                    ),
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
                "5200114": {
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
        "DOCUMENT_API_FEATURES": [
            DocumentAPIFeature.FILES_UPLOAD,
            DocumentAPIFeature.FILES_DELETE,
            DocumentAPIFeature.FILES_DOWNLOAD,
            DocumentAPIFeature.FILES_MULTI_DOWNLOAD,
            DocumentAPIFeature.DOCUMENTS_READ,
            DocumentAPIFeature.CATEGORIES_READ,
        ],
    },
    "kt_schwyz": {
        "ENABLED": env.bool("ECH0211_API_ACTIVE", default=False),
        "API_LEVEL": "basic",
        "DOCUMENT_API_FEATURES": [
            DocumentAPIFeature.FILES_DOWNLOAD,
            DocumentAPIFeature.FILES_MULTI_DOWNLOAD,
        ],
    },
    "kt_bern": {
        "ENABLED": True,
        "API_LEVEL": "full",
        "DOCUMENT_API_FEATURES": [
            DocumentAPIFeature.FILES_UPLOAD,
            DocumentAPIFeature.FILES_DELETE,
            DocumentAPIFeature.FILES_DOWNLOAD,
            DocumentAPIFeature.FILES_MULTI_DOWNLOAD,
            DocumentAPIFeature.DOCUMENTS_READ,
            DocumentAPIFeature.CATEGORIES_READ,
        ],
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
        "ACCOMPANYING_REPORT": {
            "attachment_section": ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN
        },
        "REDIRECTS": {
            r"instance/<int:instance_id>/": "/page/index/instance-resource-id/20074/instance-id/%(instance_id)i",
            r"ebau-number/<int:instance_id>/": "/taskform/taskform/index/instance-resource-id/12000002/instance-id/%(instance_id)i",
            r"claim/<int:instance_id>/": "/page/index/instance-resource-id/18000006/instance-id/%(instance_id)i/additional-demand",
            r"dossier-check/<int:instance_id>/": "/page/index/instance-resource-id/150009/instance-id/%(instance_id)i",
            r"revision-history/<int:instance_id>/": "/revisionhistory/revisionhistory/index/instance-resource-id/150004/instance-id/%(instance_id)i",
        },
        "NOTICE_RULING": {
            "ALLOWED_STATES": ["coordination", "circulation"],
            "ONLY_DECLINE": ["circulation_init"],
            "SKIP_TASKS_ON_APPROVAL": ["distribution"],
        },
        "JUDGEMENT_MAPPING": {
            "inquiry-answer-status-positive": 1,
            "inquiry-answer-status-not-involved": 3,
            "inquiry-answer-status-claim": 4,
            "inquiry-answer-status-negative": 4,
            "inquiry-answer-status-unknown": None,
        },
        "CLOSE_DOSSIER": {
            "ALLOWED_STATES": ["sb1", "sb2", "conclusion", "construction-acceptance"],
            "WORK_ITEM_ACTIONS": [
                ("skip", "sb1", None),
                ("skip", "sb2", None),
                ("complete", "complete", None),
            ],
        },
        "DOCS": {
            "GET_TABLE_DATA_FULL": {
                ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN: {
                    "type": "StatusNotification",
                    "desc": "eBau-Nummer vergeben melden",
                    "spec": "3.1",
                    "example": (
                        "status_notification_ebau_nr_vergeben",
                        "xml/get/status_notification_ebau_nr_vergeben.xml",
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
                ECH_STATUS_NOTIFICATION_ENTSCHIEDEN: {"disabled": True},
                ECH_STATUS_NOTIFICATION_BAUBEGLEITUNG: {"disabled": True},
                ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN: {"disabled": True},
            },
            "POST_TABLE_DATA": {
                "5200115": {"disabled": True},  # Claim
                "5200110": {
                    "type": "KindOfProceedings",
                    "desc": "Verfahrensprogramm erstellen",
                    "spec": "3.2",
                    "example": (
                        "kind_of_proceedings",
                        "xml/post/kind_of_proceedings.xml",
                    ),
                },
            },
        },
        "ALLOWED_CATEGORIES": [
            # TODO this needs to be configured fully and correctly
            # once we migrate to Alexandria.
            "beteiligte-behörden",
            "intern",
        ],
        "ALLOWED_ATTACHMENT_SECTIONS": [
            # TODO this needs to be configured fully and correctly. This is
            # for now "just" an assumption
            "2",  # Beteiligte Behörden
            "4",  # Intern
        ],
    },
    "kt_gr": {
        "ENABLED": True,
        "DOCUMENT_API_FEATURES": [
            DocumentAPIFeature.FILES_UPLOAD,
            DocumentAPIFeature.FILES_DELETE,
            DocumentAPIFeature.FILES_DOWNLOAD,
            DocumentAPIFeature.DOCUMENTS_READ,
            DocumentAPIFeature.DOCUMENTS_DELETE,
            DocumentAPIFeature.DOCUMENTS_VOID_ADD,
            DocumentAPIFeature.DOCUMENTS_VOID_REMOVE,
            DocumentAPIFeature.DOCUMENTS_DECISION_ADD,
            DocumentAPIFeature.DOCUMENTS_DECISION_REMOVE,
            DocumentAPIFeature.DOCUMENTS_PUBLICATION_ADD,
            DocumentAPIFeature.DOCUMENTS_PUBLICATION_REMOVE,
            DocumentAPIFeature.DOCUMENTS_SENSITIVE_ADD,
            DocumentAPIFeature.DOCUMENTS_SENSITIVE_REMOVE,
        ],
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
        "ACCOMPANYING_REPORT": {
            "ALEXANDRIA_CATEGORY": "beteiligte-behörden",
            "ENABLE_ORGANISATION_EXTENSION": True,
            "EXTENSION_MAPPING": {
                "inquiry-answer-situation": {
                    "tag": "situation",
                },
                "inquiry-answer-considerations": {
                    "tag": "considerations",
                },
                "stellungnahme-bemerkungen": {
                    "tag": "comments",
                },
                "stellungnahme-in-dokumentanablage": {
                    "tag": "documentsAvailable",
                    "true_value": "stellungnahme-in-dokumentanablage-ja",
                },
            },
        },
        "REDIRECTS": {
            r"instance/<int:instance_id>/": "/cases/%(instance_id)i",
            r"claim/<int:instance_id>/": "/cases/%(instance_id)i/additional-demand",
            r"dossier-check/<int:instance_id>/": "/cases/%(instance_id)i/task-form/formal-exam",
        },
        "ALLOWED_CATEGORIES": [
            "beteiligte-behörden",
            "intern",
            "beilagen-zum-gesuch",
            "alle-beteiligten",
            "bauabnahme",
        ],
        "NOTICE_RULING": {
            "ALLOWED_STATES": ["decision", "circulation"],
            "ONLY_DECLINE": ["distribution-init"],
            "SKIP_TASKS_ON_APPROVAL": ["distribution"],
            "ALEXANDRIA_CATEGORY": "alle-beteiligten",
            "ALEXANDRIA_MARK": "decision",
        },
        "CLOSE_DOSSIER": {
            "ALLOWED_STATES": ["construction-acceptance"],
            "WORK_ITEM_ACTIONS": [
                # old module, needed until construction monitoring is rolled out
                ("complete", "construction-acceptance", None),
                # set "skip" context for 'resolve_after_construction_monitoring' (see dynamic_tasks.py)
                ("skip", "init-construction-monitoring", {"skip": True}),
            ],
        },
        "TASK_SEND": {
            "SKIP_WORK_ITEMS": ["formal-exam"],
            "COMPLETE_WORK_ITEMS": ["init-distribution"],
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
                            "ech0211:person/ech0129:identification/ech0129:personIdentification": {
                                "question_slug": "juristische-person-gesuchstellerin",
                                "static_value": "juristische-person-gesuchstellerin-nein",
                            },
                            "ech0211:person/ech0129:identification/ech0129:organisationIdentification": {
                                "question_slug": "juristische-person-gesuchstellerin",
                                "static_value": "juristische-person-gesuchstellerin-ja",
                            },
                            "ech0211:person/ech0129:identification/ech0129:personIdentification/ech0044:officialName": {
                                "question_slug": "name-gesuchstellerin",
                            },
                            "ech0211:person/ech0129:identification/ech0129:personIdentification/ech0044:firstName": {
                                "question_slug": "vorname-gesuchstellerin",
                            },
                            "ech0211:person/ech0129:identification/ech0129:organisationIdentification/ech0097:organisationName": {
                                "question_slug": "name-juristische-person-gesuchstellerin",
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
        "CLAIM": {
            "ENABLED": True,
            "ALEXANDRIA_CATEGORY": "nachforderung",
        },
        "DOCS": {
            "GET_TABLE_DATA_FULL": {
                ECH_STATUS_NOTIFICATION_IN_KOORDINATION: {
                    "desc": "Entscheid ausstehend",
                },
                ECH_STATUS_NOTIFICATION_ENTSCHIEDEN: {"disabled": True},
                ECH_FILE_SUBSEQUENTLY: {
                    "desc": "Nachforderung beantwortet",
                },
                ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION: {
                    "desc": "Baugesuch zurückgezogen (⏳ noch in Entwicklung)",
                },
                ECH_CLAIM: {"desc": "Nachforderung"},
                ECH_CHANGE_RESPONSIBILITY: {"disabled": True},
            },
            "POST_TABLE_DATA": {
                "5100011": {"disabled": True},  # Change responsibility
            },
        },
        "GEOFENCE": {"ENABLE": True, "REGIONS": ["CH"]},
    },
    "kt_so": {
        "ENABLED": True,
        "DOCUMENT_API_FEATURES": [
            DocumentAPIFeature.FILES_UPLOAD,
            DocumentAPIFeature.FILES_DELETE,
            DocumentAPIFeature.FILES_DOWNLOAD,
        ],
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
        "ACCOMPANYING_REPORT": {"ALEXANDRIA_CATEGORY": "beteiligte-behoerden"},
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
            "ALLOWED_STATES": ["decision", "distribution"],
            "ONLY_DECLINE": ["distribution-init"],
            "SKIP_TASKS_ON_APPROVAL": ["distribution"],
            "ALEXANDRIA_CATEGORY": "beteiligte-behoerden",
            "ALEXANDRIA_MARK": "decision",
        },
        "CLOSE_DOSSIER": {
            "ALLOWED_STATES": ["construction-monitoring"],
            "WORK_ITEM_ACTIONS": [
                # set "skip" context for 'resolve_after_construction_monitoring' (see dynamic_tasks.py)
                ("skip", "init-construction-monitoring", {"skip": True}),
                ("complete", "complete-instance", None),
            ],
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
                    "desc": "Zirkulation abgeschlossen",
                },
                ECH_CHANGE_RESPONSIBILITY: {"disabled": True},
            },
            "POST_TABLE_DATA": {
                "5200115": {"disabled": True},  # Claim
                "5100011": {"disabled": True},  # Change responsibility
            },
        },
    },
    "kt_ag": {
        "ENABLED": True,
        "DOCUMENT_API_FEATURES": [
            DocumentAPIFeature.FILES_UPLOAD,
            DocumentAPIFeature.FILES_DELETE,
            DocumentAPIFeature.FILES_DOWNLOAD,
        ],
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
                "new_state": ["to-finish", "decided"],
                "type": ECH_STATUS_NOTIFICATION_ENTSCHIEDEN,
            },
        ],
        "TASK_MAP": {
            "circulation": {
                "message_type": ECH_TASK_STELLUNGNAHME,
                "comment": _("Inquiry sent"),
                "category": "beilagen-zum-gesuch",
            },
        },
        "ACCOMPANYING_REPORT": {
            "ALEXANDRIA_CATEGORY": "beteiligte-behörden",
            "ENABLE_ORGANISATION_EXTENSION": True,
        },
        "REDIRECTS": {
            r"instance/<int:instance_id>/": "/cases/%(instance_id)i",
            r"claim/<int:instance_id>/": "/cases/%(instance_id)i/additional-demand",
            r"dossier-check/<int:instance_id>/": "/cases/%(instance_id)i/task-form/formal-exam",
        },
        "ALLOWED_CATEGORIES": [
            "beilagen-zum-gesuch",
            "unterlagenergaenzung",
            "alle-beteiligten",
            "beteiligte-behörden",
            "intern",
        ],
        "NOTICE_RULING": {
            "ALLOWED_STATES": ["subm", "distribution-init", "circulation", "decision"],
            "ONLY_DECLINE": [],
            "SKIP_TASKS_ON_APPROVAL": ["formal-exam", "distribution"],
            "ALEXANDRIA_CATEGORY": "alle-beteiligten",
            "ALEXANDRIA_MARK": "decision",
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
                    "ech0211:planningPermissionApplication/ech0211:description": {
                        "question_slug": "beschreibung-bauvorhaben",
                    },
                    "ech0211:planningPermissionApplication/ech0211:locationAddress/ech0010:town": {
                        "question_slug": "ort-grundstueck",
                    },
                    "ech0211:planningPermissionApplication/ech0211:locationAddress/ech0010:swissZipCode": {
                        "question_slug": "plz",
                        "default": 0000,
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
                            "ech0211:person/ech0129:identification/ech0129:personIdentification": {
                                "question_slug": "juristische-person-gesuchstellerin",
                                "static_value": "juristische-person-gesuchstellerin-nein",
                            },
                            "ech0211:person/ech0129:identification/ech0129:organisationIdentification": {
                                "question_slug": "juristische-person-gesuchstellerin",
                                "static_value": "juristische-person-gesuchstellerin-ja",
                            },
                            "ech0211:person/ech0129:identification/ech0129:personIdentification/ech0044:officialName": {
                                "question_slug": "name-gesuchstellerin",
                            },
                            "ech0211:person/ech0129:identification/ech0129:personIdentification/ech0044:firstName": {
                                "question_slug": "vorname-gesuchstellerin",
                            },
                            "ech0211:person/ech0129:identification/ech0129:organisationIdentification/ech0097:organisationName": {
                                "question_slug": "name-juristische-person-gesuchstellerin",
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
        "CLOSE_DOSSIER": {
            "ALLOWED_STATES": ["decided", "construction-monitoring", "to-finish"],
            "WORK_ITEM_ACTIONS": [
                ("skip", "init-construction-monitoring", {"skip": True}),
                ("complete", "complete-instance", None),
            ],
        },
        "TASK_SEND": {
            "SKIP_WORK_ITEMS": ["formal-exam"],
            "COMPLETE_WORK_ITEMS": ["init-distribution"],
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
        "CLAIM": {
            "ENABLED": True,
            "ALEXANDRIA_CATEGORY": "unterlagenergaenzung",
        },
        "DOCS": {
            "GET_TABLE_DATA_FULL": {
                ECH_STATUS_NOTIFICATION_IN_KOORDINATION: {
                    "desc": "Zirkulation abgeschlossen",
                },
                ECH_CHANGE_RESPONSIBILITY: {"disabled": True},
                ECH_FILE_SUBSEQUENTLY: {
                    "desc": "Nachforderung beantwortet",
                },
                ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION: {
                    "desc": "Baugesuch zurückgezogen",
                },
                ECH_CLAIM: {"disabled": True},
            },
            "POST_TABLE_DATA": {
                "5100011": {"disabled": True},  # Change responsibility
            },
        },
    },
}
