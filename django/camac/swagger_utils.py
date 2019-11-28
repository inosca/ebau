import os

from django.conf import settings
from django.contrib.staticfiles.templatetags.staticfiles import static
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

from camac.user.permissions import ViewPermissions

group_param = openapi.Parameter(
    "group",
    openapi.IN_QUERY,
    description="Group ID the request should be made for.",
    type=openapi.TYPE_INTEGER,
)


def get_xml_link_list(method):
    messages = []
    for filename in os.listdir(
        str(settings.ROOT_DIR(f"camac/echbern/static/xml/{method}/"))
    ):
        messages.append(
            f" - [{filename.replace('.xml', '')}]({static(f'xml/{method}/{filename}')})"
        )
    return messages


def get_swagger_description():
    with open(str(settings.ROOT_DIR(f"camac/echbern/docs/NOTES.md")), "r") as myfile:
        desc = myfile.read()

    get_messages = get_xml_link_list("get")
    post_messages = get_xml_link_list("post")
    desc = desc.replace("{get_messages}", "\n".join(get_messages)).replace(
        "{post_messages}", "\n".join(post_messages)
    )
    return desc


SCHEMA_VIEW = get_schema_view(
    openapi.Info(
        title="Camac API", default_version="v1", description=get_swagger_description()
    ),
    public=True,
    permission_classes=(ViewPermissions,),
)
