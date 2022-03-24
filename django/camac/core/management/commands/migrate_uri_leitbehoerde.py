from caluma.caluma_user.models import BaseUser
from django.core.management.base import BaseCommand

from camac.caluma.api import CalumaApi
from camac.core.models import AuthorityLocation, WorkflowEntry

caluma_api = CalumaApi()


class MigrationUser(BaseUser):
    def __str__(self):
        return "migration-user"


class Command(BaseCommand):
    help = "Adds the leitbehörde for portal instances that don't have one yet"

    def handle(self, *args, **options):
        for entry in WorkflowEntry.objects.filter(workflow_item_id=12000000):
            instance = entry.instance
            authority_location = AuthorityLocation.objects.filter(
                location_id=instance.location_id
            )

            if (
                authority_location
                and not instance.case.document.answers.filter(
                    question_id="leitbehoerde"
                ).exists()
            ):
                caluma_api.update_or_create_answer(
                    instance.case.document,
                    "leitbehoerde",
                    str(authority_location.first().authority_id),
                    user=MigrationUser(),
                )
