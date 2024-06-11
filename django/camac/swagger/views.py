from typing import List

from django.conf import settings
from django.templatetags.static import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from tabulate import tabulate

from camac.user.permissions import ViewPermissions


def convert_to_table_data(rows: dict) -> List[List]:
    return [
        [
            config["type"],  # Type
            config["desc"],  # Description
            config["spec"],  # Reference from specification
            message_type,  # Message type
            f"[{config['example'][0]}]({static(config['example'][1])})"  # Example
            if config["example"]
            else "",
        ]
        for message_type, config in rows.items()
        if not config.get("disabled")
    ]


def get_swagger_description():
    with open(
        str(settings.ROOT_DIR(f"camac/ech0211/docs/{settings.APPLICATION_NAME}.md")),
        "r",
    ) as myfile:
        desc = myfile.read()

    if settings.ECH0211:
        api_level = settings.ECH0211.get("API_LEVEL")

        get_table_data = settings.ECH0211["DOCS"]["GET_TABLE_DATA_BASIC"]
        post_table_data = {}

        if api_level == "full":
            get_table_data = {
                **get_table_data,
                **settings.ECH0211["DOCS"]["GET_TABLE_DATA_FULL"],
            }
            post_table_data = {
                **post_table_data,
                **settings.ECH0211["DOCS"]["POST_TABLE_DATA"],
            }

        if settings.ECH0211.get("SUBMIT_PLANNING_PERMISSION_APPLICATION", {}).get(
            "ENABLED"
        ):
            post_table_data = {
                **post_table_data,
                **settings.ECH0211["DOCS"]["POST_SUBMIT"],
            }

        get_messages = tabulate(
            convert_to_table_data(get_table_data),
            settings.ECH0211["DOCS"]["TABLE_HEADERS"],
            tablefmt="github",
        )
        post_messages = tabulate(
            convert_to_table_data(post_table_data),
            settings.ECH0211["DOCS"]["TABLE_HEADERS"],
            tablefmt="github",
        )

        desc = desc.replace("{get_messages}", get_messages).replace(
            "{post_messages}", post_messages
        )

    desc = (
        desc.replace("{internal_base_url}", settings.INTERNAL_BASE_URL)
        .replace("{keycloak_url}", settings.KEYCLOAK_URL)
        .replace("{keycloak_realm}", settings.KEYCLOAK_REALM)
    )

    return desc


def get_swagger_view():
    return get_schema_view(
        openapi.Info(
            title="Camac API",
            default_version="v1",
            description=get_swagger_description(),
        ),
        public=True,
        permission_classes=(ViewPermissions,),
    )
