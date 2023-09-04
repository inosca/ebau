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
