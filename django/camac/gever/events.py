from django_q.tasks import async_task

from . import tasks

"""
GEVER Events

Public entrypoints for the events that have a GEVER-related effect.
"""


def decision_decreed(instance):
    """Perform GEVER sync operations after decision has been decreed."""
    # Spec: "Nach dem Bauentscheid durch die Leitbehörde werden nochmals die
    # Dokumente im BE-GEVER aktualisiert."
    return async_task(tasks.sync_documents, instance)


def sync_button_pressed(instance):
    return async_task(tasks.sync_full, instance)
