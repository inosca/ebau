import re

from django.views.debug import SafeExceptionReporterFilter


class CensoredExceptionReporterFilter(SafeExceptionReporterFilter):
    """Very conservative exception reporter filter.

    This exception reporter filter should be used in production environments to
    avoid sending sensitive data in email exceptions. This will remove any
    settings from the exception body and also censors alot of request
    information (e.g the auth token).
    """

    hidden_settings = re.compile(
        # Exclude HTTP_AUTHORIZATION from logs
        "API|AUTH|TOKEN|KEY|SECRET|PASS|SIGNATURE|HTTP_COOKIE|HTTP_AUTHORIZATION",
        flags=re.IGNORECASE,
    )

    def get_safe_request_meta(self, request):
        """Only log HTTP_* values from `request.META`."""

        meta = super().get_safe_request_meta(request)

        return {k: v for k, v in meta.items() if k.startswith("HTTP_")}

    def get_safe_settings(self):
        """Don't log any settings."""

        return {}
