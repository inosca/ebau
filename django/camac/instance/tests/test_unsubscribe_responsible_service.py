import pytest
from django.urls import reverse
from rest_framework import status

from camac.core.models import InstanceService
from camac.permissions import api as permissions_api
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize(
    "role__name,is_active,expected_result",
    [
        ("municipality-lead", 0, status.HTTP_204_NO_CONTENT),
        ("municipality-lead", 1, status.HTTP_403_FORBIDDEN),
        ("support", 1, status.HTTP_204_NO_CONTENT),
        ("support", 0, status.HTTP_204_NO_CONTENT),
    ],
)
def test_unsubscribe_responsible_service(
    db,
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
    "role__name,service_type,instance_services_count_after",
    [
        ("Municipality", "municipality", 4),
        ("Municipality", "construction-control", 4),
        ("Support", "municipality", 2),
        ("Support", "construction-control", 2),
    ],
)
def test_unsubscribe_responsible_service_removes_correct_services(
    db,
    admin_client,
    be_instance,
    application_settings,
    service_type,
    instance_services_count_after,
    instance_service_factory,
    service_factory,
):
    application_settings["ACTIVE_SERVICES"][service_type.upper().replace("-", "_")][
        "FILTERS"
    ] = {"service__service_group__name__in": [service_type]}
    group = admin_client.user.groups.first()
    group.service.instance_services.all().delete()

    group.service.service_group.name = service_type
    group.service.service_group.save()

    instance_service_factory(
        instance=be_instance,
        service=group.service,
        active=0,
    )

    for i in range(0, 2):
        instance_service_factory(
            instance=be_instance,
            service=service_factory(service_group__name="municipality"),
            active=0,
        )
        instance_service_factory(
            instance=be_instance,
            service=service_factory(service_group__name="construction-control"),
            active=0,
        )
    assert InstanceService.objects.all().count() == 5

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
    "access_level_name,expected_status",
    [
        ("lead-authority", status.HTTP_403_FORBIDDEN),
        ("involved-authority", status.HTTP_204_NO_CONTENT),
    ],
)
def test_unsubscribe_responsible_service_with_permission_module(
    db,
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
