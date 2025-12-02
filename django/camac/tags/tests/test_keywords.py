import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("Applicant", 0), ("Municipality", 1), ("Service", 1), ("Support", 3)],
)
def test_keyword_list(admin_client, keyword_factory, service, expected_count):
    keyword_factory(service=service)
    keyword_factory.create_batch(2)

    response = admin_client.get(reverse("keyword-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize(
    "exclude_instance,expected_count",
    [(False, 3), (True, 2)],
)
def test_keyword_list_exclude_instance(
    admin_client,
    instance_factory,
    keyword_factory,
    exclude_instance,
    expected_count,
):
    i1 = instance_factory()
    i2 = instance_factory()
    k1 = keyword_factory()
    k2 = keyword_factory()
    k3 = keyword_factory()

    k1.instances.set([i1])
    k2.instances.set([i2])
    k3.instances.set([i2])

    filters = {}
    if exclude_instance:
        filters = {"exclude_instance": str(i1.pk)}
    response = admin_client.get(reverse("keyword-list"), filters)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count


@pytest.mark.parametrize(
    "role__name,expected_count",
    [("Municipality", 1), ("Service", 1)],
)
def test_keyword_visibility(
    admin_client,
    active_inquiry_factory,
    gr_instance,
    keyword_factory,
    service_factory,
    service,
    expected_count,
):
    active_inquiry_factory(gr_instance, service)
    own_keyword = keyword_factory(service=service)
    own_keyword.instances.add(gr_instance)

    other_service = service_factory()
    active_inquiry_factory(gr_instance, other_service)
    hidden_keyword = keyword_factory(service=other_service)
    hidden_keyword.instances.add(gr_instance)

    response = admin_client.get(reverse("keyword-list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["data"]) == expected_count

    response = admin_client.get(reverse("instance-detail", args=[gr_instance.pk]))

    assert response.status_code == status.HTTP_200_OK
    assert (
        response.json()["data"]["relationships"]["keywords"]["meta"]["count"]
        == expected_count
    )
