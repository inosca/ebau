import pytest
from django.urls import reverse
from rest_framework import status


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
    user_group_factory,
    params,
    status_first,
    status_second,
):
    user_group_factory(user=admin_user, group__pk=1)
    user_group_factory(user=admin_user, group__pk=2)

    url = reverse("message")

    query = "&".join([f"{key}={value}" for key, value in params.items()])

    for expected_status in [status_first, status_second]:
        response = admin_client.get(f"{url}?{query}")
        assert response.status_code == expected_status
