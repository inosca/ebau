import locale
import uuid

import pytest
from django.urls import reverse
from django.utils import translation
from django.utils.module_loading import import_string
from rest_framework.response import Response

import camac.middleware


@pytest.mark.parametrize(
    "cookie,header,target,expect_res_lang",
    [
        # Admin: cookie > header > default
        # Any requested language that's not explicitly enabled will cause a fallback
        # to default as well.
        #
        # Note as we're not messing with the DB, we can easily just test the
        # full set of combinations
        ("de", "de", "admin", "de"),
        ("de", "fr", "admin", "de"),
        ("de", "en_GB", "admin", "de"),
        ("de", "en", "admin", "de"),
        ("de", None, "admin", "de"),
        ("fr", "de", "admin", "fr"),
        ("fr", "fr", "admin", "fr"),
        ("fr", "en_GB", "admin", "fr"),
        ("fr", "en", "admin", "fr"),
        ("fr", None, "admin", "fr"),
        ("en_GB", "de", "admin", "de"),
        ("en_GB", "fr", "admin", "de"),
        ("en_GB", "en_GB", "admin", "de"),
        ("en_GB", "en", "admin", "de"),
        ("en_GB", None, "admin", "de"),
        ("en", "de", "admin", "de"),
        ("en", "fr", "admin", "de"),
        ("en", "en_GB", "admin", "de"),
        ("en", "en", "admin", "de"),
        ("en", None, "admin", "de"),
        (None, "de", "admin", "de"),
        (None, "fr", "admin", "fr"),
        (None, "en_GB", "admin", "de"),
        (None, "en", "admin", "de"),
        (None, None, "admin", "de"),
        # API: Ignore the cookie in all cases. Validate accept-language header
        # and use default as a fallback for "invalid" requests or no requested
        # language at all
        ("de", "de", "api", "de"),
        ("de", "fr", "api", "fr"),
        ("de", "en_GB", "api", "de"),
        ("de", "en", "api", "de"),
        ("de", None, "api", "de"),
        ("fr", "de", "api", "de"),
        ("fr", "fr", "api", "fr"),
        ("fr", "en_GB", "api", "de"),
        ("fr", "en", "api", "de"),
        ("fr", None, "api", "de"),
        ("en_GB", "de", "api", "de"),
        ("en_GB", "fr", "api", "fr"),
        ("en_GB", "en_GB", "api", "de"),
        ("en_GB", "en", "api", "de"),
        ("en_GB", None, "api", "de"),
        ("en", "de", "api", "de"),
        ("en", "fr", "api", "fr"),
        ("en", "en_GB", "api", "de"),
        ("en", "en", "api", "de"),
        ("en", None, "api", "de"),
        (None, "de", "api", "de"),
        (None, "fr", "api", "fr"),
        (None, "en_GB", "api", "de"),
        (None, "en", "api", "de"),
        (None, None, "api", "de"),
    ],
)
def test_locale_setting_priority(
    # fixtures
    set_application_be,
    rf,
    settings,
    caplog,
    snapshot,
    # params
    cookie,
    header,
    target,
    expect_res_lang,
):
    expected_middleware = [
        "camac.middleware.EBauLocalePriority",
    ]
    disallowed_middleware = [
        # Don't re-add this - it does not respect *our* priority list of how to
        # set locales / languages from request
        "django.middleware.locale.LocaleMiddleware",
    ]

    def handle(request):
        # Our "view" here is just the check that the translation was initialized
        # correctly.
        # We check both Django's translation settings as well as (system)
        # gettext's configuration

        # there is no en_CH
        expected_locale = (
            "en_US.UTF-8" if expect_res_lang == "en" else f"{expect_res_lang}_CH.UTF-8"
        )

        current_gettext_locale = ".".join(locale.getlocale(locale.LC_ALL))
        current_django_lang = translation.get_language()

        assert current_gettext_locale == expected_locale
        assert current_django_lang == expect_res_lang

        return Response(status=200)

    # Ensure middleware is configured correctly
    middleware_stack = [mw for mw in settings.MIDDLEWARE if mw in expected_middleware]
    assert middleware_stack == expected_middleware

    assert all(mw not in settings.MIDDLEWARE for mw in disallowed_middleware)

    # Build our own middleware stack. We only run through "our" middlewares
    # and don't bother with authentication, sesison and all that stuff.
    middleware = [import_string(mw) for mw in middleware_stack]
    handle_request = handle
    # build up the call structure from "bottom up": last middleware calls "view",
    # then previous middleware calls *that* middleware, and so on.
    for mw in reversed(middleware):
        handle_request = mw(handle_request)

    endpoints = {
        # client-managed URL, so this shhould be visible to the user
        "admin": "/django/admin/core/servicecontent/",
        # We don't need anything existing to detect the response language
        "api": reverse("work-item-list-row-detail", args=[uuid.uuid4()]),
    }

    endpoint = endpoints[target]

    headers = {}

    # Set language in the mechanisms as defined by the parametrization
    if cookie:
        rf.cookies[settings.LANGUAGE_COOKIE_NAME] = cookie

    if header:
        # Note: We're only about the priority between the different locations
        # of setting the language, not about the detailled accept-language header
        # semantics, so a simple language parameter suffices
        headers["Accept-Language"] = header

    # we set the translation to the "default" first, then run the request
    translation.activate("en")

    # Now fetch data, and see what the result looks like
    request = rf.get(endpoint, headers=headers, cookies={})

    with caplog.at_level("DEBUG"):
        handle_request(request)
    snapshot.assert_match(caplog.messages)


def test_set_invalid_locale(rf, settings, caplog):
    mw = camac.middleware.EBauLocalePriority()

    with caplog.at_level("DEBUG"):
        mw._activate_language(rf.get("/foo"), "cn")

    assert caplog.messages == [
        "Unsupported locales - tried cn_CH, cn. Falling back to default de_CH.UTF-8",
        "Setting django language to cn",
        "Setting request language to cn",
    ]


def test_set_en_us(rf, settings, caplog):
    mw = camac.middleware.EBauLocalePriority()

    with caplog.at_level("DEBUG"):
        mw._activate_language(rf.get("/foo"), "en")

    assert caplog.messages == [
        "Set system locale to en_US.UTF-8",
        "Setting django language to en",
        "Setting request language to en",
    ]


def test_set_unsupported_language(rf, settings, caplog, application_settings):

    application_settings["AVAILABLE_LANGUAGES"] = []

    def view(request):
        return ""

    mw = camac.middleware.EBauLocalePriority(view)

    with caplog.at_level("DEBUG"):
        mw(rf.get("/foo", headers={"Accept-Language": "it"}))

    assert caplog.messages == [
        "Disabling language cookie for non-django-admin URL",
        "Detected language from accept-language header: 'it'",
        "Application is monolingual, activating default language 'de'",
        "Set system locale to de_CH.UTF-8",
        "Setting django language to de",
        "Setting request language to de",
    ]
