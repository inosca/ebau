import pytest
from django.template import Context, Template


def test_custom_template_tag_settings_value(settings, application_settings):
    settings.APPLICATION_NAME = "kt_gr"
    application_settings["SHORT_NAME"] = settings.APPLICATIONS["kt_gr"]["SHORT_NAME"]
    template = Template(
        "{% load settings_value %}"
        "{% settings_value 'APPLICATION_NAME' as APPLICATION_NAME %}"
        "{% settings_value 'SHORT_NAME' from_application_settings=True as SHORT_NAME %}"
        "{{APPLICATION_NAME}}, {{SHORT_NAME}}"
    )

    rendered = template.render(Context())
    assert rendered == "kt_gr, gr"


@pytest.mark.parametrize(
    "use_tagged_releases,env,expected",
    [
        (True, "production", "1.2.3"),
        (True, "development", "development"),
        (False, "production", None),
    ],
)
def test_custom_template_tag_app_version(
    settings, application_settings, mocker, use_tagged_releases, env, expected
):
    mocker.patch("camac.camac_metadata.__version__", "1.2.3")

    settings.ENV = env
    application_settings["TAGGED_RELEASES"] = use_tagged_releases

    template = Template("{% load app_version %}{% app_version as VERSION %}{{VERSION}}")

    rendered = template.render(Context())
    assert rendered == str(expected)
