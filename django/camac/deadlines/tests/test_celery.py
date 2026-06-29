from datetime import date

import pytest

from camac.deadlines.tasks import update_deadlines


@pytest.mark.freeze_time("2026-04-24")
@pytest.mark.django_db
def test_task_update_deadlines(
    instance_deadline_factory,
    deadline_type_factory,
    suspension_factory,
    service_factory,
    so_instance,
    deadlines_settings,
    disable_deadline_side_effects,
    set_application_so,
):
    """Test deadline progression update through the celery task."""
    service1 = service_factory()
    service2 = service_factory()
    service3 = service_factory()

    deadline_type = deadline_type_factory(
        lead_time=40,
        exclude_weekends=True,
        exclude_public_holidays=True,
    )

    # deadline without suspension
    deadline1 = instance_deadline_factory(
        instance=so_instance,
        service=service1,
        start_date=date(2026, month=4, day=13),
        process_deadline_date=date(2026, 5, 20),
        total_days_of_suspension=0,
        process_deadline_days=0,
        deadline_type=deadline_type,
    )

    # deadline with closed suspension
    deadline2 = instance_deadline_factory(
        instance=so_instance,
        service=service2,
        start_date=date(2026, month=4, day=13),
        process_deadline_date=date(2026, 5, 20),
        total_days_of_suspension=0,
        process_deadline_days=0,
        deadline_type=deadline_type,
    )
    suspension_factory(
        deadline=deadline2,
        start_date=date(2026, 4, 14),
        end_date=date(2026, 4, 15),
    )

    # deadline with open suspension
    deadline3 = instance_deadline_factory(
        instance=so_instance,
        service=service3,
        start_date=date(2026, month=4, day=13),
        process_deadline_date=date(2026, 5, 20),
        total_days_of_suspension=0,
        process_deadline_days=0,
        deadline_type=deadline_type,
    )
    suspension_factory(
        deadline=deadline3,
        start_date=date(2026, 4, 14),
        end_date=None,
    )

    assert deadline1.process_deadline_days == 0
    assert deadline2.process_deadline_days == 0
    assert deadline3.process_deadline_days == 0
    assert deadline1.total_days_of_suspension == 0
    assert deadline2.total_days_of_suspension == 0
    assert deadline3.total_days_of_suspension == 0

    update_deadlines()
    deadline1.refresh_from_db()
    deadline2.refresh_from_db()
    deadline3.refresh_from_db()

    assert deadline1.process_deadline_days == 10
    assert deadline2.process_deadline_days == 8
    assert deadline3.process_deadline_days == 1
    assert deadline1.total_days_of_suspension == 0
    assert deadline2.total_days_of_suspension == 2
    assert deadline3.total_days_of_suspension == 9
    assert deadline1.target_deadline_date == date(2026, 6, 9)
    assert deadline2.target_deadline_date == date(2026, 6, 11)
    assert deadline3.target_deadline_date == date(2026, 6, 20)
