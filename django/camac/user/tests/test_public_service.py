import pytest
from django.urls import reverse
from rest_framework import status

from camac.user.models import ServiceRelation


def test_public_service_list(admin_client, service, service_factory):
    service_factory()

    response = admin_client.get(reverse("publicservice-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == 2


@pytest.mark.parametrize(
    "service_t__name,service_t__language", [("je ne sais pas", "fr")]
)
def test_public_service_list_multilingual(admin_client, service_t, multilang):
    url = reverse("publicservice-list")

    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE=service_t.language)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["data"][0]["attributes"]["name"] == service_t.name


@pytest.mark.parametrize(
    "exclude_own_service,expected_count", [(True, 1), (False, 2), ("", 2)]
)
def test_public_service_filter_exclude_own_service(
    admin_client, service_factory, service, exclude_own_service, expected_count
):
    service_factory()

    response = admin_client.get(
        reverse("publicservice-list"), data={"exclude_own_service": exclude_own_service}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == expected_count
    assert bool(service.pk in [int(entry["id"]) for entry in data]) != bool(
        exclude_own_service
    )


@pytest.mark.parametrize(
    "service_name,expected_count", [("ABC", 1), ("DEF", 1), ("", 3)]
)
def test_public_service_filter_service_name(
    admin_client, service_factory, service_name, expected_count
):
    service_factory(name="Test ABC")
    service_factory(name="Test DEF")

    response = admin_client.get(
        reverse("publicservice-list"), data={"service_name": service_name}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == expected_count


@pytest.mark.parametrize(
    "service_name,language, expected_count",
    [("ABC", "de", 1), ("DEF", "de", 1), ("", "de", 3)],
)
def test_public_service_filter_service_name_multlang(
    admin_client, service_t_factory, multilang, service_name, language, expected_count
):
    service_t_factory(language=language, name="Test ABC")
    service_t_factory(language=language, name="Test DEF")

    response = admin_client.get(
        reverse("publicservice-list"),
        HTTP_ACCEPT_LANGUAGE=language,
        data={"service_name": service_name},
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == expected_count


@pytest.mark.parametrize("service__name", [""])
@pytest.mark.parametrize(
    "language,search,expected",
    [
        ("de", "fr", 0),
        ("de", "de", 1),
        ("fr", "fr", 1),
        ("fr", "de", 0),
    ],
)
def test_public_service_multilingual_search(
    admin_client,
    service,
    service_t_factory,
    multilang,
    language,
    search,
    expected,
):
    service_t_factory(language="de", service=service, name="de")
    service_t_factory(language="fr", service=service, name="fr")

    response = admin_client.get(
        reverse("publicservice-list"),
        HTTP_ACCEPT_LANGUAGE=language,
        data={"search": search},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected


@pytest.mark.parametrize(
    "function,use_other_service, expect_result",
    [
        ("geometer", False, 1),
        ("geometer", True, 0),
        ("dummy_function", True, 0),
        ("dummy_function", False, 0),
    ],
)
def test_public_service_filter_provider_for(
    admin_client, service_factory, service, function, use_other_service, expect_result
):
    geometer_service = service_factory()
    dummy_service = service_factory()
    ServiceRelation.objects.create(
        provider=geometer_service, receiver=service, function="geometer"
    )

    response = admin_client.get(
        reverse("publicservice-list"),
        data={
            "provider_for": f"{function};{dummy_service.pk if use_other_service else service.pk}"
        },
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expect_result
    if expect_result:
        assert (
            response.json()["data"][0]["attributes"]["name"]
            == geometer_service.get_name()
        )


@pytest.mark.parametrize(
    "function, use_other_instance, expect_result",
    [
        ("geometer", False, 1),
        ("geometer", True, 0),
        ("dummy_function", True, 0),
        ("dummy_function", False, 0),
    ],
)
def test_public_service_filter_provider_for_instance_municipality(
    admin_client,
    service_factory,
    instance_service_factory,
    instance_factory,
    function,
    use_other_instance,
    expect_result,
):
    service = service_factory(service_group__name="municipality")

    instance = instance_service_factory(service=service).instance
    other_instance = instance_service_factory(
        service__service_group=service.service_group
    ).instance

    geometer_service = service_factory()
    ServiceRelation.objects.create(
        provider=geometer_service, receiver=service, function="geometer"
    )

    filter_by_instance = other_instance.pk if use_other_instance else instance.pk

    response = admin_client.get(
        reverse("publicservice-list"),
        data={"provider_for_instance_municipality": f"{function};{filter_by_instance}"},
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expect_result
    if expect_result:
        assert (
            response.json()["data"][0]["attributes"]["name"]
            == geometer_service.get_name()
        )


@pytest.mark.parametrize(
    "role__name,has_billing_entries,expected_count",
    [("Municipality", True, 1), ("Muncipality", False, 3), ("Municipality", "", 3)],
)
def test_public_service_filter_has_billing_entries(
    admin_client,
    service_factory,
    instance,
    billing_v2_entry_factory,
    group_factory,
    instance_service_factory,
    has_billing_entries,
    expected_count,
):
    service_1 = service_factory(name="Test ABC")
    service_2 = service_factory(name="Test DEF")
    group_factory(service=service_1)
    group_2 = group_factory(service=service_2)
    instance_service_factory(instance=instance, service=service_1, active=1)
    instance_service_factory(instance=instance, service=service_2, active=0)

    billing_v2_entry_factory(instance=instance, group=group_2)

    response = admin_client.get(
        reverse("publicservice-list"), data={"has_billing_entries": has_billing_entries}
    )

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]

    assert len(data) == expected_count

    service_ids = [str(rec["id"]) for rec in data]
    if has_billing_entries:
        assert str(service_2.pk) in service_ids
        assert str(service_1.pk) not in service_ids
    else:
        assert str(service_2.pk) in service_ids
        assert str(service_1.pk) in service_ids
