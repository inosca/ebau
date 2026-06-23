import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.django_db
def test_service_available_in_sanctions_filter(admin_client, service_factory):
    enabled_service = service_factory(disabled=False)
    disabled_service = service_factory(disabled=True)

    resp = admin_client.get(
        reverse("service-list"),
        {"available_in_sanctions": 1},
    )

    assert resp.status_code == status.HTTP_200_OK, resp.content

    ids = [int(i["id"]) for i in resp.json()["data"]]

    assert enabled_service.pk in ids
    assert disabled_service.pk not in ids


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "set_available_service_groups,should_contain_unavailable",
    [
        (True, False),
        (False, True),
    ],
)
@pytest.mark.django_db
def test_configured_service_available_in_sanctions_filter(
    admin_client,
    application_settings,
    role,
    service_factory,
    set_available_service_groups,
    sanctions_settings,
    should_contain_unavailable,
):
    if set_available_service_groups:
        sanctions_settings.available_service_groups = ["available-servicegroup"]

    available_service = service_factory(service_group__slug="available-servicegroup")
    unavailable_service = service_factory(
        service_group__slug="unavailable-servicegroup"
    )

    resp = admin_client.get(
        reverse("service-list"),
        {"available_in_sanctions": 1},
    )

    assert resp.status_code == status.HTTP_200_OK, resp.content
    json_data = resp.json()["data"]

    def json_data_contains_service(json_data, service):
        return any(
            entry["type"] == "services" and entry["id"] == str(service.pk)
            for entry in json_data
        )

    assert json_data_contains_service(json_data, available_service)
    if should_contain_unavailable:
        assert json_data_contains_service(json_data, unavailable_service)


@pytest.mark.parametrize(
    "has_pending_sanctions,expected_count", [("1", 6), ("0", 9), ("", 15)]
)
@pytest.mark.django_db
def test_has_pending_sanctions_filter(
    admin_client,
    expected_count,
    has_pending_sanctions,
    instance_factory,
    new_sanction_factory,
):
    # 1 instance with controlled sanctions:
    new_sanction_factory(
        instance=instance_factory(user=admin_client.user),
        controlled=True,
    )

    # 2 instances with pending sanctions:
    for instance in instance_factory.create_batch(2, user=admin_client.user):
        new_sanction_factory(instance=instance, controlled=False)

    # 4 instances with both controlled and pending sanctions:
    for instance in instance_factory.create_batch(4, user=admin_client.user):
        new_sanction_factory(instance=instance, controlled=False)
        new_sanction_factory(instance=instance, controlled=True)

    # 8 instances without any sanctions:
    instance_factory.create_batch(8, user=admin_client.user)

    resp = admin_client.get(
        reverse("instance-list"),
        {"has_pending_sanctions": has_pending_sanctions},
    )

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert len(resp.json()["data"]) == expected_count


@pytest.mark.parametrize(
    "matching_service,controlled,expected_count",
    [(False, False, 0), (False, True, 0), (True, False, 1), (True, True, 0)],
)
@pytest.mark.django_db
def test_pending_sanctions_assigned_to_service_filter(
    admin_client,
    controlled,
    expected_count,
    instance_factory,
    matching_service,
    new_sanction_factory,
    service_factory,
):
    service = service_factory()
    instance = instance_factory(user=admin_client.user)
    new_sanction_factory(
        instance=instance,
        controlled=controlled,
        **({"assigned_service": service} if matching_service else {}),
    )

    resp = admin_client.get(
        reverse("instance-list"),
        {"has_pending_sanctions_assigned_to_service": service.pk},
    )

    assert resp.status_code == status.HTTP_200_OK, resp.content
    assert len(resp.json()["data"]) == expected_count
