from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef
from tqdm import tqdm

from camac.applicants.models import Applicant
from camac.permissions.events.core import Trigger
from camac.permissions.models import InstanceACL


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

        applicants_missing_acl = (
            Applicant.objects.filter(invitee__isnull=False)
            .annotate(
                acls_exists=Exists(
                    InstanceACL.objects.filter(
                        user=OuterRef("invitee"), instance=OuterRef("instance")
                    )
                )
            )
            .exclude(acls_exists=True)
        )

        sid = transaction.savepoint()
        for applicant in tqdm(applicants_missing_acl, desc="Creating permissions"):
            Trigger.applicant_added(None, applicant.instance, applicant)

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
