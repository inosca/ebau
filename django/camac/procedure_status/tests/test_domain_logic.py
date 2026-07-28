from __future__ import annotations

from datetime import timedelta
from typing import TYPE_CHECKING

import pytest
from caluma.caluma_workflow.models import WorkItem
from django.utils import timezone

from camac.procedure_status.domain_logic import (
    StepStatus,
    get_pending_work_items_overview,
    get_status_timeline,
)
from camac.settings.modules.procedure_status_schema import StepMapping

if TYPE_CHECKING:
    from camac.settings.modules.procedure_status_schema import ProcedureStatusConfig


@pytest.mark.parametrize(
    ("instance_state__name", "expected"),
    [
        ("new", [StepStatus.RUNNING, StepStatus.PENDING, StepStatus.PENDING]),
        ("decision", [StepStatus.DONE, StepStatus.RUNNING, StepStatus.PENDING]),
        ("finished", [StepStatus.DONE, StepStatus.DONE, StepStatus.DONE]),
    ],
)
@pytest.mark.django_db
def test_get_status_timeline(
    expected, instance, procedure_status_settings: ProcedureStatusConfig
):

    procedure_status_settings.steps = ["submit", "decision", "finish"]
    procedure_status_settings.instance_state_map = {
        "new": StepMapping(step="submit"),
        "decision": StepMapping(step="decision"),
        "finished": StepMapping(step="finish", done=True),
    }

    for i, (step, status) in enumerate(get_status_timeline(instance).items()):
        expected_status = expected[i]

        assert status == expected_status, (
            f"Expected status '{expected_status}' for step '{step}' with "
            f"instance state '{instance.instance_state.name}' but got "
            f"'{status}' instead."
        )


@pytest.mark.django_db
def test_get_pending_work_items_overview(
    application_settings,
    caluma_case_factory,
    caluma_task_factory,
    caluma_work_item_factory,
    instance,
    multilang,
    service_factory,
):
    instance.case = caluma_case_factory()
    instance.save()

    service_a = service_factory(trans__name="Organisation A")
    service_b = service_factory(trans__name="Organisation B")

    task_a = caluma_task_factory(name="Wichtige Aufgabe")
    task_b = caluma_task_factory(name="Auch eine Aufgabe")

    # Two ready work items of the same task addressed to different services are
    # merged into a single entry holding both service names
    caluma_work_item_factory(
        case=instance.case,
        task=task_a,
        status=WorkItem.STATUS_READY,
        deadline=timezone.now() + timedelta(days=2),
        addressed_groups=[str(service_a.pk)],
    )
    caluma_work_item_factory(
        case=instance.case,
        task=task_a,
        status=WorkItem.STATUS_READY,
        deadline=timezone.now() + timedelta(days=1),
        addressed_groups=[str(service_b.pk)],
    )
    # Another ready work item for another task
    caluma_work_item_factory(
        case=instance.case,
        task=task_b,
        status=WorkItem.STATUS_READY,
        deadline=timezone.now() + timedelta(days=3),
        addressed_groups=[str(service_b.pk)],
    )
    # Work item without a deadline: excluded
    caluma_work_item_factory(
        case=instance.case,
        status=WorkItem.STATUS_READY,
        deadline=None,
        addressed_groups=[str(service_a.pk)],
    )
    # Work item addressed to the applicant: excluded
    caluma_work_item_factory(
        case=instance.case,
        status=WorkItem.STATUS_READY,
        deadline=timezone.now(),
        addressed_groups=["applicant"],
    )
    # Manual work item: excluded
    caluma_work_item_factory(
        case=instance.case,
        task__slug=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
        status=WorkItem.STATUS_READY,
        deadline=timezone.now(),
        addressed_groups=[str(service_a.pk)],
    )
    # Completed work item: excluded
    caluma_work_item_factory(
        case=instance.case,
        status=WorkItem.STATUS_COMPLETED,
        deadline=timezone.now(),
        addressed_groups=[str(service_a.pk)],
    )

    assert get_pending_work_items_overview(instance) == [
        {
            "name": "Wichtige Aufgabe",
            "services": {"Organisation B", "Organisation A"},
        },
        {
            "name": "Auch eine Aufgabe",
            "services": {"Organisation B"},
        },
    ]
