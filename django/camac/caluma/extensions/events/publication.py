from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_complete_work_item
from django.conf import settings
from django.db import transaction

from camac.notification.tasks import send_notification_for_publication


@on(post_complete_work_item, raise_exception=True)
@filter_events(
    lambda work_item: (
        work_item.task.slug == settings.PUBLICATION.get("FILL_TASKS", {}).get("PUBLIC")
        and settings.APPLICATION.get("NOTIFICATIONS", {}).get("PUBLICATION_START")
    )  # currently only defined for kt. GR.
)
@transaction.atomic
def post_complete_publication(sender, work_item, user, context=None, **kwargs):
    send_notification_for_publication.delay(str(work_item.pk))
