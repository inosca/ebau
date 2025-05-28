from caluma.caluma_workflow.models import Task
from django.conf import settings

from camac.user.models import Service


def is_agr_addressed(work_item):
    """Return True if one of the AGR groups is invited on the given workitem."""
    return (
        Service.objects.filter(slug__in=get_all_agr_service_slugs())
        .filter(pk__in=(work_item.addressed_groups))
        .exists()
    )


def get_gever_task():
    """Return the GEVER Caluma task."""
    return Task.objects.get(pk=settings.GEVER["GEVER_TASK_SLUG"])


# Service slugs
def get_all_agr_service_slugs():
    """Return a list of all service slugs for the AGR GEVER services."""
    return [
        settings.GEVER["AGR_SERVICE_SLUG_BAUEN"],
        settings.GEVER["AGR_SERVICE_SLUG_SHOOTING_NOISE"],
    ]
