import re
from datetime import date, datetime

import pytest
from caluma.caluma_workflow.models import Task, WorkItem
from django.urls import reverse
from django.utils.timezone import make_aware, now
from faker import Faker
from rest_framework import status

from camac.caluma.utils import date_to_deadline
from camac.gis.utils import to_query
from camac.settings.modules.work_item_list_schema import (
    WorkItemListConfig,
)
from camac.tests.form_utils import FormUtils

fake = Faker()


def replace_instance_id(link):
    if isinstance(link, str):
        link = re.sub(
            r"((?:instance-id|instances)/)(\d+)(?=[/?&])", r"\1<INSTANCE_ID>", link
        )
    elif isinstance(link, dict):
        link["models"][0] = "<INSTANCE_ID>"

    return link


def normalize_response(response):
    for row in response["data"]:
        row["attributes"]["instance-id"] = "<INSTANCE_ID>"
        row["relationships"]["addressed-service"]["data"]["id"] = "<SERVICE_ID>"

        row["attributes"]["edit-link"] = replace_instance_id(
            row["attributes"]["edit-link"]
        )
        row["attributes"]["direct-link"] = replace_instance_id(
            row["attributes"]["direct-link"]
        )

        if row["relationships"]["assigned-user"]["data"] is not None:
            row["relationships"]["assigned-user"]["data"]["id"] = "<USER_ID>"
        if row["relationships"]["closed-by-user"]["data"] is not None:
            row["relationships"]["closed-by-user"]["data"]["id"] = "<USER_ID>"

    return response


@pytest.fixture
def disable_deadlines_progression(db, mocker):
    # disable auto calculating the deadline dates, as we set them manually here for this test.
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )


@pytest.fixture
def work_item_list_row_factory(db, caluma_work_item_factory, service_factory, request):
    def wrapper(
        canton="ag",
        addressed=None,
        controlling=None,
        assigned=None,
        case=None,
        **kwargs,
    ):
        master_data_case = request.getfixturevalue(f"{canton.lower()}_master_data_case")

        for module in [
            "distribution",
            "construction_monitoring",
            "deadlines",
            "work_item_list",
        ]:
            try:
                request.getfixturevalue(f"{canton.lower()}_{module}_settings")
            except pytest.FixtureLookupError:
                pass

        addressed = addressed if addressed else service_factory()
        controlling = controlling if controlling else service_factory()

        created_at = kwargs.pop("created_at", None)

        used_case = case or master_data_case
        work_item = caluma_work_item_factory(
            case=used_case,
            pk=fake.uuid4(),
            deadline=date_to_deadline(
                date.fromisoformat(kwargs.pop("deadline", fake.date()))
            ),
            child_case=None,
            addressed_groups=[str(addressed.pk)],
            controlling_groups=[str(controlling.pk)],
            assigned_users=[str(assigned.username)] if assigned else [],
            status=kwargs.pop("status", WorkItem.STATUS_READY),
            meta=kwargs.pop("meta", {"not-viewed": True}),
            **kwargs,
        )

        if created_at is not None:
            work_item.created_at = make_aware(
                datetime.combine(
                    date.fromisoformat(created_at),
                    datetime.min.time(),
                )
            )
            work_item.save(update_fields=["created_at"])

        return work_item

    return wrapper


@pytest.fixture
def setup_work_item_list(
    service,
    user,
    work_item_list_row_factory,
    user_factory,
    caluma_task_factory,
    caluma_case_factory,
    instance_factory,
    work_item_template_factory,
    work_item_list_filter_preset,
    instance_deadline_factory,
    request,
    settings,
    disable_deadlines_progression,
):
    def wrapper(canton="ag"):
        request.getfixturevalue(f"set_application_{canton.lower()}")

        application_settings = request.getfixturevalue("application_settings")

        task = caluma_task_factory(
            meta={
                "directLink": {
                    "route": "instance-resource-name=foobar&ember-hash=/foobar/{{TASK_SLUG}}",
                    "models": ["TASK_SLUG"],
                }
                if application_settings["INTERNAL_FRONTEND"] == "camac"
                else {
                    "route": "foo.bar.baz",
                    "models": ["INSTANCE_ID", "TASK_SLUG", "no-placeholder"],
                }
            }
        )
        template = work_item_template_factory()

        work_item_list_filter_preset.prefilter_tasks = True
        work_item_list_filter_preset.prefilter_work_item_templates = True
        work_item_list_filter_preset.tasks.add(task)
        work_item_list_filter_preset.work_item_templates.add(template)
        work_item_list_filter_preset.save()

        work_item_list_row_factory(
            canton=canton,
            name="not-visible",
        )
        work_item_list_row_factory(
            canton=canton,
            name="from-template-and-read",
            addressed=service,
            created_at="2025-01-05",
            deadline="2025-01-01",
            meta={
                "not-viewed": False,
                "template-id": str(template.pk),
                "imported": True,
            },
        )
        work_item_list_row_factory(
            canton=canton,
            name="from-task",
            addressed=service,
            created_at="2025-01-04",
            deadline="2025-01-02",
            task_id=task,
        )
        work_item_list_row_factory(
            canton=canton,
            name="assigned",
            addressed=service,
            assigned=user,
            created_at="2025-01-03",
            deadline="2025-01-03",
        )
        work_item_list_row_factory(
            canton=canton,
            name="completed",
            addressed=service,
            closed_at=now(),
            closed_by_user=user_factory().username,
            created_at="2025-01-02",
            deadline="2025-01-07",
            status=WorkItem.STATUS_COMPLETED,
        )
        work_item_list_row_factory(
            canton=canton,
            name="controlling",
            controlling=service,
            created_at="2025-01-01",
            deadline="2025-01-05",
        )

        if canton == "ur":
            additional_demand_instance = instance_factory(
                case=caluma_case_factory(), instance_state__name="nfd"
            )
            work_item_list_row_factory(
                canton=canton,
                name="additional-demand",
                addressed=service,
                case=additional_demand_instance.case,
                created_at="2026-01-07",
                deadline="2026-01-07",
            )

        # because the target deadline date is set on the instance,
        # we need to create a new instance for this work item.
        target_deadline_instance = instance_factory(case=caluma_case_factory())
        work_item_list_row_factory(
            canton=canton,
            name="target-deadline-date",
            addressed=service,
            assigned=user,
            case=target_deadline_instance.case,
            created_at="2025-01-04",
            deadline="2025-01-06",
        )

        if settings.DEADLINES.enabled:
            master_data_case = request.getfixturevalue(
                f"{canton.lower()}_master_data_case"
            )

            instance_deadline_factory(
                instance=master_data_case.family.instance,
                start_date="2025-01-02",
                process_deadline_date_override=True,
                process_deadline_date="2025-01-01",
                target_deadline_date="2025-01-02",
                service=service,
            )
            instance_deadline_factory(
                instance=target_deadline_instance,
                start_date="2025-01-01",
                process_deadline_date_override=True,
                process_deadline_date="2025-01-01",
                target_deadline_date="2025-01-01",
                service=service,
            )

        return task, template, work_item_list_filter_preset

    return wrapper


def test_work_item_list_row_list_no_pagination(
    admin_client, setup_work_item_list, snapshot
):
    setup_work_item_list()
    response = admin_client.get(reverse("work-item-list-row-list"), {"role": "active"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["errors"][0]["detail"] == "Pagination is required"


@pytest.mark.freeze_time("2025-07-17 14:33")
@pytest.mark.parametrize("canton", ["ag", "so", "gr", "sz", "ur", "be"])
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
            reverse("work-item-list-row-list"),
            {"page[number]": 1, "page[size]": 20, "role": "active"},
        )

    assert response.status_code == status.HTTP_200_OK
    assert normalize_response(response.json()) == snapshot()


def test_work_item_list_row_list_filters(admin_client, setup_work_item_list, user):
    task, template, preset = setup_work_item_list()

    for filters, expected_status, expected in [
        ({}, status.HTTP_400_BAD_REQUEST, None),
        (
            {"role": "active", "unread": True},
            status.HTTP_200_OK,
            {"assigned", "completed", "from-task", "target-deadline-date"},
        ),
        (
            {"role": "active", "unread": False},
            status.HTTP_200_OK,
            {"from-template-and-read"},
        ),
        (
            {"role": "active"},
            status.HTTP_200_OK,
            {
                "assigned",
                "completed",
                "from-task",
                "from-template-and-read",
                "target-deadline-date",
            },
        ),
        (
            {"role": "control"},
            status.HTTP_200_OK,
            {"controlling"},
        ),
        (
            {"role": "all"},
            status.HTTP_200_OK,
            set(),
        ),
        (
            {"role": "active", "responsible": "placeholder"},
            status.HTTP_200_OK,
            {"assigned", "target-deadline-date"},
        ),
        (
            {"role": "active", "task": "task"},
            status.HTTP_200_OK,
            {"from-task"},
        ),
        (
            {"role": "active", "task": "template"},
            status.HTTP_200_OK,
            {"from-template-and-read"},
        ),
        (
            {"role": "active", "preset": "placeholder"},
            status.HTTP_200_OK,
            {"from-task", "from-template-and-read"},
        ),
        (
            {"role": "active", "preset": "placeholder", "task": "task"},
            status.HTTP_200_OK,
            {"from-task"},
        ),
        (
            {"role": "active", "exclude_imported": True},
            status.HTTP_200_OK,
            {"assigned", "completed", "from-task", "target-deadline-date"},
        ),
        (
            {"role": "active", "exclude_imported": False},
            status.HTTP_200_OK,
            {
                "assigned",
                "completed",
                "from-task",
                "from-template-and-read",
                "target-deadline-date",
            },
        ),
    ]:
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

        assert response.status_code == expected_status

        if expected_status == status.HTTP_200_OK:
            received = {r["attributes"]["task"] for r in response.json()["data"]}
            assert received == expected, (
                f"Given the query params {to_query(filters)} the following work items were expected: {', '.join(expected)} but received {', '.join(received)}"
            )


def test_work_item_list_row_list_ordering(
    admin_client, django_assert_num_queries, setup_work_item_list
):
    setup_work_item_list()

    for sort, expected_work_item, expected_ordering in [
        (
            None,
            "from-template-and-read",
            'ORDER BY "caluma_workflow_workitem"."deadline" ASC NULLS FIRST LIMIT',
        ),
        (
            "deadline",
            "from-template-and-read",
            'ORDER BY "caluma_workflow_workitem"."deadline" ASC NULLS FIRST LIMIT',
        ),
        (
            "created_at",
            "completed",
            'ORDER BY "caluma_workflow_workitem"."created_at" ASC LIMIT',
        ),
        (
            "-created_at",
            "from-template-and-read",
            'ORDER BY "caluma_workflow_workitem"."created_at" DESC LIMIT',
        ),
        (
            "target_deadline_date",
            "target-deadline-date",
            # 37 is the column index for target_deadline_date in the SELECT statement because it is a subquery result.
            "ORDER BY 37 ASC LIMIT",
        ),
    ]:
        params = {
            "page[number]": 1,
            "page[size]": 20,
            "role": "active",
            "fields[work-item-list-rows]": "task,target_deadline_date",
        }

        if sort is not None:
            params["sort"] = sort

        with django_assert_num_queries(6) as captured:
            response = admin_client.get(reverse("work-item-list-row-list"), params)

        select_query = captured.captured_queries[2]["sql"]

        assert response.status_code == status.HTTP_200_OK
        assert response.json()["data"][0]["attributes"]["task"] == expected_work_item
        assert expected_ordering in select_query


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


@pytest.mark.parametrize(
    "annotation,expected_description",
    [
        ("beschreibung-bauvorhaben", "bauvorhaben"),
        ("beschreibung-projektaenderung", "projektaenderung"),
        ("nonexisting", None),
        (
            [
                "beschreibung-projektaenderung",
                "beschreibung-bauvorhaben",
                "nonexisting",
            ],
            "projektaenderung",
        ),
        (
            [
                "beschreibung-bauvorhaben",
                "beschreibung-projektaenderung",
                "nonexisting",
            ],
            "bauvorhaben",
        ),
        (
            [
                "nonexisting",
                "beschreibung-projektaenderung",
                "beschreibung-bauvorhaben",
            ],
            "projektaenderung",
        ),
        (
            [
                "nonexisting",
                "beschreibung-bauvorhaben",
                "beschreibung-projektaenderung",
            ],
            "bauvorhaben",
        ),
    ],
)
def test_work_item_list_row_description_coalesce(
    db,
    admin_client,
    service,
    annotation,
    expected_description,
    work_item_list_row_factory,
    gr_work_item_list_settings: WorkItemListConfig,
    form_utils: FormUtils,
    set_application_gr,
):
    """Test that the description annotation can be a list of slugs.

    If it is a string, just return that answer.
    If it is a list, return the first non-empty answer.
    """
    gr_work_item_list_settings.annotations.description = annotation
    work_item = work_item_list_row_factory(
        canton="gr",
        addressed=service,
        controlling=service,
        status=WorkItem.STATUS_READY,
        task__type=Task.TYPE_SIMPLE,
    )

    bauvorhaben_answer = work_item.case.document.answers.get(
        question__slug="beschreibung-bauvorhaben"
    )
    bauvorhaben_answer.value = "bauvorhaben"
    bauvorhaben_answer.save()
    form_utils.add_answer(
        work_item.case.document,
        "beschreibung-projektaenderung",
        "projektaenderung",
    )

    response = admin_client.get(
        reverse("work-item-list-row-list"),
        {"page[number]": 1, "page[size]": 20, "role": "active"},
    )

    assert response.status_code == status.HTTP_200_OK

    assert (
        response.json()["data"][0]["attributes"]["description"] == expected_description
    )
