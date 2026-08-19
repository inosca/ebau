from unittest.mock import Mock, patch

from django.test import override_settings

from camac.wsgi_common import setup_environment


@override_settings(EAGER_LOAD_URLCONF=True)
@patch("camac.wsgi_common.locale.setlocale")
@patch("camac.wsgi_common.django.setup")
@patch("django.urls.get_resolver")
def test_setup_environment_eagerly_loads_urlconf(
    get_resolver, django_setup, setlocale, settings
):
    resolver = Mock()
    get_resolver.return_value = resolver

    setup_environment(is_dav=False)

    django_setup.assert_called_once_with(set_prefix=False)
    get_resolver.assert_called_once_with()


@override_settings(EAGER_LOAD_URLCONF=False)
@patch("camac.wsgi_common.locale.setlocale")
@patch("camac.wsgi_common.django.setup")
@patch("django.urls.get_resolver")
def test_setup_environment_can_skip_urlconf(
    get_resolver, django_setup, setlocale, settings
):
    setup_environment(is_dav=False)

    django_setup.assert_called_once_with(set_prefix=False)
    get_resolver.assert_not_called()


@override_settings(EAGER_LOAD_URLCONF=True)
@patch("camac.wsgi_common.locale.setlocale")
@patch("camac.wsgi_common.django.setup")
@patch("django.urls.get_resolver")
def test_setup_environment_skips_urlconf_for_dav(
    get_resolver, django_setup, setlocale, settings
):
    setup_environment(is_dav=True)

    django_setup.assert_called_once_with(set_prefix=False)
    get_resolver.assert_not_called()
