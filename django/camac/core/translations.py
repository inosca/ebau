from django.conf import settings
from django.utils import translation


def get_translation_in(language, s):
    with translation.override(language, True):
        return translation.gettext(s)


def get_translations(s):
    return {lang: get_translation_in(lang, s) for lang, _ in settings.LANGUAGES}
