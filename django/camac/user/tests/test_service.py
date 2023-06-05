import pytest
from django.urls import reverse
from rest_framework import status

from camac.user.models import Service


@pytest.mark.parametrize(
    "role__name,size",
    [
        ("Applicant", 0),
        ("Service", 1),
        ("Canton", 1),
        ("Municipality", 1),
        ("Coordination", 1),
        ("Reader", 1),
    ],
)
def test_service_list(admin_client, service, size):
    url = reverse("service-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["attributes"]["name"] == service.name
        assert json["data"][0]["attributes"]["city"] == service.get_trans_attr("city")


@pytest.mark.parametrize(
    "role__name,role_t__name,role__group_prefix,role_t__group_prefix,status_code",
    [
        ("Applicant", "Applicant", None, None, status.HTTP_404_NOT_FOUND),
        (
            "Municipality",
            "Municipality",
            "Leitung",
            "Leitung",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Administration Leitbehörde",
            "Administration Leitbehörde",
            None,
            None,
            status.HTTP_200_OK,
        ),
        (
            "Administration Leitbehörde",
            "Administration Leitbehörde",
            "Administration",
            "Administration",
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.parametrize(
    "service_t__name,service_t__description,service_t__city",
    [("service name", "service name", "city name")],
)
@pytest.mark.parametrize(
    "service_t__language,role_t__language,group_t__language", [("de",) * 3, ("fr",) * 3]
)
@pytest.mark.parametrize("service__name,group__name", [(None, None)])
@pytest.mark.parametrize("multilang", [True, False])
def test_service_update(
    admin_client,
    service,
    service_t,
    group,
    group_t,
    role,
    role_t,
    status_code,
    multilang,
    application_settings,
):
    if multilang:
        application_settings["IS_MULTILINGUAL"] = True
        group_t.name = f"{role_t.name} {service_t.name}"
        group_t.save()
    else:
        group.name = f"{role_t.name} {service_t.name}"
        group.save()
    service.groups.add(group)
    url = reverse("service-detail", args=[service.pk])
    data = {
        "data": {
            "type": "services",
            "id": service.pk,
            "attributes": {
                "name": "new service name",
                "description": "new service name",
                "city": "new city name",
            },
        }
    }
    response = admin_client.patch(
        url, data=data, HTTP_ACCEPT_LANGUAGE=service_t.language
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        service.refresh_from_db()
        assert service.get_name() == "new service name"
        if role_t.group_prefix:
            assert (
                service.groups.first().get_name()
                == f"{role_t.group_prefix} new service name"
            )
        else:
            assert service.groups.first().get_name() == "new service name"
        if multilang:
            service_t.refresh_from_db()
            assert service_t.description == service_t.name == "new service name"
            assert service_t.city == "new city name"
        else:
            assert service.name == "new service name"
            assert service.city == "new city name"


@pytest.mark.parametrize(
    "role__name,allowed_roles,same_service,status_code",
    [
        ("Municipality", None, False, status.HTTP_403_FORBIDDEN),
        ("Municipality", ["Municipality"], True, status.HTTP_200_OK),
        ("Municipality", ["some other role"], True, status.HTTP_403_FORBIDDEN),
        ("Municipality", None, True, status.HTTP_200_OK),
    ],
)
def test_service_update_permissions(
    admin_client,
    service,
    service_factory,
    status_code,
    application_settings,
    allowed_roles,
    same_service,
):
    application_settings.pop("SERVICE_UPDATE_ALLOWED_ROLES", None)
    if allowed_roles:
        application_settings["SERVICE_UPDATE_ALLOWED_ROLES"] = allowed_roles

    if not same_service:
        service = service_factory()

    url = reverse("service-detail", args=[service.pk])
    response = admin_client.patch(url)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name",
    ["Municipality"],
)
@pytest.mark.parametrize(
    "email,success",
    [
        ("not.an.email", False),
        (" VALID@eXample.COM", True),
        ("foo@bar.ch, nope@, x@y.com", False),
    ],
)
def test_service_update_invalid_email(
    admin_client, service, application_settings, email, success
):
    application_settings["SERVICE_UPDATE_ALLOWED_ROLES"] = ["Municipality"]
    url = reverse("service-detail", args=[service.pk])
    old_email = service.email
    data = {
        "data": {
            "type": "services",
            "id": service.pk,
            "attributes": {
                "email": email,
                "description": "service name",
                "city": "city name",
            },
        }
    }
    response = admin_client.patch(url, data=data)

    expected_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
    assert response.status_code == expected_status
    service.refresh_from_db()
    expected_email = email.lower().strip() if success else old_email
    assert service.email == expected_email


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Coordination", status.HTTP_403_FORBIDDEN),
    ],
)
def test_service_delete(admin_client, service, status_code):
    url = reverse("service-detail", args=[service.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "service_t__name,service_t__language", [("je ne sais pas", "fr")]
)
@pytest.mark.parametrize(
    "role__name,size", [("Applicant", 0), ("Canton", 1), ("Service", 1)]
)
def test_service_list_multilingual(admin_client, service_t, size, multilang):
    url = reverse("service-list")

    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE=service_t.language)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["attributes"]["name"] == service_t.name


@pytest.mark.parametrize("multilang", [True, False])
@pytest.mark.parametrize(
    "name,expected_status",
    [
        ("Subservice 1", status.HTTP_201_CREATED),
        ("Existing", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_service_create(
    admin_client,
    application_settings,
    expected_status,
    multilang,
    name,
    role_t,
    role,
    service_factory,
    service,
):
    if multilang:
        application_settings["IS_MULTILINGUAL"] = True
        role_t.group_prefix = ""
        role_t.save()
        service_factory(trans__name="Existing", trans__language="de")
    else:
        role.group_prefix = ""
        role.save()
        service_factory(name="Existing")

    application_settings["SUBSERVICE_ROLES"] = [role.name]

    data = {
        "data": {
            "id": None,
            "type": "services",
            "attributes": {
                "name": name,
                "email": "test@example.com",
                "description": name,
                "city": "Musterhausen",
                "notification": True,
            },
        }
    }

    response = admin_client.post(reverse("service-list"), data=data)

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        new_service = Service.objects.get(pk=response.json()["data"]["id"])
        new_group = new_service.groups.first()

        if multilang:
            assert new_service.name is None
            assert new_group.name is None

        assert new_service.get_name() == name
        assert new_group.get_name() == name

        assert new_service.service_parent == service
        assert new_service.service_group == service.service_group
