from django import template
from django.conf import settings

from camac import camac_metadata

register = template.Library()


@register.simple_tag
def app_version():
    if not settings.APPLICATION.get("TAGGED_RELEASES"):
        return None
    elif settings.ENV != "production":
        return settings.ENV

    return camac_metadata.__version__
