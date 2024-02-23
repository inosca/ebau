import pytest

from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)


@pytest.mark.parametrize("role__name,service__email", [("support", "geometer@example.com")])
@pytest.mark.parametrize("has_location,has_same_location,expected", [
    (False, False, [{ "to": "geometer@example.com" }]),
    (True, True, [{ "to": "geometer@example.com" }]),
    (True, False, [])
])
def test_recipient_localized_geometer(
    db,
    sz_instance_with_form,
    notification_template,
    form_field_factory,
    application_settings,
    location_factory,
    service,
    group,
    has_location,
    has_same_location,
    expected,
):
    if not has_location:
        group.locations.remove(sz_instance_with_form.location)

    if not has_same_location:
        sz_instance_with_form.location = location_factory()
        sz_instance_with_form.save()

    application_settings["GEOMETER_FORM_FIELDS"] = ["geometer-v3"]
    application_settings["LOCALIZED_GEOMETER_SERVICE_MAPPING"] = {
        "Test Geometer": [service.pk],
    }

    form_field_factory(instance=sz_instance_with_form, name="geometer-v3", value="Test Geometer")

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["localized_geometer"],
            "instance": {"type": "instances", "id": sz_instance_with_form.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert serializer._get_recipients_localized_geometer(sz_instance_with_form) == expected


@pytest.mark.parametrize("role__name", ["support"])
def test_recipient_tax_administration(
    db,
    sz_instance,
    notification_template,
    service_factory,
    application_settings,
):

    tax_administration_service = service_factory(email="tax-administration@example.com")
    application_settings["TAX_ADMINISTRATION"] = tax_administration_service.pk

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["inquiry_addressed", "inquiry_controlling"],
            "instance": {"type": "instances", "id": sz_instance.pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert serializer._get_recipients_tax_administration(sz_instance) == [
        {"to": "tax-administration@example.com"}
    ]


@pytest.mark.parametrize("role__name", ["support"])
def test_recipient_involved_in_construction_step(
    db,
    sz_instance,
    notification_template,
    sz_construction_monitoring_settings,
    construction_monitoring_planned_case_sz,
    service,
):

    sz_construction_monitoring_settings["NOTIFICATION_RECIPIENTS"] = {
        "construction-step-baubeginn-melden": [service.pk]
    }

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["involved_in_construction_step"],
            "instance": {"type": "instances", "id": sz_instance.pk},
            "work_item": { "type": "work-items", "id": construction_monitoring_planned_case_sz.work_items.filter(task="construction-step-baubeginn-melden").first().pk},
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert serializer._get_recipients_involved_in_construction_step(sz_instance) == [{ "to": service.email }]

