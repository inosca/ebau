from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from camac.permissions.models import InstanceACL
from camac.user.models import Service


@receiver(post_save, sender=InstanceACL)
@transaction.atomic
def create_afu_work_item(
    sender: type[InstanceACL], instance: InstanceACL, raw: bool, created: bool, **kwargs
) -> None:
    """Create a work item for the AfU custom afu-form task."""
    if settings.APPLICATION_NAME != "kt_so" or raw or not created:
        return

    acl = instance
    if (
        acl.instance.instance_state.name == "finished"
        or not acl.service
        or acl.service.slug != "afu"
    ):
        return

    case = acl.instance.case
    task = Task.objects.get(pk="afu-form")
    existing_work_item = WorkItem.objects.filter(
        task=task,
        case=case,
    )

    if not existing_work_item.exists():
        afu = Service.objects.get(slug="afu")
        WorkItem.objects.create(
            task_id=task.pk,
            case=case,
            addressed_groups=[str(afu.pk)],
            controlling_groups=[],
            document=Document.objects.create_document_for_task(task, user=None),
            status=WorkItem.STATUS_READY,
        )
