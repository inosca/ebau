import pytest
from django.urls import reverse
from rest_framework import status

from camac.permissions import api as permissions_api
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "is_active,expected_result",
    [
        (0, status.HTTP_204_NO_CONTENT),
        (1, status.HTTP_403_FORBIDDEN),
    ],
)
def test_unsubscribe_responsible_service(
    db,
    admin_client,
    be_instance,
    be_permissions_settings,
    instance_service_factory,
    is_active,
    expected_result,
    instance_acl_factory,
    access_level_factory,
):
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.GeneralPermissionEventHandlerBE"
    )
    access_level_factory(slug="lead-authority")
    old_responsible = be_instance.instance_services.get(active=1).service
    old_responsible.service_group.name = "lead-authority"
    old_responsible.service_group.save()

    instance_acl_factory(
        instance=be_instance, access_level_id="lead-authority", service=old_responsible
    )
    instance_service_factory(
        service=be_instance.group.service, instance=be_instance, active=is_active
    )

    response = admin_client.post(
        reverse("instance-unsubscribe-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-unsubscribe-responsible-services",
            }
        },
    )

    assert response.status_code == expected_result


@pytest.mark.parametrize("role__name", ["Municipality"])
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
            }
        },
    )
    assert response.status_code == expected_status
