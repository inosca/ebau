import functools

import pyexcel
import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.circulation import serializers


@pytest.mark.parametrize(
    "role__name,instance__user,num_queries",
    [
        ("Applicant", LazyFixture("admin_user"), 5),
        ("Canton", LazyFixture("user"), 5),
        ("Municipality", LazyFixture("user"), 8),
        ("Service", LazyFixture("user"), 5),
    ],
)
def test_activation_list(
    admin_client, activation, num_queries, django_assert_num_queries
):
    url = reverse("activation-list")

    included = serializers.ActivationSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(url, data={"include": ",".join(included.keys())})
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(activation.pk)
    assert len(json["included"]) == len(included)


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_activation_detail(admin_client, activation):
    url = reverse("activation-detail", args=[activation.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize("role__name", ["Canton"])
def test_activation_export(
    admin_client,
    user,
    activation_factory,
    django_assert_num_queries,
    form_field_factory,
    instance_state_factory,
):
    url = reverse("activation-export")
    activations = activation_factory.create_batch(2)
    instance_1 = activations[0].circulation.instance
    instance_2 = activations[1].circulation.instance

    instance_1.instance_state = instance_state_factory(pk=1)
    instance_1.save()

    instance_2.instance_state = instance_state_factory(pk=2)
    instance_2.save()

    add_field = functools.partial(form_field_factory, instance=instance_1)
    add_field(
        name="projektverfasser-planer-v2",
        value=[{"name": "Muster Hans"}, {"name": "Beispiel Jean"}],
    )
    add_field(name="bezeichnung", value="Bezeichnung")

    with django_assert_num_queries(4):
        response = admin_client.get(
            url,
            data={
                "instance-state-ids": f"{instance_1.instance_state_id}, {instance_2.instance_state_id}"
            },
        )
    assert response.status_code == status.HTTP_200_OK
    book = pyexcel.get_book(file_content=response.content, file_type="xlsx")
    # bookdict is a dict of tuples(name, content)
    sheet = book.bookdict.popitem()[1]
    assert len(sheet) == len(activations)
    row = sheet[0]
    assert row[4] == "Muster Hans, Beispiel Jean"
    assert row[5] == "Bezeichnung"
