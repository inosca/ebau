import pytest
from django.urls import reverse
from rest_framework import status


def test_instance_mark_list(admin_client, instance_mark_factory):
    instance_mark_factory.create_batch(3)

    response = admin_client.get(reverse("instancemark-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == 3


@pytest.mark.parametrize("service_group__name", ["coordination"])
@pytest.mark.parametrize(
    "role__name,access_level_id,status_code",
    [
        ("Municipality", "lead-authority", status.HTTP_200_OK),
        ("Service", "distribution-service", status.HTTP_200_OK),
        ("Applicant", "applicant", status.HTTP_403_FORBIDDEN),
        ("Support", "support", status.HTTP_403_FORBIDDEN),
    ],
)
def test_instance_mark_link_to_instance(
    admin_client,
    instance_mark_factory,
    instance_acl_factory,
    access_level_id,
    sg_access_levels,
    status_code,
    instance,
    service,
):
    instance_acl_factory(
        instance=instance,
        service=service,
        grant_type="SERVICE",
        access_level_id=access_level_id,
    )

    instance_mark = instance_mark_factory()
    assert instance.instance_marks.count() == 0

    url = reverse("instance-detail", args=[instance.pk])

    data = {
        "data": {
            "type": "instances",
            "id": instance.pk,
            "relationships": {
                "instance-marks": {
                    "data": [{"type": "instance-marks", "id": instance_mark.pk}]
                }
            },
        }
    }

    response = admin_client.patch(url, data=data)

    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        instance.refresh_from_db()
        assert instance.instance_marks.count() == 1
