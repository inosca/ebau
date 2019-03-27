import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.instance import serializers


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role__name,instance__user,num_queries,editable",
    [
        ("Applicant", LazyFixture("admin_user"), 9, {"instance", "form", "document"}),
        # reader should see instances from other users but has no editables
        ("Reader", LazyFixture("user"), 9, set()),
        ("Canton", LazyFixture("user"), 9, {"form", "document"}),
        ("Municipality", LazyFixture("user"), 9, {"form", "document"}),
        ("Service", LazyFixture("user"), 9, {"form", "document"}),
    ],
)
def test_instance_list(
    admin_client,
    instance,
    activation,
    num_queries,
    group,
    django_assert_num_queries,
    editable,
    group_location_factory,
):
    url = reverse("bern-instance-list")

    # verify that two locations may be assigned to group
    group_location_factory(group=group)

    included = serializers.InstanceSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url,
            data={
                "include": ",".join(included.keys()),
                "creation_date_before": "17.04.2018",
                "creation_date_after": "17.04.2018",
            },
        )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(instance.pk)
    assert set(json["data"][0]["meta"]["editable"]) == set(editable)
    # included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1
