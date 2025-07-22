from datetime import datetime

import pytest
from django.core.management import call_command
from django.utils.timezone import make_aware

from camac.deadlines import models as deadlines_models


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
    caplog,
):
    """Test the management command execution for updating deadline progression."""
    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=make_aware(datetime.strptime("2025-05-20", "%Y-%m-%d")),
    )
    suspension_factory(
        deadline=deadline,
        start_date=make_aware(datetime.strptime("2025-05-25", "%Y-%m-%d")),
        end_date=None,
    )

    deadline.refresh_from_db()
    deadline.process_deadline_days = 0
    deadline.save()
    assert deadline.process_deadline_days == 0
    call_command("update_deadline_progression", verbosity=verbosity)

    assert len(caplog.messages) == (1 if has_stdout else 0)
    deadline.refresh_from_db()
    assert deadline.process_deadline_days == 4


def test_management_command_deadline_progression_query(
    db,
    service_factory,
    suspension_factory,
    instance_deadline_factory,
    instance_factory,
):
    """Test the management command query to only select deadlines with open suspensions."""
    service1 = service_factory()
    service2 = service_factory()

    instance1 = instance_factory()
    instance2 = instance_factory()

    deadline1 = instance_deadline_factory(instance=instance1, service=service1)
    deadline2 = instance_deadline_factory(instance=instance1, service=service2)
    deadline3 = instance_deadline_factory(instance=instance2, service=service2)
    instance_deadline_factory(instance=instance_factory(), service=service1)
    instance_deadline_factory(instance=instance1, service=service_factory())

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
            deadlines_models.InstanceDeadline.objects.with_open_suspensions()
            .order_by("instance__pk", "service__pk")
            .values_list("instance__pk", "service__pk")
        )
    ]
    assert [
        (instance1.pk, service1.pk),
        (instance1.pk, service2.pk),
        (instance2.pk, service2.pk),
    ] == updates, "The query should only return deadlines with open suspensions."
