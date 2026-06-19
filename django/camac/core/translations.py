from typing import Union

from django.conf import settings
from django.utils import translation


def get_available_languages():
    available_languages = settings.LANGUAGES
    if config := settings.APPLICATION.get("AVAILABLE_LANGUAGES"):
        available_languages = [
            (code, translation)
            for code, translation in settings.LANGUAGES
            if code in config
        ]

    return available_languages


def get_translation_in(language, s):
    with translation.override(language):
        return translation.gettext(s)


def get_translations(s):
    return {lang: get_translation_in(lang, s) for lang, _ in get_available_languages()}


def get_translations_canton_aware(config: Union[dict, str], static=False) -> dict:
    """Make translations for configured locales of the current config.

    :param config: the string or a dict specifying a config specific translation
    :param static: create translations dict without translating
    """
    text = config

    if isinstance(config, dict):
        text = config.get(settings.APPLICATION["SHORT_NAME"], config.get("default"))

    if static:
        return {lang: text for lang, _ in get_available_languages()}

    return get_translations(text)
