from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.permissions.models import InstanceACL
from camac.user.models import Service


class Command(BaseCommand):
    help = """Create custom work item for AfU service"""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if settings.APPLICATION_NAME != "kt_so":
            raise Exception("Only for Kt SO")

        sid = transaction.savepoint()

        afu = Service.objects.get(slug="afu")
        task = Task.objects.get(pk="afu-form")
        acls = (
            InstanceACL.objects.filter(service_id=afu)
            .exclude(instance__instance_state__name="finished")
            .exclude(instance__case__work_items__task_id=task.pk)
        )

        for acl in tqdm(acls, desc="Creating WorkItem"):
            case = acl.instance.case
            WorkItem.objects.create(
                task_id=task.pk,
                case=case,
                addressed_groups=[str(afu.pk)],
                controlling_groups=[],
                document=Document.objects.create_document_for_task(task, user=None),
                status=WorkItem.STATUS_READY,
            )
        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
