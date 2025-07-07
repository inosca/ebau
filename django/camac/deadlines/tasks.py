from celery import shared_task


@shared_task()
def update_deadlines():  # pragma: no cover
    """Celery task to update deadline progression."""

    from camac.deadlines import models as deadlines_models

    deadlines_models.InstanceDeadline.objects.recalculate_deadlines()
