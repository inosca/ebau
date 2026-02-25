from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.caluma.extensions.events.ktso_afu_custom_task_form import (
    _create_afu_work_item,
)
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
        sid = transaction.savepoint()

        afu = Service.objects.get(slug="afu")
        acls = InstanceACL.objects.filter(
            service_id__in=[afu.pk, *afu.service_children.values_list("pk", flat=True)]
        )

        for acl in tqdm(acls, desc="Creating WorkItem"):
            _create_afu_work_item(acl)
        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
