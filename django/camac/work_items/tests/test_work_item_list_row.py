from datetime import date

import pytest
from caluma.caluma_workflow.models import Task, WorkItem
from django.urls import reverse
from django.utils.timezone import now
from faker import Faker
from rest_framework import status

from camac.caluma.utils import date_to_deadline

fake = Faker()


def normalize_response(response):
    for row in response["data"]:
        row["attributes"]["instance-id"] = "<INSTANCE_ID>"
        row["attributes"]["edit-link"]["models"][0] = "<INSTANCE_ID>"
        row["relationships"]["addressed-service"]["data"]["id"] = "<SERVICE_ID>"

        if row["attributes"]["direct-link"] is not None:
            row["attributes"]["direct-link"]["models"][0] = "<INSTANCE_ID>"
        if row["relationships"]["assigned-user"]["data"] is not None:
            row["relationships"]["assigned-user"]["data"]["id"] = "<USER_ID>"
        if row["relationships"]["closed-by-user"]["data"] is not None:
            row["relationships"]["closed-by-user"]["data"]["id"] = "<USER_ID>"

    return response


@pytest.fixture
def work_item_list_row_factory(db, caluma_work_item_factory, service_factory, request):
    def wrapper(canton="ag", addressed=None, controlling=None, assigned=None, **kwargs):
        master_data_case = request.getfixturevalue(f"{canton.lower()}_master_data_case")

        request.getfixturevalue(f"{canton.lower()}_distribution_settings")
        request.getfixturevalue(f"{canton.lower()}_work_item_list_settings")

        addressed = addressed if addressed else service_factory()
        controlling = controlling if controlling else service_factory()

        return caluma_work_item_factory(
            case=master_data_case,
            pk=fake.uuid4(),
            deadline=date_to_deadline(date.fromisoformat(fake.date())),
            child_case=None,
            addressed_groups=[str(addressed.pk)],
            controlling_groups=[str(controlling.pk)],
            assigned_users=[str(assigned.username)] if assigned else [],
            status=kwargs.pop("status", WorkItem.STATUS_READY),
            meta=kwargs.pop("meta", {"not-viewed": True}),
            **kwargs,
        )

    return wrapper


@pytest.fixture
def setup_work_item_list(
    service,
    user,
    work_item_list_row_factory,
    user_factory,
    caluma_task_factory,
    work_item_template_factory,
    work_item_list_filter_preset,
):
    task = caluma_task_factory(
        meta={
            "directLink": {
                "route": "foo.bar.baz",
                "models": ["INSTANCE_ID", "TASK_SLUG"],
            }
        }
    )
    template = work_item_template_factory()

    work_item_list_filter_preset.prefilter_tasks = True
    work_item_list_filter_preset.prefilter_work_item_templates = True
    work_item_list_filter_preset.tasks.add(task)
    work_item_list_filter_preset.work_item_templates.add(template)
    work_item_list_filter_preset.save()

    def wrapper(canton="ag"):
        work_item_list_row_factory(
            canton=canton,
            name="not-visible",
        )
        work_item_list_row_factory(
            canton=canton,
            addressed=service,
            meta={
                "not-viewed": False,
                "template-id": str(template.pk),
                "imported": True,
            },
            name="from-template-and-read",
        )
        work_item_list_row_factory(
            canton=canton,
            name="controlling",
            controlling=service,
            task_id=task,
        )
        work_item_list_row_factory(
            canton=canton,
            name="assigned",
            addressed=service,
            assigned=user,
        )
        work_item_list_row_factory(
            canton=canton,
            name="completed",
            addressed=service,
            status=WorkItem.STATUS_COMPLETED,
            closed_by_user=user_factory().username,
            closed_at=now(),
        )

        return task, template, work_item_list_filter_preset

    return wrapper


def test_work_item_list_row_list_no_pagination(admin_client, setup_work_item_list):
    setup_work_item_list()
    response = admin_client.get(reverse("work-item-list-row-list"))
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.freeze_time("2025-07-17 14:33")
@pytest.mark.parametrize("canton", ["ag", "so"])
def test_work_item_list_row_list(
    admin_client,
    canton,
    django_assert_num_queries,
    setup_work_item_list,
    snapshot,
):
    setup_work_item_list(canton)

    with django_assert_num_queries(6):
        response = admin_client.get(
            reverse("work-item-list-row-list"), {"page[number]": 1, "page[size]": 20}
        )

    assert response.status_code == status.HTTP_200_OK
    assert normalize_response(response.json()) == snapshot()


@pytest.mark.parametrize(
    "filters,expected",
    [
        (
            {},
            {
                "from-template-and-read",
                "controlling",
                "assigned",
                "completed",
                "controlling",
            },
        ),
        ({"unread": True}, {"controlling", "assigned", "completed"}),
        ({"unread": False}, {"from-template-and-read"}),
        ({"role": "active"}, {"from-template-and-read", "assigned", "completed"}),
        ({"role": "control"}, {"controlling"}),
        ({"responsible": "placeholder"}, {"assigned"}),
        ({"task": "task"}, {"controlling"}),
        ({"task": "template"}, {"from-template-and-read"}),
        ({"preset": "placeholder"}, {"from-template-and-read", "controlling"}),
        ({"preset": "placeholder", "task": "task"}, {"controlling"}),
        (
            {"exclude_imported": True},
            {"controlling", "assigned", "completed", "controlling"},
        ),
        (
            {"exclude_imported": False},
            {
                "from-template-and-read",
                "controlling",
                "assigned",
                "completed",
                "controlling",
            },
        ),
    ],
)
def test_work_item_list_row_list_filters(
    admin_client, expected, filters, setup_work_item_list, user
):
    task, template, preset = setup_work_item_list()

    if "responsible" in filters:
        filters["responsible"] = user.username
    if filters.get("task") == "task":
        filters["task"] = task.pk
    if filters.get("task") == "template":
        filters["task"] = template.pk
    if "preset" in filters:
        filters["preset"] = preset.pk

    response = admin_client.get(
        reverse("work-item-list-row-list"),
        {"page[number]": 1, "page[size]": 20, **filters},
    )

    assert response.status_code == status.HTTP_200_OK
    assert {r["attributes"]["task"] for r in response.json()["data"]} == expected


@pytest.mark.parametrize(
    "is_addressed,is_ready,expected_status",
    [
        (True, True, status.HTTP_200_OK),
        (False, True, status.HTTP_403_FORBIDDEN),
        (True, False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_work_item_list_row_toggle_read(
    db,
    admin_client,
    expected_status,
    is_addressed,
    is_ready,
    service,
    work_item_list_row_factory,
):
    work_item = work_item_list_row_factory(
        canton="ag",
        addressed=service if is_addressed else None,
        controlling=None if is_addressed else service,
        status=WorkItem.STATUS_READY if is_ready else WorkItem.STATUS_COMPLETED,
        meta={"not-viewed": True},
    )

    response1 = admin_client.post(
        reverse("work-item-list-row-toggle-read", args=[work_item.pk])
    )

    assert response1.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert response1.json()["data"]["attributes"]["unread"] is False

        response2 = admin_client.post(
            reverse("work-item-list-row-toggle-read", args=[work_item.pk])
        )

        assert response2.status_code == status.HTTP_200_OK
        assert response2.json()["data"]["attributes"]["unread"] is True


@pytest.mark.parametrize(
    "is_addressed,is_ready,is_not_assigned,expected_status",
    [
        (True, True, True, status.HTTP_200_OK),
        (False, True, True, status.HTTP_403_FORBIDDEN),
        (True, False, True, status.HTTP_403_FORBIDDEN),
        (True, True, False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_work_item_list_row_assign_to_me(
    db,
    admin_client,
    admin_user,
    expected_status,
    is_addressed,
    is_not_assigned,
    is_ready,
    service,
    work_item_list_row_factory,
):
    work_item = work_item_list_row_factory(
        canton="ag",
        addressed=service if is_addressed else None,
        controlling=None if is_addressed else service,
        assigned=None if is_not_assigned else admin_user,
        status=WorkItem.STATUS_READY if is_ready else WorkItem.STATUS_COMPLETED,
    )

    response = admin_client.post(
        reverse("work-item-list-row-assign-to-me", args=[work_item.pk])
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert response.json()["data"]["relationships"]["assigned-user"]["data"][
            "id"
        ] == str(admin_user.pk)


@pytest.mark.parametrize(
    "is_addressed,is_ready,is_manually_completable,expected_status",
    [
        (True, True, True, status.HTTP_200_OK),
        (False, True, True, status.HTTP_403_FORBIDDEN),
        (True, False, True, status.HTTP_403_FORBIDDEN),
        (True, True, False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_work_item_list_row_quick_complete(
    db,
    admin_client,
    expected_status,
    is_addressed,
    is_manually_completable,
    is_ready,
    service,
    work_item_list_row_factory,
):
    work_item = work_item_list_row_factory(
        canton="ag",
        addressed=service if is_addressed else None,
        controlling=None if is_addressed else service,
        status=WorkItem.STATUS_READY if is_ready else WorkItem.STATUS_COMPLETED,
        task__meta={"is-manually-completable": is_manually_completable},
        task__type=Task.TYPE_SIMPLE,
    )

    response = admin_client.post(
        reverse("work-item-list-row-quick-complete", args=[work_item.pk])
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        assert response.json()["data"]["attributes"]["is-ready"] is False
        assert response.json()["data"]["attributes"]["status"] == "completed"
