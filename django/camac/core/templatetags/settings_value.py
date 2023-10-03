from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def settings_value(name, from_application_settings=False):
    if from_application_settings:
        return settings.APPLICATION.get(name, "")

    return getattr(settings, name, "")
