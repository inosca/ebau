import json

import pytest
from caluma.caluma_form import (
    models as caluma_form_models,
)
from django.urls import reverse
from rest_framework import status

from camac.utils import build_url


def test_check_password(admin_user):
    assert admin_user.check_password("password")
    assert not admin_user.check_password("invalid")


def test_get_full_name(admin_user):
    admin_user.name = "Hans"
    admin_user.surname = "Muster"

    assert admin_user.get_full_name() == "Hans Muster"


def test_me(admin_client, admin_user, user_group_factory, group_factory):
    admin_user.groups.all().delete()

    user_group_factory(user=admin_user, group=group_factory(disabled=0))
    user_group_factory(user=admin_user, group=group_factory(disabled=1))

    url = reverse("me")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["attributes"]["username"] == admin_user.username
    assert len(json["data"]["relationships"]["groups"]["data"]) == 1


def test_me_group(admin_client, admin_user, service):
    url = reverse("me")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert json["data"]["relationships"]["service"]["data"]["id"] == str(service.pk)


@pytest.mark.parametrize(
    "service_t__name,service_group__name",
    [("Baukontrolle Test", "construction-control")],
)
def test_me_service_municipality(
    admin_client, admin_user, service, mocker, service_factory
):
    url = reverse("me")
    lead_authority = service_factory(
        service_group__name="municipality",
        trans__language="de",
        trans__name="Leitbehörde Test",
    )

    response = admin_client.get(url, data={"include": "service.municipality"})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert (
        int(json["included"][0]["relationships"]["municipality"]["data"]["id"])
        == lead_authority.pk
    )


@pytest.mark.parametrize(
    "role__name,size",
    [
        ("Applicant", 0),
        ("Service", 1),
        ("Canton", 1),
        ("Municipality", 1),
        ("Coordination", 1),
        ("Geometer", 1),
        ("Support", 1),
    ],
)
def test_user_list(admin_client, size):
    url = reverse("user-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size


@pytest.mark.parametrize("role__name,size", [("Service", 2), ("Municipality", 0)])
def test_user_role_filter(
    admin_client,
    admin_user,
    user,
    group,
    user_group_factory,
    group_factory,
    role_factory,
    size,
):
    user_group_factory(user=user, group=group, default_group=1)
    user_group_factory(
        user=user, group=group_factory(role=role_factory(name="Municipality"))
    )

    url = reverse("user-list")

    response = admin_client.get(url, {"exclude_primary_role": "Municipality"})
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size


@pytest.mark.parametrize("role__name", ["Service"])
@pytest.mark.parametrize(
    "responsible_for_instances,expected_count", [(True, 3), (False, 6)]
)
def test_user_responsible_in_service_filter(
    admin_client,
    service,
    user_group_factory,
    responsible_service_factory,
    responsible_for_instances,
    expected_count,
):
    user_group_factory.create_batch(5, group__service=service)

    for user_group in user_group_factory.create_batch(3, group__service=service):
        responsible_service_factory(service=service, responsible_user=user_group.user)

    response = admin_client.get(
        reverse("user-list"), {"responsible_for_instances": responsible_for_instances}
    )

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize(
    "has_permission,expected_status",
    [
        (True, status.HTTP_201_CREATED),
        (False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_user_keycloak_apply(
    set_application_gr,
    gr_user_settings,
    admin_client,
    admin_user,
    mocker,
    gr_instance,
    settings,
    requests_mock,
    has_permission,
    expected_status,
):
    caluma_form_models.Question.objects.create(
        slug="e-mail-gesuchstellerin", type=caluma_form_models.Question.TYPE_TEXT
    )
    requests_mock.get(
        build_url(
            settings.API_HOST, reverse("instance-detail", args=(gr_instance.pk,))
        ),
        json={
            "data": {
                "id": gr_instance.pk,
                "type": "instances",
                "meta": {"permissions": {"main": ["write"] if has_permission else []}},
            }
        },
    )
    mocker.patch(
        "camac.user.authentication.JSONWebTokenKeycloakAuthentication.get_jwt_value",
        lambda self, token: type("token", (bytes,), {"decode": lambda: None}),
    )
    token_value = {
        "sub": admin_user.username,
        "email": admin_user.email,
        "family_name": admin_user.surname,
        "given_name": admin_user.name,
    }
    userinfo = mocker.patch("keycloak.KeycloakOpenID.userinfo")
    userinfo.return_value = token_value

    response = admin_client.post(
        reverse("keycloak-apply"),
        data=json.dumps({"document": str(gr_instance.case.document.pk)}),
        content_type="application/json",
    )

    assert response.status_code == expected_status
    if response.status_code == status.HTTP_201_CREATED:
        assert set(response.json()["questions"]) == {
            "e-mail-gesuchstellerin",
            "vorname-gesuchstellerin",
            "name-gesuchstellerin",
        }

        answers = gr_instance.case.document.answers.all()

        assert (
            answers.get(question_id="e-mail-gesuchstellerin").value
            == token_value["email"]
        )
        assert (
            answers.get(question_id="vorname-gesuchstellerin").value
            == token_value["given_name"]
        )
        assert (
            answers.get(question_id="name-gesuchstellerin").value
            == token_value["family_name"]
        )
