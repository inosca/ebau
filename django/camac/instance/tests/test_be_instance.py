import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.applicants.factories import ApplicantFactory
from camac.instance import serializers


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role__name,instance__user,editable",
    [
        ("Service", LazyFixture("user"), {"form", "document"}),
        ("Fachstelle", LazyFixture("user"), {"form", "instance", "document"}),
        ("Support", LazyFixture("user"), {"form", "instance", "document"}),
    ],
)
def test_instance_list(
    admin_client, instance, activation, group, editable, group_location_factory
):

    url = reverse("bern-instance-list")
    included = serializers.InstanceSerializer.included_serializers
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
    # Included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1


@pytest.mark.parametrize(
    "instance_state__name,instance__creation_date",
    [("new", "2018-04-17T09:31:56+02:00")],
)
@pytest.mark.parametrize(
    "role__name,instance__user,editable",
    [("Applicant", LazyFixture("admin_user"), {"form", "instance", "document"})],
)
def test_instance_list_as_applicant(
    admin_client,
    admin_user,
    instance,
    activation,
    group,
    editable,
    group_location_factory,
):

    ApplicantFactory(instance=instance, user=admin_user, invitee=admin_user)

    url = reverse("bern-instance-list")
    included = serializers.InstanceSerializer.included_serializers
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
    # Included previous_instance_state and instance_state are the same
    assert len(json["included"]) == len(included) - 1
