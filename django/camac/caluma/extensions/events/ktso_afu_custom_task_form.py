from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.db.models.signals import post_save
from django.dispatch import receiver

from camac.permissions.models import InstanceACL
from camac.user.models import Service


def _create_afu_work_item(acl: InstanceACL) -> None:
    """Create a work item for the AfU custom afu-form task."""
    if (
        acl.instance.instance_state.name != "finished"
        and acl.service
        # Check if service is afu or child service of afu
        and Service.objects.filter(
            Q(slug="afu", pk=acl.service.pk)
            | Q(slug="afu", service_children__pk__contains=acl.service.pk)
        ).exists()
    ):
        case = acl.instance.case
        task = Task.objects.get(pk="afu-form")
        existing_work_item = WorkItem.objects.filter(
            Q(
                task=task,
                case=case,
                status=WorkItem.STATUS_READY,
            )
        )

        if not existing_work_item.exists():
            WorkItem.objects.create(
                task_id=task.pk,
                case=case,
                addressed_groups=[acl.service.pk],
                controlling_groups=[],
                document=Document.objects.create_document_for_task(task, user=None),
                status=WorkItem.STATUS_READY,
            )
        elif existing_work_item.filter(~Q(addressed_groups__contains=[acl.service.pk])):
            afu_workitem = existing_work_item.first()
            afu_workitem.addressed_groups.append(str(acl.service.pk))
            afu_workitem.save()


@receiver(post_save, sender=InstanceACL)
@transaction.atomic
def create_afu_work_item(
    sender: type[InstanceACL], instance: InstanceACL, raw: bool, **kwargs
) -> None:
    if settings.APPLICATION_NAME == "kt_so" and not raw:
        _create_afu_work_item(instance)


@on(post_complete_work_item, raise_exception=True)
@filter_events(lambda work_item: work_item.task.slug == "complete-instance")
@transaction.atomic
def complete_afu_work_item(
    sender: type[WorkItem], work_item: WorkItem, user, context=None, **kwargs
) -> None:
    if settings.APPLICATION_NAME != "kt_so":
        return

    case = work_item.case

    task = Task.objects.get(pk="afu-form")
    existing_work_item = WorkItem.objects.filter(
        task=task,
        case=case,
        status=WorkItem.STATUS_READY,
    )

    if not existing_work_item.exists():
        return

    complete_work_item(existing_work_item.first(), user)
