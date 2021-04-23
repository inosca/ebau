from django.urls import reverse
from rest_framework import status


def test_public_user_list(admin_client, user):

    response = admin_client.get(reverse("publicuser-list"))

    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    assert len(data) == 2


def test_public_user_username_filter(admin_client, user):
    url = reverse("publicuser-list")

    response = admin_client.get(url, data={"username": user.username})

    assert response.status_code == status.HTTP_200_OK
    data = response.json()["data"]
    assert len(data) == 1
    assert data[0]["attributes"]["username"] == user.username


def test_public_user_service_filter(
    admin_client,
    user_group_factory,
    service_factory,
    group_factory,
):
    url = reverse("publicuser-list")

    service1 = service_factory()
    service2 = service_factory()

    user_group_factory(group__service=service1)
    user_group_factory(group__service=service1)
    user_group_factory(group__service=service1)
    user_group_factory(group__service=service2)

    response1 = admin_client.get(url, data={"service": service1.pk})
    response2 = admin_client.get(url, data={"service": service2.pk})
    response3 = admin_client.get(
        url,
        data={
            "service": ",".join(
                [
                    str(service1.pk),
                    str(service2.pk),
                ],
            )
        },
    )

    assert response1.status_code == status.HTTP_200_OK
    assert response2.status_code == status.HTTP_200_OK
    assert response3.status_code == status.HTTP_200_OK

    assert len(response1.json()["data"]) == 3
    assert len(response2.json()["data"]) == 1
    assert len(response3.json()["data"]) == 4
