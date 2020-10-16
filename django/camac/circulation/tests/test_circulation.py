import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.models import Case, Workflow, WorkItem
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.circulation import serializers


def get_activation_work_item(case, activation_id):
    return case.work_items.get(
        **{"task_id": "activation", "meta__activation-id": activation_id}
    )


@pytest.mark.parametrize(
    "role__name,instance__user,num_queries",
    [
        ("Applicant", LazyFixture("admin_user"), 10),
        ("Canton", LazyFixture("user"), 10),
        ("Municipality", LazyFixture("user"), 9),
        ("Service", LazyFixture("user"), 9),
    ],
)
def test_circulation_list(
    admin_client,
    instance_state,
    circulation,
    activation,
    num_queries,
    django_assert_num_queries,
):
    url = reverse("circulation-list")

    included = serializers.CirculationSerializer.included_serializers
    with django_assert_num_queries(num_queries):
        response = admin_client.get(
            url,
            data={
                "instance_state": instance_state.pk,
                "include": ",".join(included.keys()),
            },
        )
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(circulation.pk)
    assert len(json["included"]) == len(included)


@pytest.mark.parametrize(
    "role__name,instance__user", [("Applicant", LazyFixture("admin_user"))]
)
def test_circulation_detail(admin_client, circulation):
    url = reverse("circulation-detail", args=[circulation.pk])

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "url,method,expected_status",
    [
        ("circulation-list", "get", status.HTTP_200_OK),
        ("circulation-list", "post", status.HTTP_405_METHOD_NOT_ALLOWED),
        ("circulation-detail", "get", status.HTTP_200_OK),
        ("circulation-detail", "patch", status.HTTP_403_FORBIDDEN),
        ("circulation-detail", "delete", status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
)
def test_circulation_permissions(
    admin_client, circulation, url, method, expected_status
):
    assert (
        getattr(admin_client, method)(
            reverse(url, **({"args": [circulation.pk]} if "detail" in url else {}))
        ).status_code
        == expected_status
    )


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
def test_sync_circulation(
    admin_client,
    instance_service,
    circulation,
    activation_factory,
    caluma_workflow_config_be,
):
    user = BaseUser()
    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=user,
        meta={"camac-instance-id": circulation.instance.pk},
    )

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        skip_work_item(
            case.work_items.get(task_id=task_id),
            user,
            context={"circulation-id": circulation.pk},
        )

    circulation_work_item = case.work_items.get(
        **{"task_id": "circulation", "meta__circulation-id": circulation.pk}
    )

    assert not circulation_work_item.child_case

    a1 = activation_factory(circulation=circulation)
    a2 = activation_factory(circulation=circulation)
    a3 = activation_factory(circulation=circulation)

    response = admin_client.patch(reverse("circulation-sync", args=[circulation.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    circulation_work_item.refresh_from_db()
    assert circulation_work_item.child_case.status == Case.STATUS_RUNNING

    for activation in [a1, a2, a3]:
        assert (
            get_activation_work_item(
                circulation_work_item.child_case, activation.pk
            ).status
            == WorkItem.STATUS_READY
        )

    now = timezone.now()
    a2.deadline_date = now
    a2.save()

    a3_pk = a3.pk  # save for later usage
    a3.delete()

    response = admin_client.patch(reverse("circulation-sync", args=[circulation.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    assert (
        get_activation_work_item(circulation_work_item.child_case, a2.pk).deadline
        == now
    )

    assert (
        get_activation_work_item(circulation_work_item.child_case, a3_pk).status
        == WorkItem.STATUS_CANCELED
    )

    a1.delete()
    a2.delete()

    response = admin_client.patch(reverse("circulation-sync", args=[circulation.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    circulation_work_item.refresh_from_db()
    assert circulation_work_item.child_case.status == Case.STATUS_CANCELED
