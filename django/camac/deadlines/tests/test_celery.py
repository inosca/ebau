from datetime import datetime

import pytest
from django.utils.timezone import make_aware

from camac.deadlines.tasks import update_deadlines


@pytest.mark.freeze_time("2025-05-28")
def test_task_update_deadlines(
    db,
    service,
    instance_deadline_factory,
    suspension_factory,
    gr_instance,
    gr_deadlines_settings,
):
    """Test deadline progression update through the celery task."""
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
    update_deadlines()
    deadline.refresh_from_db()
    assert deadline.process_deadline_days == 4
