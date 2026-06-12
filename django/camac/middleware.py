import locale
import logging
import re
from contextlib import contextmanager

from django.conf import settings
from django.utils import translation

request_logger = logging.getLogger("django.request")
log = logging.getLogger()


class LoggingMiddleware(object):
    """Middleware logging all request incl. json data and user."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        log_request = False
        body = b""
        if request.method in settings.REQUEST_LOGGING_METHODS:
            body = b"multipart/form-data"
            if request.content_type != "multipart/form-data":
                body = request.body
            log_request = True

        response = self.get_response(request)
        content_type = response.get("Content-Type", "")
        if log_request and content_type in settings.REQUEST_LOGGING_CONTENT_TYPES:
            request_logger.info(
                "method=%s path=%s status=%s user=%s request=%s response=%s",
                request.method,
                request.get_full_path(),
                response.status_code,
                request.user.username,
                body.decode(),
                response.content.decode(),
            )

        return response


class EBauLocalePriority(object):
    """
    Middleware for setting the locale detection priorities right.

    Fully replace Django's own LocaleMiddleware, and define a fixed set of rules
    for language detection. These differ slightly for Django Admin and the APIs:

    A) In the django admin:
       1. cookie
       2. header
    B) in the API (GraphQL and REST):
       1. header
       Here, any language cookie is ignored, to keep the API fully stateless.

    Django's Admin pages are stateful, and *need* the cookie for the language
    switcher to work correctly. Therefore, we allow it and even give it a bit
    of preference.
    """

    def __init__(self, get_response=None):
        self.get_response = get_response

    def _reset_language_cookie_if_needed(self, request):
        """Reset the language cookie in the request, if needed.

        Django Admin uses a cookie to store the user's language. The REST API
        should use only the Accept-Language header, but apart from that, should
        be stateless.

        There are a few more Django URLs, but luckily they're all under the /django
        prefix:

           * /django/admin
           * /django/i18n
           * /django/oidc
        """
        # TODO maybe turn this into a setting, but as long as it's only
        # one prefix, it's probably not worth it
        if not request.path_info.startswith("/django"):
            # Django admin needs the cookie, but everything else should
            # use the HTTP headers or query parameter instead
            try:
                log.debug("Disabling language cookie for non-django-admin URL")
                del request.COOKIES[settings.LANGUAGE_COOKIE_NAME]
            except KeyError:
                pass

    @contextmanager
    def _hidden_lang_cookie(self, request):
        """Context manager to temporarily hide the language cookie.

        We use this so we can still use Django's get_language_from_request()
        functionality, without it giving us "wrong" results
        """
        old_cookie = request.COOKIES.pop(settings.LANGUAGE_COOKIE_NAME, None)

        yield
        if old_cookie is not None:  # pragma: no cover
            request.COOKIES[settings.LANGUAGE_COOKIE_NAME] = old_cookie

    def _detect_from_header(self, request):
        """Detect language from Accept-Language HTTP header."""

        if "HTTP_ACCEPT_LANGUAGE" not in request.META:
            return None

        # Only call get_language_from_request() if there is an accept-language header.
        # otherwise it will fallback to the default, and we want to try other options
        # before, so we cannot have that. Also hide the language cookie as well here
        # to avoid that messing with our rule priorities
        with self._hidden_lang_cookie(request):
            return translation.get_language_from_request(request, check_path=False)

    def _detect_from_cookie(self, request):
        """Detect language from HTTP cookies."""
        lang = request.COOKIES.get(settings.LANGUAGE_COOKIE_NAME)
        return lang

    def _detect_language_of_request(self, request):
        detectors = [
            ("language cookie", self._detect_from_cookie),
            ("accept-language header", self._detect_from_header),
        ]

        for source, detector in detectors:
            if lang := detector(request):
                log.debug(f"Detected language from {source}: '{lang}'")
                return lang

        # No language detected - return default
        return settings.LANGUAGE_CODE

    def _sanitize_language(self, language):
        available_languages = settings.APPLICATION.get("AVAILABLE_LANGUAGES", [])
        if language in available_languages:
            return language

        elif not available_languages:
            if settings.APPLICATION["IS_MULTILINGUAL"]:
                log.warning(
                    "Application has no available languages configured, "
                    f"falling back to default '{settings.LANGUAGE_CODE}'"
                )
            else:
                log.debug(
                    f"Application is monolingual, activating default language '{settings.LANGUAGE_CODE}'"
                )

        else:
            # language not in available_languages:
            log.debug(
                f"Detected language {language} not allowed, "
                f"falling back to {settings.LANGUAGE_CODE}"
            )
        return settings.LANGUAGE_CODE

    def _activate_language(self, request, language):
        try_locale = [self._swissify_locale(language), language]
        if language == "en":
            try_locale.append("en_US")
        has_locale_set = False
        for locale_code in try_locale:
            try:
                locale.setlocale(locale.LC_ALL, f"{locale_code}.UTF-8")
                log.debug(f"Set system locale to {locale_code}.UTF-8")
                has_locale_set = True
                break

            except locale.Error:
                pass

        if not has_locale_set:
            tried = ", ".join(try_locale)
            log.debug(
                f"Unsupported locales - tried {tried}. "
                f"Falling back to default {settings.DEFAULT_LOCALE_CODE}.UTF-8"
            )
            locale.setlocale(locale.LC_ALL, f"{settings.DEFAULT_LOCALE_CODE}.UTF-8")

        log.debug(f"Setting django language to {language}")
        translation.activate(language)
        log.debug(f"Setting request language to {language}")
        request.LANGUAGE_CODE = language

    def _swissify_locale(self, locale_code):
        if not re.match(r"^[a-z]{2}_[A-Z]{2}$", locale_code):
            return f"{locale_code}_CH"
        return locale_code  # pragma: no cover

    def __call__(self, request):
        self._reset_language_cookie_if_needed(request)

        language = self._detect_language_of_request(request)
        language = self._sanitize_language(language)

        self._activate_language(request, language)

        return self.get_response(request)
