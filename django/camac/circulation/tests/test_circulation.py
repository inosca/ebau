import pytest
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.models import Case, Workflow, WorkItem
from django.urls import reverse
from django.utils import timezone
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.circulation import serializers


def get_activation_work_item(case, activation_id):
    try:
        return case.work_items.get(
            **{"task_id": "activation", "meta__activation-id": activation_id}
        )
    except WorkItem.DoesNotExist:
        return None


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
        ("circulation-detail", "delete", status.HTTP_204_NO_CONTENT),
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
    caluma_admin_user,
    service_factory,
    group_factory,
    role_factory,
    role,
    application_settings,
):
    read_only_role = role_factory(name="read_only")

    application_settings["CALUMA"]["ACTIVATION_EXCLUDE_ROLES"] = [read_only_role.name]

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    circulation.instance.case = case
    circulation.instance.save()

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        skip_work_item(
            case.work_items.get(task_id=task_id),
            caluma_admin_user,
            context={"circulation-id": circulation.pk},
        )

    circulation_work_item = case.work_items.get(
        **{"task_id": "circulation", "meta__circulation-id": circulation.pk}
    )

    assert not circulation_work_item.child_case

    excluded_service = service_factory()
    excluded_service.groups.set([group_factory(role=read_only_role)])

    service = group_factory(role=role).service
    service.groups.add(group_factory(role=read_only_role))

    a1 = activation_factory(
        circulation=circulation,
        circulation_state__name="DONE",
        circulation_answer=None,
        service=service,
    )
    a2 = activation_factory(
        circulation=circulation,
        circulation_state__name="OK",
        service=service,
    )
    a3 = activation_factory(
        circulation=circulation,
        circulation_state__name="RUN",
        service=service,
    )
    a4 = activation_factory(
        circulation=circulation,
        circulation_state__name="IDLE",
        service=service,
    )
    a5 = activation_factory(
        circulation=circulation,
        circulation_state__name="RUN",
        service=excluded_service,
    )

    response = admin_client.patch(reverse("circulation-sync", args=[circulation.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    circulation_work_item.refresh_from_db()
    assert circulation_work_item.child_case.status == Case.STATUS_RUNNING

    assert (
        get_activation_work_item(circulation_work_item.child_case, a1.pk).status
        == WorkItem.STATUS_CANCELED
    )  # done without circulation answer
    assert (
        get_activation_work_item(circulation_work_item.child_case, a2.pk).status
        == WorkItem.STATUS_SKIPPED
    )  # ok (same as done) with activation answer
    assert (
        get_activation_work_item(circulation_work_item.child_case, a3.pk).status
        == WorkItem.STATUS_READY
    )  # run, needs to be ready
    assert (
        get_activation_work_item(circulation_work_item.child_case, a4.pk) is None
    )  # a4 doesn't exist yet since it's idle
    assert (
        get_activation_work_item(circulation_work_item.child_case, a5.pk) is None
    )  # a5 doesn't exist since it's for an excluded service

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

    assert not get_activation_work_item(circulation_work_item.child_case, a3_pk)
    circulation_work_item.child_case.refresh_from_db()
    assert circulation_work_item.child_case.status == Case.STATUS_COMPLETED

    a1.delete()
    a2.delete()
    a4.delete()

    response = admin_client.patch(reverse("circulation-sync", args=[circulation.pk]))
    assert response.status_code == status.HTTP_204_NO_CONTENT

    circulation_work_item.refresh_from_db()
    assert not circulation_work_item.child_case


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
@pytest.mark.parametrize(
    "has_activation,has_other_circulations,instance_state__name,expected_status,expected_work_items",
    [
        (
            True,
            False,
            "circulation_init",
            status.HTTP_403_FORBIDDEN,
            None,
        ),
        (
            False,
            False,
            "circulation_init",
            status.HTTP_204_NO_CONTENT,
            ["init-circulation", "skip-circulation"],
        ),
        (
            False,
            False,
            "circulation",
            status.HTTP_204_NO_CONTENT,
            ["start-circulation", "start-decision"],
        ),
        (
            False,
            True,
            "circulation",
            status.HTTP_204_NO_CONTENT,
            ["start-circulation", "check-activation", "start-decision"],
        ),
    ],
)
def test_delete_circulation(
    admin_client,
    instance_service,
    instance_state,
    circulation,
    circulation_factory,
    caluma_workflow_config_be,
    caluma_admin_user,
    activation_factory,
    has_activation,
    has_other_circulations,
    expected_status,
    expected_work_items,
):
    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    circulation.instance.case = case
    circulation.instance.save()

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        skip_work_item(
            case.work_items.get(task_id=task_id),
            caluma_admin_user,
            context={"circulation-id": circulation.pk},
        )

    if has_activation:
        activation_factory(circulation=circulation)

    if has_other_circulations:
        circulation_factory(instance=circulation.instance)

    response = admin_client.delete(reverse("circulation-detail", args=[circulation.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        assert not case.work_items.filter(
            **{"meta__circulation-id": circulation.pk}
        ).exists()

        for task_id in expected_work_items:
            assert case.work_items.filter(
                task_id=task_id,
                status=WorkItem.STATUS_READY,
            ).exists()


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
def test_end_circulation(
    admin_client,
    instance_service,
    circulation,
    activation,
    caluma_workflow_config_be,
    caluma_admin_user,
    circulation_state,
    notification_template,
    application_settings,
):
    application_settings["NOTIFICATIONS"] = {
        "END_CIRCULATION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["unanswered_activation"],
            }
        ]
    }

    application_settings["CIRCULATION_STATE_END"] = circulation_state.name

    case = start_case(
        workflow=Workflow.objects.get(pk="building-permit"),
        form=Form.objects.get(pk="main-form"),
        user=caluma_admin_user,
    )
    circulation.instance.case = case
    circulation.instance.save()

    for task_id in ["submit", "ebau-number", "init-circulation"]:
        skip_work_item(
            case.work_items.get(task_id=task_id),
            caluma_admin_user,
            context={"circulation-id": circulation.pk},
        )

    response = admin_client.patch(reverse("circulation-end", args=[circulation.pk]))

    activation.refresh_from_db()

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert activation.circulation_state == circulation_state
    assert (
        case.work_items.get(**{"meta__circulation-id": circulation.pk}).status
        == WorkItem.STATUS_SKIPPED
    )


@pytest.mark.parametrize(
    "role__name,instance__user", [("Municipality", LazyFixture("admin_user"))]
)
def test_prematurely_end_circulation(
    db,
    role,
    instance_service,
    caluma_workflow_config_be,
    admin_client,
    init_circulation_with_activations,
    instance,
    be_instance,
    circulation_state_factory,
    caluma_admin_user,
    notification_template,
    application_settings,
):
    application_settings["NOTIFICATIONS"] = {
        "END_CIRCULATION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["unanswered_activation"],
            }
        ]
    }
    state_done = circulation_state_factory(name="DONE")
    application_settings["CIRCULATION_STATE_DONE_ID"] = state_done.pk

    state_inprogress = circulation_state_factory(name="WORKING")
    circulation_to_end = init_circulation_with_activations(
        be_instance, instance_service.service, (state_done, state_inprogress)
    )
    another_circulation = init_circulation_with_activations(
        be_instance, instance_service.service, (state_inprogress, state_inprogress)
    )

    admin_client.patch(reverse("circulation-end", args=[circulation_to_end.pk]))

    assert all(
        [
            a.circulation_state == state_done
            for a in circulation_to_end.activations.all()
        ]
    )
    assert all(
        [
            a.circulation_state == state_inprogress
            for a in another_circulation.activations.all()
        ]
    )
