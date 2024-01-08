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
