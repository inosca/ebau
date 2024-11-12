import pytest

from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)


@pytest.mark.parametrize(
    "role__name,service__email", [("support", "geometer@example.com")]
)
@pytest.mark.parametrize(
    "has_geometer,has_location,has_same_location,expected",
    [
        (True, False, False, [{"to": "geometer@example.com"}]),
        (True, True, True, [{"to": "geometer@example.com"}]),
        (True, True, False, []),
        (False, True, False, []),
    ],
)
def test_recipient_localized_geometer(
    db,
    sz_instance_with_form,
    notification_template,
    form_field_factory,
    application_settings,
    location_factory,
    service,
    group,
    has_geometer,
    has_location,
    has_same_location,
    expected,
):
    application_settings["GEOMETER_FORM_FIELDS"] = ["geometer-v3"]
    application_settings["LOCALIZED_GEOMETER_SERVICE_MAPPING"] = {
        "Test Geometer": [service.pk],
    }

    if not has_location:
        group.locations.remove(sz_instance_with_form.location)

    if has_geometer:
        if not has_same_location:
            sz_instance_with_form.location = location_factory()
            sz_instance_with_form.save()

        form_field_factory(
            instance=sz_instance_with_form, name="geometer-v3", value="Test Geometer"
        )

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

    assert (
        serializer._get_recipients_localized_geometer(sz_instance_with_form) == expected
    )


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
@pytest.mark.parametrize(
    "require_involvement,has_inquiry,should_receive_email",
    [
        (False, False, True),
        (False, True, True),
        (True, False, False),
        (True, True, True),
    ],
)
def test_recipient_involved_in_construction_step(
    db,
    sz_instance,
    notification_template,
    sz_construction_monitoring_settings,
    construction_monitoring_planned_case_sz,
    service,
    mocker,
    require_involvement,
    has_inquiry,
    should_receive_email,
):
    sz_construction_monitoring_settings["NOTIFICATION_RECIPIENTS"] = {
        "construction-step-baubeginn-melden": [
            {
                "service_id": service.pk,
                "require_involvement": require_involvement,
            },
        ],
    }
    mocker.patch.object(sz_instance.__class__, "has_inquiry", return_value=has_inquiry)
    expected = [{"to": service.email}] if should_receive_email else []

    serializer = PermissionlessNotificationTemplateSendmailSerializer(
        data={
            "recipient_types": ["involved_in_construction_step"],
            "instance": {"type": "instances", "id": sz_instance.pk},
            "work_item": {
                "type": "work-items",
                "id": construction_monitoring_planned_case_sz.work_items.filter(
                    task="construction-step-baubeginn-melden"
                )
                .first()
                .pk,
            },
            "notification_template": {
                "type": "notification-templates",
                "id": notification_template.pk,
            },
        }
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()

    assert (
        serializer._get_recipients_involved_in_construction_step(sz_instance)
        == expected
    )
