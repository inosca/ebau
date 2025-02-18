import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "has_service,expected_status",
    [
        (True, status.HTTP_201_CREATED),
        (False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_template_creation(
    db,
    admin_client,
    expected_status,
    group,
    has_service,
    service_factory,
):
    if not has_service:
        group.service = None
        group.save()

    data = {
        "type": "sanction-templates",
        "id": None,
        "attributes": {
            "name": "foo",
            "description": "bar",
            "control_step": "baufreigabe",
        },
        "relationships": {
            "assigned_service": {
                "data": {
                    "type": "services",
                    "id": str(service_factory().pk),
                },
            },
        },
    }
    response = admin_client.post(reverse("sanction-template-list"), {"data": data})

    assert response.status_code == expected_status


def test_template_list(db, admin_client, sanction_template_factory, service):
    sanction_template_factory()
    visible = sanction_template_factory(created_by_service=service)

    response = admin_client.get(reverse("sanction-template-list"))

    assert response.status_code == status.HTTP_200_OK
    result = response.json()["data"]
    assert len(result) == 1
    assert str(visible.pk) == result[0]["id"]
