from django.core.management.base import BaseCommand
from django.db import transaction

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance

caluma_api = CalumaApi()


class Command(BaseCommand):
    help = """Migrate the answers of the question 'oereb-thema-gemeinde' into the question 'oereb-thema'."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        # Get all instances with the 'oereb-verfahren-gemeinde' form
        instances = Instance.objects.filter(form_id=305)

        for instance in instances:
            old_answer = instance.case.document.answers.filter(
                question_id="oereb-thema-gemeinde"
            ).first()

            if not old_answer:
                print(f"Instance {instance.pk} had no 'oereb-thema-gemeinde' question")
                continue

            old_answer.value = old_answer.value.replace("-gemeinde", "")
            old_answer.question_id = "oereb-thema"
            old_answer.save()
            print(
                f"Fixed question oereb-thema of instance {instance.pk} (old value was {old_answer.value})"
            )

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
