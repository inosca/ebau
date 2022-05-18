from django.conf import settings
from django.templatetags.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from tabulate import tabulate

from camac.constants.kt_bern import ECH_BASE_DELIVERY
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
]


def get_swagger_description():
    with open(str(settings.ROOT_DIR("camac/ech0211/docs/kt_schwyz.md")), "r") as myfile:
        desc = myfile.read()

    get_messages = tabulate(GET_TABLE_DATA, GET_TABLE_HEADERS, tablefmt="github")
    desc = desc.replace("{get_messages}", get_messages)
    return desc


SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title="Camac API", default_version="v1", description=get_swagger_description()
    ),
    public=True,
    permission_classes=(ViewPermissions,),
)
