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
@pytest.mark.django_db
def test_alert_messages_show_filter(
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
@pytest.mark.django_db
def test_alert_messages_date_filter(admin_client, alert_message_factory, snapshot):
    """Test the alert messages filtering by date range."""
    # alert message from the past (should be filtered out)
    alert_message_factory(
        id=1,
        active=True,
        start_date="2024-01-01T00:00:00Z",
        end_date="2024-12-31T23:59:59Z",
    )

    # alert message currently active (should be included)
    alert_message_factory(
        id=2,
        active=True,
        start_date="2025-01-01T00:00:00Z",
        end_date="2025-12-31T23:59:59Z",
    )

    # inactive alert message (should be filtered out)
    alert_message_factory(
        id=3,
        active=False,
        start_date="2001-01-01T01:01:01Z",
        end_date="2099-09-09T09:09:09Z",
    )

    # alert message with only start_date set (no end_date) - should be included
    alert_message_factory(
        id=4,
        active=True,
        start_date="2025-01-01T00:00:00Z",
        end_date=None,
    )

    # alert message with only end_date set (no start_date) - should be included
    alert_message_factory(
        id=5,
        active=True,
        start_date=None,
        end_date="2025-12-31T23:59:59Z",
    )

    # alert message with neither start_date nor end_date - should be included
    alert_message_factory(
        id=6,
        active=True,
        start_date=None,
        end_date=None,
    )

    # alert message with future start_date - should be filtered out
    alert_message_factory(
        id=7,
        active=True,
        start_date="2025-06-01T00:00:00Z",
        end_date="2025-12-31T23:59:59Z",
    )

    # alert message with past end_date - should be filtered out
    alert_message_factory(
        id=8,
        active=True,
        start_date="2025-01-01T00:00:00Z",
        end_date="2025-05-01T23:59:59Z",
    )

    # alert message with only past end_date set - should be filtered out
    alert_message_factory(
        id=9,
        active=True,
        start_date=None,
        end_date="2025-04-01T23:59:59Z",
    )

    # alert message with only future start_date set - should be filtered out
    alert_message_factory(
        id=10,
        active=True,
        start_date="2025-07-01T00:00:00Z",
        end_date=None,
    )

    response = admin_client.get(reverse("alert-message-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]

    result.sort(key=lambda x: x["id"])

    assert len(result) == 4
    assert result == snapshot
