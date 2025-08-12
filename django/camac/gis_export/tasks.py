from celery import shared_task

from .utils import export_agis


@shared_task()
def export_agis_task():
    """Celery task to export instance data to AGIS table."""

    export_agis()
