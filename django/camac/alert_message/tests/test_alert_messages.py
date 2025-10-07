import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "alert_message_list,expected_count",
    [
        ([], 0),
        (
            [
                {"active": True},
                {"active": False},
            ],
            1,
        ),
        (
            [
                {"active": True},
                {"active": True},
            ],
            2,
        ),
    ],
)
def test_alert_messages_show_filter(
    db,
    admin_client,
    alert_message_factory,
    alert_message_list,
    expected_count,
):
    """Test the alert messages filtering by active status."""
    for alert_message in alert_message_list:
        alert_message_factory(**alert_message)

    response = admin_client.get(reverse("alert-message-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == expected_count


@pytest.mark.freeze_time("2025-05-19T12:00:00Z")
def test_alert_messages_date_filter(db, admin_client, alert_message_factory):
    """Test the alert messages filtering by date range."""
    alert_message_factory(
        active=True,
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z",
    )
    alert_message_factory(
        active=True,
        start_date="2025-01-01T00:00:00Z",
        end_date="2025-12-31T23:59:59Z",
    )
    alert_message_factory(
        active=False,
        start_date="2001-01-01T01:01:01Z",
        end_date="2099-09-09T09:09:09Z",
    )

    response = admin_client.get(reverse("alert-message-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == 1
