import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "is_authority,has_inquiry,expected_status",
    [
        (True, False, status.HTTP_201_CREATED),
        (False, True, status.HTTP_201_CREATED),
        (False, False, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_sanction_creation(
    admin_client,
    expected_status,
    has_inquiry,
    instance,
    is_authority,
    mocker,
    service_factory,
    service,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if is_authority else service_factory(),
    )
    mocker.patch("camac.instance.models.Instance.has_inquiry", return_value=has_inquiry)

    data = {
        "type": "sanctions",
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
            "instance": {
                "data": {"type": "instances", "id": str(instance.pk)},
            },
        },
    }

    response = admin_client.post(reverse("sanction-list"), {"data": data})

    assert response.status_code == expected_status


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "method,is_controlled,is_created_by_service,is_authority,expected_status",
    [
        ("delete", False, True, False, status.HTTP_204_NO_CONTENT),
        ("delete", False, False, True, status.HTTP_204_NO_CONTENT),
        ("delete", True, True, False, status.HTTP_403_FORBIDDEN),
        ("delete", True, False, True, status.HTTP_403_FORBIDDEN),
        ("patch", False, True, False, status.HTTP_200_OK),
        ("patch", False, False, True, status.HTTP_200_OK),
        ("patch", True, True, False, status.HTTP_403_FORBIDDEN),
        ("patch", True, False, True, status.HTTP_403_FORBIDDEN),
    ],
)
@pytest.mark.django_db
def test_sanction_deletion_and_update(
    admin_client,
    expected_status,
    instance,
    is_authority,
    is_controlled,
    is_created_by_service,
    method,
    mocker,
    new_sanction_factory,
    service_factory,
    service,
):
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if is_authority else service_factory(),
    )

    sanction = new_sanction_factory(instance=instance, controlled=is_controlled)

    if is_created_by_service:
        sanction.created_by_service = service
        sanction.save()

    data = (
        {
            "data": {
                "type": "sanctions",
                "id": str(sanction.pk),
                "attributes": {"name": "Test"},
            }
        }
        if method == "patch"
        else {}
    )

    response = getattr(admin_client, method)(
        reverse("sanction-detail", args=[sanction.pk]), data
    )

    assert response.status_code == expected_status
