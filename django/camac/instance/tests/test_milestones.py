from datetime import datetime

import pytest
from caluma.caluma_workflow.factories import WorkItemFactory
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from django.utils.timezone import make_aware
from rest_framework import status

from camac.constants import kt_uri as uri_constants


@pytest.mark.parametrize(
    "role__name",
    [
        ("Municipality"),
    ],
)
@pytest.mark.parametrize("is_paper_answer", ["is-paper-no", "is-paper-yes"])
@pytest.mark.freeze_time("2023-12-31")
@pytest.mark.django_db(
    transaction=True, reset_sequences=True
)  # always reset instance id
def test_milestones_ur(
    db,
    role,
    admin_client,
    ur_instance,
    settings,
    application_settings,
    snapshot,
    is_paper_answer,
    answer_factory,
):
    application_settings["CALUMA"]["SUBMIT_TASKS"] = ["submit"]
    application_settings["COORDINATION_SERVICE_IDS"] = [
        uri_constants.KOOR_BG_SERVICE_ID
    ]
    settings.APPLICATION_NAME = "kt_uri"

    answer_factory(
        document=ur_instance.case.document,
        question_id="is-paper",
        value=is_paper_answer,
    )

    submit_task = ur_instance.case.work_items.get(task_id="submit")
    submit_task.closed_at = make_aware(datetime(2023, 1, 1, 20, 0, 0))
    submit_task.save()

    for task_slug in ["check-permit", "decision"]:
        WorkItemFactory(
            task_id=task_slug,
            case=ur_instance.case,
            closed_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
            status=WorkItem.STATUS_COMPLETED,
        )

    # top level circulation (Gemeinde -> KOOR)
    WorkItemFactory(
        task_id="inquiry",
        case=ur_instance.case,
        created_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        addressed_groups=[uri_constants.KOOR_BG_SERVICE_ID],
        controlling_groups=[],
        status=WorkItem.STATUS_COMPLETED,
        closed_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
    )

    # Nested KOOR circulation
    WorkItemFactory(
        task_id="inquiry",
        case=ur_instance.case,
        created_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        controlling_groups=[uri_constants.KOOR_BG_SERVICE_ID],
        status=WorkItem.STATUS_COMPLETED,
        closed_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
    )

    url = reverse("instance-milestones", args=[ur_instance.pk])
    response = admin_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    snapshot.assert_match(response.json())
