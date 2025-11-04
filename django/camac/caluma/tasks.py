from celery import shared_task


@shared_task()
def celery_handle_manual_work_item_notification(
    event_type, context, username, camac_group, work_item_pk
):
    from caluma.caluma_workflow.models import WorkItem

    work_item = WorkItem.objects.get(pk=work_item_pk)
    if not work_item.closed_at:
        from caluma.caluma_user.models import BaseUser

        from camac.caluma.extensions.events.caluma_workflow_notifications import (
            handle_notification,
        )

        user = BaseUser(username=username)
        user.camac_group = camac_group
        handle_notification(event_type, context, user, work_item)
