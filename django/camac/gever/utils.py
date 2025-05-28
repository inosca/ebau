from camac.gever.constants import (
    AGR_SERVICE_SLUG_BAUEN,
    AGR_SERVICE_SLUG_SHOOTING_NOISE,
)
from camac.user.models import Service


def is_agr_addressed(work_item):
    """Return True if one of the AGR groups is invited on the given workitem."""
    return (
        Service.objects.filter(
            slug__in=[AGR_SERVICE_SLUG_BAUEN, AGR_SERVICE_SLUG_SHOOTING_NOISE]
        )
        .filter(pk__in=(work_item.addressed_groups))
        .exists()
    )
