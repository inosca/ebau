import pytest
from django.urls import reverse
from rest_framework import status

from camac.user.models import Group, UserGroup


@pytest.mark.parametrize(
    "params,status_first,status_second",
    [
        # last param
        (
            {"group": 1, "last": "b91d065e-76a3-4dbd-bd1d-c06ab43612ce"},
            status.HTTP_204_NO_CONTENT,
            status.HTTP_429_TOO_MANY_REQUESTS,
        ),
        # no last param, use group as fallback
        ({"group": 2}, status.HTTP_204_NO_CONTENT, status.HTTP_429_TOO_MANY_REQUESTS),
    ],
)
def test_message_throttling(
    db,
    service,
    admin_client,
    admin_user,
    params,
    set_application_be,
    be_ech0211_settings,
    status_first,
    group_factory,
    status_second,
    reload_ech0211_urls,
):
    group_1 = Group.objects.filter(pk=1).first() or group_factory(pk=1)
    group_2 = Group.objects.filter(pk=2).first() or group_factory(pk=2)
    UserGroup.objects.update_or_create(
        user=admin_user, group=group_1, defaults={"default_group": False}
    )
    UserGroup.objects.update_or_create(
        user=admin_user, group=group_2, defaults={"default_group": False}
    )

    url = reverse("message")

    query = "&".join([f"{key}={value}" for key, value in params.items()])

    for expected_status in [status_first, status_second]:
        response = admin_client.get(f"{url}?{query}")
        assert response.status_code == expected_status
