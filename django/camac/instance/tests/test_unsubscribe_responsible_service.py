import pytest
from django.urls import reverse
from rest_framework import status

from camac.core.models import InstanceService
from camac.permissions import api as permissions_api
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize(
    ("role__name", "is_active", "expected_result"),
    [
        ("municipality-lead", 0, status.HTTP_204_NO_CONTENT),
        ("municipality-lead", 1, status.HTTP_403_FORBIDDEN),
        ("support", 1, status.HTTP_204_NO_CONTENT),
        ("support", 0, status.HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.django_db
def test_unsubscribe_responsible_service(
    application_settings,
    admin_client,
    be_instance,
    role,
    be_permissions_settings,
    instance_service_factory,
    is_active,
    expected_result,
    instance_acl_factory,
    access_level_factory,
    instance_state_factory,
    service_factory,
    be_change_responsible_service_settings,
):
    application_settings["SHORT_NAME"] = "be"
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.PermissionEventHandlerBE"
    )
    access_level_factory(slug="lead-authority")
    access_level_factory(slug="involved-authority")

    be_instance.instance_state = instance_state_factory(name="subm")
    be_instance.save()

    service = admin_client.user.groups.first().service
    # make sure that no other instance services are around for test
    be_instance.instance_services.all().delete()

    instance_service = instance_service_factory(
        instance=be_instance, service=service, active=is_active
    )

    instance_acl_factory(
        instance=be_instance,
        access_level_id="lead-authority" if is_active else "involved-authority",
        service=service,
    )

    if role.name == "support":
        access_level_factory(slug="support")
        instance_acl_factory(
            instance=be_instance,
            access_level_id="support",
            service=service,
        )
        # support isn't the lead authority / involved lead authority
        instance_service.service = service_factory()
        instance_service.save()

    response = admin_client.post(
        reverse("instance-unsubscribe-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-unsubscribe-responsible-services",
                "attributes": {"service-type": "municipality"},
            }
        },
    )

    assert response.status_code == expected_result


@pytest.mark.parametrize(
    ("role__name", "service_type", "instance_services_count_after"),
    [
        ("municipality-lead", "municipality", 4),
        ("municipality-lead", "construction-control", 4),
        ("support", "municipality", 2),
        ("support", "construction_control", 2),
    ],
)
@pytest.mark.django_db
def test_unsubscribe_responsible_service_removes_correct_services(
    admin_client,
    be_instance,
    set_application_be,
    service_type,
    role,
    instance_services_count_after,
    instance_service_factory,
    service_factory,
    be_change_responsible_service_settings,
    be_permissions_settings,
    access_level_factory,
    instance_acl_factory,
    instance_state_factory,
):
    be_instance.instance_state = instance_state_factory(
        name="sb1" if service_type == "construction-control" else "subm"
    )
    be_instance.save()
    group = admin_client.user.groups.first()
    group.service.instance_services.all().delete()

    group.service.service_group.name = service_type
    group.service.service_group.save()

    involved_construction_control_access_level = access_level_factory(
        slug="involved-construction-control"
    )
    involved_authority_access_level = access_level_factory(slug="involved-authority")
    support_access_level = access_level_factory(slug="support")

    # Support is never an involved lead authority
    if role.name != "support":
        instance_service_factory(
            instance=be_instance,
            service=group.service,
            active=0,
        )

    instance_acl_factory(
        instance=be_instance,
        access_level=support_access_level
        if role.name == "support"
        else involved_authority_access_level
        if service_type == "municipality"
        else involved_construction_control_access_level,
        service=group.service,
    )

    for _ in range(2):
        involved_municipality = service_factory(service_group__name="municipality")
        instance_service_factory(
            instance=be_instance,
            service=involved_municipality,
            active=0,
        )
        instance_acl_factory(
            instance=be_instance,
            access_level=involved_authority_access_level,
            service=group.service,
        )

        involved_construction_control = service_factory(
            service_group__name="construction-control"
        )
        instance_service_factory(
            instance=be_instance,
            service=involved_construction_control,
            active=0,
        )
        instance_acl_factory(
            instance=be_instance,
            access_level=involved_construction_control_access_level,
            service=involved_construction_control,
        )

    assert InstanceService.objects.all().count() == (4 if role.name == "support" else 5)

    admin_client.post(
        reverse("instance-unsubscribe-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-unsubscribe-responsible-services",
                "attributes": {"service-type": service_type},
            }
        },
    )

    assert InstanceService.objects.all().count() == instance_services_count_after


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize(
    ("access_level_name", "expected_status"),
    [
        ("lead-authority", status.HTTP_403_FORBIDDEN),
        ("involved-authority", status.HTTP_204_NO_CONTENT),
    ],
)
@pytest.mark.django_db
def test_unsubscribe_responsible_service_with_permission_module(
    admin_client,
    be_instance,
    be_permissions_settings,
    access_level_factory,
    service,
    access_level_name,
    expected_status,
    service_factory,
    instance_state_factory,
    disable_ech0211_settings,
    be_change_responsible_service_settings,
):
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    be_instance.instance_state = instance_state_factory(name="subm")
    be_instance.save()

    permissions_api.grant(
        be_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level_factory(pk=access_level_name),
        service=service,
    )
    response = admin_client.post(
        reverse("instance-unsubscribe-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-unsubscribe-responsible-services",
                "attributes": {"service-type": "municipality"},
            }
        },
    )
    assert response.status_code == expected_status
