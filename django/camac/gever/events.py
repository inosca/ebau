from django.conf import settings
from django_q.tasks import async_task

from . import tasks

"""
GEVER Events

Public entrypoints for the events that have a GEVER-related effect.
"""


def decision_decreed(instance):
    """Perform GEVER sync operations after decision has been decreed."""
    if not settings.GEVER or not settings.GEVER["ENABLED"]:
        # GEVER not active - don't do anything
        return False
    # Spec: "Nach dem Bauentscheid durch die Leitbehörde werden nochmals die
    # Dokumente im BE-GEVER aktualisiert."
    return async_task(tasks.sync_documents, instance)


def sync_button_pressed(instance):
    if not settings.GEVER or not settings.GEVER["ENABLED"]:  # pragma: no cover
        # GEVER not active - don't do anything
        return False
    return async_task(tasks.sync_full, instance)
