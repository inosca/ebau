from datetime import date, datetime

import pytest
from django.core.management import call_command

from camac.deadlines import models as deadlines_models


@pytest.mark.freeze_time("2025-05-28")
@pytest.mark.parametrize(
    "service_group__name,role__name", [("municipality", "municipality-lead")]
)
@pytest.mark.parametrize("verbosity,has_stdout", [(1, False), (2, True)])
def test_management_command_deadline_progression(
    db,
    service,
    instance_deadline_factory,
    suspension_factory,
    gr_instance,
    verbosity,
    has_stdout,
    gr_deadlines_settings,
    disable_deadline_side_effects,
    caplog,
):
    """Test the management command execution for updating deadline progression."""
    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2025, 6, 28),
    )
    suspension_factory(
        deadline=deadline,
        start_date=date(2025, 5, 25),
        end_date=None,
    )

    deadline.refresh_from_db()
    deadline.process_deadline_days = 0
    deadline.save()
    assert deadline.process_deadline_days == 0
    call_command("update_deadline_progression", verbosity=verbosity)

    assert len(caplog.messages) == (1 if has_stdout else 0)
    deadline.refresh_from_db()
    assert deadline.process_deadline_days == 5


@pytest.mark.freeze_time("2025-05-28")
def test_management_command_deadline_progression_query(
    db,
    service_factory,
    suspension_factory,
    instance_deadline_factory,
    instance_factory,
    disable_deadline_side_effects,
    gr_deadlines_settings,
):
    """Test the management command query to only select deadlines with open suspensions."""
    service1 = service_factory()
    service2 = service_factory()
    service3 = service_factory()

    instance1 = instance_factory()
    instance2 = instance_factory()
    instance3 = instance_factory()

    deadline1 = instance_deadline_factory(
        instance=instance1,
        service=service1,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2025, 6, 28),
    )
    deadline2 = instance_deadline_factory(
        instance=instance1,
        service=service2,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2025, 6, 28),
    )
    # deadline ended already
    deadline3 = instance_deadline_factory(
        instance=instance2,
        service=service2,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2025, 5, 21),
    )
    # Will have no suspensions, but end date in the future
    instance_deadline_factory(
        instance=instance3,
        service=service3,
        start_date=datetime(2025, 4, 20),
        process_deadline_date=date(2025, 6, 28),
    )
    instance_deadline_factory(
        instance=instance1,
        service=service_factory(),
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2025, 5, 21),
    )

    # Closed suspension for instance1 and service1
    suspension_factory(
        deadline=deadline1,
        start_date="2022-01-01",
        end_date="2023-01-01",
    )
    # Open suspension for instance1 and service1
    suspension_factory(
        deadline=deadline1,
        start_date="2022-01-01",
        end_date=None,
    )
    # Open suspension for instance1 and service2
    suspension_factory(
        deadline=deadline2,
        start_date="2022-01-01",
        end_date=None,
    )
    # Open suspension for instance2 and service2
    suspension_factory(
        deadline=deadline3,
        start_date="2022-01-01",
        end_date=None,
    )

    updates = [
        v
        for v in (
            deadlines_models.InstanceDeadline.objects.only_running()
            .order_by("instance__pk", "service__pk")
            .values_list("instance__pk", "service__pk")
        )
    ]

    assert set(
        [
            (instance1.pk, service1.pk),
            (instance1.pk, service2.pk),
            (instance2.pk, service2.pk),
            (instance3.pk, service3.pk),
        ]
    ) == set(updates), (
        "The query should only return deadlines with open suspensions or not ended."
    )
