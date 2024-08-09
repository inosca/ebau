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
        ("Sekretariat der Gemeindebaubehörde"),
    ],
)
@pytest.mark.parametrize(
    "is_paper_answer,complete_check_outcome,open_additional_demands",
    [
        ("is-paper-no", "complete-check-vollstaendigkeitspruefung-complete", False),
        ("is-paper-yes", "complete-check-vollstaendigkeitspruefung-complete", False),
        ("is-paper-no", "complete-check-vollstaendigkeitspruefung-incomplete", True),
        ("is-paper-no", "complete-check-vollstaendigkeitspruefung-incomplete", False),
    ],
)
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
    answer_factory,
    document_factory,
    set_application_ur,
    #
    is_paper_answer,
    complete_check_outcome,
    open_additional_demands,
):
    answer_factory(
        document=ur_instance.case.document,
        question_id="is-paper",
        value=is_paper_answer,
    )

    submit_task = ur_instance.case.work_items.get(task_id="submit")
    submit_task.closed_at = make_aware(datetime(2023, 1, 1, 20, 0, 0))
    submit_task.status = WorkItem.STATUS_COMPLETED
    submit_task.save()

    complete_check_work_item = WorkItemFactory(
        task_id="complete-check",
        case=ur_instance.case,
        closed_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form_id="complete-check"),
    )
    answer_factory(
        document=complete_check_work_item.document,
        question__slug="complete-check-vollstaendigkeitspruefung",
        value=complete_check_outcome,
    )
    WorkItemFactory(
        task_id="check-additional-demand",
        case=ur_instance.case,
        closed_at=make_aware(datetime(2023, 1, 1, 20, 0, 0)),
        status=WorkItem.STATUS_READY
        if open_additional_demands
        else WorkItem.STATUS_COMPLETED,
    )
    WorkItemFactory(
        task_id="decision",
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
