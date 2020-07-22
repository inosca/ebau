from django.conf import settings
from django.templatetags.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from tabulate import tabulate

from camac.constants.kt_bern import (
    ECH_ACCOMPANYING_REPORT,
    ECH_BASE_DELIVERY,
    ECH_CHANGE_RESPONSIBILITY,
    ECH_CLAIM,
    ECH_FILE_SUBSEQUENTLY,
    ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
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
from camac.user.permissions import ViewPermissions

GET_TABLE_HEADERS = [
    "Typ",
    "Beschreibung",
    "Kapitel in Spezifikation",
    "messageType",
    "Beispiel",
]

GET_TABLE_DATA = [
    [
        "BaseDelivery",
        "Gesamtdatenlieferung",
        "3.3.3",
        ECH_BASE_DELIVERY,
        f"[base_delivery]({static('xml/get/base_delivery.xml')})",
    ],
    [
        "Submit",
        "Baugesuch zustellen",
        "3.1",
        ECH_SUBMIT,
        f"[submit]({static('xml/get/submit_planning_permission_application.xml')})",
    ],
    [
        "FileSubsequently",
        "Nachforderung beantworten",
        "3.1",
        ECH_FILE_SUBSEQUENTLY,
        f"[file_subsequently]({static('xml/get/file_subsequently.xml')})",
    ],
    [
        "WithdrawPlanningPermissionApplication",
        "Rückzug des Baugesuchs melden",
        "3.3.7",
        ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION,
        f"[withdraw_planning_permission_application]({static('xml/get/withdraw_planning_permission_application.xml')})",
    ],
    [
        "Claim",
        "Nachforderungen durch Fachstelle",
        "3.3.2",
        ECH_CLAIM,
        f"[claim]({static('xml/get/claim.xml')})",
    ],
    [
        "AccompanyingReport",
        "Stellungnahme abgeben",
        "3.2",
        ECH_ACCOMPANYING_REPORT,
        f"[accompanying_report]({static('xml/get/accompanying_report.xml')})",
    ],
    [
        "ChangeResponsibility",
        "Wechsel der Zuständigkeit melden",
        "3.3.8",
        ECH_CHANGE_RESPONSIBILITY,
        f"[change_responsibility]({static('xml/get/change_responsibility.xml')})",
    ],
    [
        "Task",
        "Baugesuch zustellen",
        "5.1",
        ECH_TASK_STELLUNGNAHME,
        f"[task_stellungnahme]({static('xml/get/task_stellungnahme.xml')})",
    ],
    [
        "Task",
        "SB1 eingereicht",
        "4.1",
        ECH_TASK_SB1_SUBMITTED,
        f"[task_sb1_eingereicht]({static('xml/get/task_sb1_eingereicht.xml')})",
    ],
    [
        "Task",
        "SB2 eingereicht",
        "4.1",
        ECH_TASK_SB2_SUBMITTED,
        f"[task_sb2_eingereicht]({static('xml/get/task_sb2_eingereicht.xml')})",
    ],
    [
        "StatusNotification",
        "eBau-Nummer vergeben melden",
        "3.1",
        ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
        f"[status_notification_ebau_nr_vergeben]({static('xml/get/status_notification_ebau_nr_vergeben.xml')})",
    ],
    [
        "StatusNotification",
        "Prüfung abgeschlossen melden",
        "3.1",
        ECH_STATUS_NOTIFICATION_PRUEFUNG_ABGESCHLOSSEN,
        f"[status_notification_pruefung_abgeschlossen]({static('xml/get/status_notification_pruefung_abgeschlossen.xml')})",
    ],
    [
        "StatusNotification",
        "Zirkulation gestartet melden",
        "3.2",
        ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
        f"[status_notification_start_zirkulation]({static('xml/get/status_notification_start_zirkulation.xml')})",
    ],
    [
        "StatusNotification",
        "Selbstdeklaration 1 ausstehend melden",
        "4.1",
        ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND,
        f"[status_notification_sebstdeklaration_1_ausstehend]({static('xml/get/status_notification_sebstdeklaration_1_ausstehend.xml')})",
    ],
    [
        "StatusNotification",
        "Abgeschlossen melden",
        "4.2",
        ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
        f"[status_notification_abgeschlossen]({static('xml/get/status_notification_abgeschlossen.xml')})",
    ],
    [
        "StatusNotification",
        "Zurückgewiesen melden",
        "3.1",
        ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN,
        f"[status_notification_zurueckgewiesen]({static('xml/get/status_notification_zurueckgewiesen.xml')})",
    ],
    [
        "StatusNotification",
        "In Koordination melden",
        "3.1",
        ECH_STATUS_NOTIFICATION_IN_KOORDINATION,
        f"[status_notification_in_koordination]({static('xml/get/status_notification_in_koordination.xml')})",
    ],
]

POST_TABLE_HEADERS = [
    "Typ",
    "Beschreibung",
    "Kapitel in Spezifikation",
    "messageType",
    "Beispiel",
]

POST_TABLE_DATA = [
    [
        "NoticeRuling",
        "Entscheid zurückweisen fällen",
        "3.1",
        "5200113",
        f"[notice_ruling]({static('xml/post/notice_ruling.xml')})",
    ],
    [
        "NoticeRuling",
        "Entscheid verfügen",
        "3.2",
        "5100039",
        f"[notice_ruling]({static('xml/post/notice_ruling_2.xml')})",
    ],
    [
        "NoticeRuling",
        "Rückzugsverfügung durch Gemeinde (identisch 'Entscheid zurückweisen fällen')",
        "3.3.7",
        "5100008",
        f"[notice_ruling]({static('xml/post/notice_ruling.xml')})",
    ],
    [
        "ChangeResponsibility",
        "Zuständige Behörde melden",
        "3.1",
        "5100011",
        f"[change_responsibility]({static('xml/post/change_responsibility.xml')})",
    ],
    [
        "KindOfProceedings",
        "Verfahrensprogramm erstellen",
        "3.2",
        "5200110",
        f"[kind_of_proceedings]({static('xml/post/kind_of_proceedings.xml')})",
    ],
    [
        "Task",
        "Stellungnahme anfordern",
        "3.2",
        "5200111",
        f"[task]({static('xml/post/task.xml')})",
    ],
    [
        "CloseDossier",
        "Abschluss melden",
        "4.2",
        "5100013",
        f"[close_dossier]({static('xml/post/close_dossier.xml')})",
    ],
    [
        "AccompanyingReport",
        "Stellungnahme abgeben",
        "5.1",
        "5200112",
        f"[accompanying_report]({static('xml/post/accompanying_report.xml')})",
    ],
]


def get_swagger_description():
    with open(str(settings.ROOT_DIR("camac/echbern/docs/NOTES.md")), "r") as myfile:
        desc = myfile.read()

    get_messages = tabulate(GET_TABLE_DATA, GET_TABLE_HEADERS, tablefmt="github")
    post_messages = tabulate(POST_TABLE_DATA, POST_TABLE_HEADERS, tablefmt="github")
    desc = desc.replace("{get_messages}", get_messages).replace(
        "{post_messages}", post_messages
    )
    return desc


SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title="Camac API", default_version="v1", description=get_swagger_description()
    ),
    public=True,
    permission_classes=(ViewPermissions,),
)
