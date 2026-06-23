from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from camac.caluma.utils import find_answer
from camac.core.models import HistoryActionConfig
from camac.core.utils import create_history_entry
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
    # must wait for the transaction to complete, otherwise celery will start the task
    # before the db update is actually complete (meta changes for `is-published`) and
    # then loses the changes after modifying the meta.
    transaction.on_commit(
        lambda: send_notification_for_publication.delay(str(work_item.pk))
    )


def _is_not_so_and_publication(work_item: WorkItem) -> bool:
    return not settings.APPLICATION.get(
        "SHORT_NAME"
    ) == "so" or not work_item.task_id == settings.PUBLICATION.get(
        "FILL_TASKS", {}
    ).get("PUBLIC")


@receiver(pre_save, sender=WorkItem)
def so_pre_save_unpublished_publication_history(
    sender, instance: WorkItem, **kwargs
) -> None:
    if _is_not_so_and_publication(instance) or instance.pk is None:
        return

    if old_wi := WorkItem.objects.filter(pk=instance.pk).first():
        instance._pre_save_meta = old_wi.meta


@receiver(post_save, sender=WorkItem)
@transaction.atomic
def so_post_save_publication_create_history_entry(
    sender, instance: WorkItem, created: bool, **kwargs
) -> None:
    if (
        _is_not_so_and_publication(instance)
        # Only run if work item is not newly created, meta is updated and is-published is set
        or created
        or instance.meta.get("is-published") is None
        or instance.meta.get("is-published")
        == instance._pre_save_meta.get("is-published")
    ):
        return

    user = get_user_model().objects.filter(username=instance.modified_by_user).first()

    publication_start = find_answer(instance.document, "publikation-start")
    publication_ende = find_answer(instance.document, "publikation-ende")
    publication_newspaper = find_answer(instance.document, "publikation-organ")
    publication_newspaper_date = find_answer(instance.document, "publikation-anzeiger")
    publication_gazette_date = find_answer(instance.document, "publikation-amtsblatt")

    text_parts = [
        _("Publication created for %(start)s to %(end)s in %(newspaper)s.")
        if instance.meta.get("is-published")
        else _("Publication cancelled for %(start)s to %(end)s in %(newspaper)s."),
    ]

    if publication_gazette_date:
        text_parts.append(_("Gazette: %(gazette_date)s."))

    if publication_newspaper_date:
        text_parts.append(_("Newspaper: %(newspaper_date)s."))

    text = ((" ").join(text_parts)) % {
        "start": publication_start,
        "end": publication_ende,
        "newspaper": publication_newspaper,
        "newspaper_date": publication_newspaper_date,
        "gazette_date": publication_gazette_date,
    }

    create_history_entry(
        instance.case.family.instance,
        user=user,
        text=text,
        history_type=HistoryActionConfig.HISTORY_TYPE_PUBLICATION,
    )
