import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,localized,count",
    [
        ("Applicant", False, 0),
        ("Service", False, 1),
        ("Canton", False, 2),
        ("Municipality", True, 1),
        ("Reader", False, 0),
        ("Support", False, 0),
        ("PublicReader", False, 0),
    ],
)
def test_public_services_for_distribution_list(
    admin_client,
    group,
    role,
    service,
    localized,
    count,
    service_factory,
    service_group_factory,
    group_factory,
    group_location_factory,
    location_factory,
    application_settings,
):
    service_group = service_group_factory()
    application_settings["SERVICE_GROUPS_FOR_DISTRIBUTION"] = {
        f"{role.name}": [{"id": service_group.pk, "localized": localized}]
    }

    # Service not applicable for distribution
    service_factory()

    # Role "Service" can invite subservice
    service_factory(service_parent=service)

    # Role "Municipality" cannot invite service due to different location
    # Role "Canton" can invite service of allowed service group
    service_1 = service_factory(service_group=service_group)
    group_1 = group_factory(service=service_1)
    group_location_factory(location=location_factory(), group=group_1)

    # Role "Municipality" and "Canton" cannot invite service
    # due to wrong service group
    service_2 = service_factory()
    group_2 = group_factory(service=service_2)
    group_location_factory(location=group.locations.first(), group=group_2)

    # Role "Municipality" and "Canton" can invite service of
    # allowed service group in same location
    service_3 = service_factory(service_group=service_group)
    group_3 = group_factory(service=service_3)
    group_location_factory(location=group.locations.first(), group=group_3)

    response = admin_client.get(
        reverse("publicservice-list"), {"available_in_distribution": True}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == count
