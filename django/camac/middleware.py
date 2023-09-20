import locale
import logging
import re

from django.conf import settings

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


class SystemLocaleMiddleware(object):
    """Middleware setting python locale since this is not done by django locale."""

    def __init__(self, get_response=None):
        self.get_response = get_response

    def __call__(self, request):
        locale_code = request.LANGUAGE_CODE
        if not re.match(r"^[a-z]{2}_[A-Z]{2}$", locale_code):
            locale_code = f"{locale_code}_CH"

        try:
            locale.setlocale(locale.LC_ALL, f"{locale_code}.UTF-8")
        except locale.Error:
            log.debug(f"Trying to load unsupported locale {locale_code}")
            locale.setlocale(locale.LC_ALL, f"{settings.DEFAULT_LOCALE_CODE}.UTF-8")

        return self.get_response(request)
