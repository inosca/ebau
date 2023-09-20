from django.template import Context, Template


def test_custom_template_tag_settings_value(settings, application_settings):
    settings.APPLICATION_NAME = "kt_gr"
    application_settings["APPLICATION_NAME"] = "kt_gr"
    context = Context({"APPLICATION_NAME": application_settings["APPLICATION_NAME"]})
    template = Template(
        "{% load settings_value %}"
        "{% settings_value 'APPLICATION_NAME' as APPLICATION_NAME %}"
        "Application name: {{APPLICATION_NAME}}"
    )

    rendered = template.render(context)
    assert rendered == "Application name: kt_gr"
