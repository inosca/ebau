import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,localized,group_visibility,count",
    [
        ("Applicant", False, False, 0),
        ("Service", False, True, 2),
        ("Service", False, False, 1),
        ("Municipality", True, False, 1),
        ("Reader", False, False, 0),
        ("Support", False, False, 0),
        ("PublicReader", False, False, 0),
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
    group_visibility,
):
    service_group = service_group_factory()
    application_settings["SERVICE_GROUPS_FOR_DISTRIBUTION"] = {
        "roles": {role.name: [{"id": service_group.pk, "localized": localized}]},
        "groups": (
            {group.pk: [{"id": service_group.pk, "localized": localized}]}
            if group_visibility
            else {}
        ),
    }

    # Service not applicable for distribution
    service_factory()

    # Role "Service" can invite subservice
    service_factory(service_parent=service)

    # Role "Municipality" cannot invite service due to different location
    # Configured group can invite service of allowed service_group
    service_1 = service_factory(service_group=service_group)
    group_1 = group_factory(service=service_1)
    group_location_factory(location=location_factory(), group=group_1)

    # Role "Municipality" and configured group cannot invite service
    # due to wrong service group
    service_2 = service_factory()
    group_2 = group_factory(service=service_2)
    group_location_factory(location=group.locations.first(), group=group_2)

    # Role "Municipality" and configured group can invite service of
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


@pytest.mark.parametrize(
    "role__name",
    [
        ("Sekretariat der Gemeindebaubehörde"),
        ("Koordinationsstelle Baudirektion BD"),
    ],
)
def test_ur_municipality_coordination_suggestions(
    admin_client,
    role,
    service_factory,
    service_group_factory,
    set_application_ur,
    mocker,
    application_settings,
):
    koor_service_group = service_group_factory(name="Koordinationsstellen")

    koor_bg = service_factory(name="ARE KOOR BG", service_group=koor_service_group)
    koor_np = service_factory(name="ARE KOOR NP", service_group=koor_service_group)
    koor_bd = service_factory(name="ARE KOOR BD", service_group=koor_service_group)

    application_settings["SERVICE_GROUPS_FOR_DISTRIBUTION"]["roles"][
        "Sekretariat der Gemeindebaubehörde"
    ] = [{"id": koor_service_group.pk, "localized": False}]

    mocker.patch(
        "camac.user.filters.uri_constants.KOOR_SERVICE_IDS",
        [koor_bg.pk, koor_np.pk, koor_bd.pk],
    )
    mocker.patch(
        "camac.user.filters.uri_constants.KOOR_BG_SERVICE_ID",
        koor_bg.pk,
    )
    mocker.patch(
        "camac.user.filters.uri_constants.KOOR_NP_SERVICE_ID",
        koor_np.pk,
    )

    response = admin_client.get(
        reverse("publicservice-list"),
        {
            "available_in_distribution": True,
            "service_group_name": ["Koordinationsstellen"],
        },
    )

    data = response.json()["data"]

    if role.name == "Sekretariat der Gemeindebaubehörde":
        assert any(
            item["attributes"]["name"] == "ARE KOOR BG" for item in data
        ), "ARE KOOR BG should be visible for municipalities"
        assert any(
            item["attributes"]["name"] == "ARE KOOR NP" for item in data
        ), "ARE KOOR NP should be visible for municipalities"
        assert not any(
            item["attributes"]["name"] == "ARE KOOR BD" for item in data
        ), "ARE KOOR BD should not be visible for municipalities"

    if role.name == "Koordinationsstelle Baudirektion BD":
        assert any(
            item["attributes"]["name"] == "ARE KOOR BG" for item in data
        ), "ARE KOOR BG should always be visible for KOORS"
        assert any(
            item["attributes"]["name"] == "ARE KOOR NP" for item in data
        ), "ARE KOOR NP should always be visible for KOORS"
        assert any(
            item["attributes"]["name"] == "ARE KOOR BD" for item in data
        ), "ARE KOOR BD should always be visible for KOORS"


@pytest.mark.parametrize(
    "service_group__name,is_authority,expected_services",
    [
        ("service", False, {"subservice-1", "service-1"}),
        ("municipality", True, {"subservice-1", "service-2", "service-3"}),
        ("municipality", False, {"subservice-1"}),
    ],
)
def test_distribution_services(
    admin_client,
    service_factory,
    service,
    instance,
    distribution_settings,
    mocker,
    is_authority,
    expected_services,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if is_authority else service_factory(),
    )

    distribution_settings["AVAILABLE_SERVICES_FOR_INQUIRY"] = {
        "service": [{"include": [("service_groups", ["service"])]}],
        "authority": [
            {"include": [("service_groups", ["external"]), ("services", ["service-3"])]}
        ],
    }

    for slug, service_group_name, service_parent in [
        ("service-1", "service", None),
        ("service-2", "external", None),
        ("service-3", "some-other", None),
        ("subservice-1", "service", service),
        ("subservice-2", "service", service_factory()),
    ]:
        service_factory(
            slug=slug,
            name=slug,
            service_group__name=service_group_name,
            service_parent=service_parent,
        )

    response = admin_client.get(
        reverse("publicservice-list"),
        {
            "available_in_distribution_for_instance": instance.pk,
            "exclude_own_service": True,
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert (
        set([i["attributes"]["name"] for i in response.json()["data"]])
        == expected_services
    )
