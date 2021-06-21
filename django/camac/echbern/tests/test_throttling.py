from django.urls import reverse
from rest_framework import status


def test_message_throttling(
    db, service, admin_client, admin_user, group_factory, user_group_factory
):
    group1 = group_factory()
    group2 = group_factory()

    user_group_factory(user=admin_user, group=group1)
    user_group_factory(user=admin_user, group=group2)

    url = reverse("message")

    response1 = admin_client.get(f"{url}?group={group1.pk}")
    response2 = admin_client.get(f"{url}?group={group1.pk}")
    response3 = admin_client.get(f"{url}?group={group2.pk}")

    assert response1.status_code == status.HTTP_204_NO_CONTENT
    assert response2.status_code == status.HTTP_204_NO_CONTENT
    assert response3.status_code == status.HTTP_204_NO_CONTENT
