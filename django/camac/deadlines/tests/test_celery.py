from datetime import date

import pytest

from camac.deadlines.tasks import update_deadlines


@pytest.mark.freeze_time("2025-05-28")
def test_task_update_deadlines(
    db,
    instance_deadline_factory,
    suspension_factory,
    service_factory,
    gr_instance,
    gr_deadlines_settings,
    disable_deadline_side_effects,
):
    """Test deadline progression update through the celery task."""
    service1 = service_factory()
    service2 = service_factory()
    service3 = service_factory()

    # deadline with closed suspension
    deadline1 = instance_deadline_factory(
        instance=gr_instance,
        service=service1,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2026, 5, 20),
        process_deadline_date_override=True,
        total_days_of_suspension=0,
        process_deadline_days=0,
    )
    suspension_factory(
        deadline=deadline1,
        start_date=date(2025, 5, 25),
        end_date=date(2025, 5, 26),
    )

    # deadline with open suspension
    deadline2 = instance_deadline_factory(
        instance=gr_instance,
        service=service2,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2026, 5, 20),
        process_deadline_date_override=True,
        total_days_of_suspension=0,
        process_deadline_days=0,
    )
    suspension_factory(
        deadline=deadline2,
        start_date=date(2025, 5, 25),
        end_date=None,
    )

    # closed deadline
    deadline3 = instance_deadline_factory(
        instance=gr_instance,
        service=service3,
        start_date=date(2025, 5, 20),
        process_deadline_date=date(2026, 5, 20),
        process_deadline_date_override=True,
        total_days_of_suspension=2,
        process_deadline_days=1,
    )
    suspension_factory(
        deadline=deadline3,
        start_date=date(2025, 5, 25),
        end_date=None,
    )

    assert deadline1.process_deadline_days == 0
    assert deadline2.process_deadline_days == 0
    assert deadline3.process_deadline_days == 1
    assert deadline1.total_days_of_suspension == 0
    assert deadline2.total_days_of_suspension == 0
    assert deadline3.total_days_of_suspension == 2

    update_deadlines()
    deadline1.refresh_from_db()
    deadline2.refresh_from_db()

    assert deadline1.process_deadline_days == 7
    assert deadline2.process_deadline_days == 5
    assert deadline3.process_deadline_days == 1
    assert deadline1.total_days_of_suspension == 1
    assert deadline2.total_days_of_suspension == 3
    assert deadline3.total_days_of_suspension == 2
