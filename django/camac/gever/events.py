from django_q.tasks import async_task

from . import tasks

"""
GEVER Events

Public entrypoints for the events that have a GEVER-related effect.
"""


def sync_button_pressed(instance):
    return async_task(tasks.sync_full, instance)
