import pytest
from django.utils.translation import get_language, gettext_noop, override

from camac.core.translations import get_translations


@pytest.mark.parametrize("current_language", ["de", "fr"])
def test_get_translations(application_settings, current_language):
    application_settings["AVAILABLE_LANGUAGES"] = ["de", "fr"]

    with override(current_language):
        assert get_language() == current_language
        assert get_translations(gettext_noop("User")) == {
            "de": "Benutzer",
            "fr": "Utilisateur",
        }
        assert get_language() == current_language
