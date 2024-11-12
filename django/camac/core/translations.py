from typing import Union

from django.conf import settings
from django.utils import translation


def get_available_languages():
    available_languages = settings.LANGUAGES
    if config := settings.APPLICATION.get("AVAILABLE_LANGUAGES"):
        available_languages = [
            (code, translation)
            for code, translation in settings.LANGUAGES if code in config
        ]

    return available_languages


def get_translation_in(language, s):
    with translation.override(language, True):
        return translation.gettext(s)


def get_translations(s):
    return {lang: get_translation_in(lang, s) for lang, _ in get_available_languages()}


def get_translations_canton_aware(config: Union[dict, str]) -> dict:
    text = config

    if isinstance(config, dict):
        text = config.get(settings.APPLICATION["SHORT_NAME"], config.get("default"))

    return get_translations(text)
