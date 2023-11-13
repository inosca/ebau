from typing import Union

from django.conf import settings
from django.utils import translation


def get_translation_in(language, s):
    with translation.override(language, True):
        return translation.gettext(s)


def get_translations(s):
    return {lang: get_translation_in(lang, s) for lang, _ in settings.LANGUAGES}


def get_translations_canton_aware(config: Union[dict, str]) -> dict:
    text = config

    if isinstance(config, dict):
        text = config.get(settings.APPLICATION["SHORT_NAME"], config.get("default"))

    return get_translations(text)
