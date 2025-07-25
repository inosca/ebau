from django.test import Client
from django.urls import path
from django.views.debug import get_default_exception_reporter_filter
from rest_framework import status


def exception_view(request):
    raise Exception("This is an exception to test error emails")


urlpatterns = [path("exception-test/", exception_view)]


def test_error_email(mailoutbox, settings, snapshot):
    settings.ROOT_URLCONF = __name__
    settings.ADMINS = [("Admin", "admin@example.com")]
    settings.DEFAULT_EXCEPTION_REPORTER_FILTER = (
        "camac.logging.CensoredExceptionReporterFilter"
    )

    # Make sure lru cache of the function that uses the above setting is empty
    get_default_exception_reporter_filter.cache_clear()
    assert get_default_exception_reporter_filter.cache_info().hits == 0

    client = Client()
    client.raise_request_exception = False

    response = client.get(
        "/exception-test/",
        data={"foo": "bar"},
        HTTP_USER_AGENT="pytest",
        HTTP_AUTHORIZATION="Bearer sometoken",
        HTTP_X_CAMAC_GROUP="123",
    )

    assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert len(mailoutbox) == 1

    # Only check everything after "Request information" as the header data and
    # traceback would cause this snapshot to be failing all the time
    assert snapshot == mailoutbox[0].body.split("Request information:", 1)[-1].strip()
