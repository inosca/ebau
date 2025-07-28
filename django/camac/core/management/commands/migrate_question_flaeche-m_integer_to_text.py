from logging import getLogger

from caluma.caluma_form.models import Question
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

log = getLogger(__name__)


class Command(BaseCommand):
    help = """Migrate flaeche-m caluma question from type integer to text."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if settings.APPLICATION_NAME != "kt_so":
            log.error("Only for kt_so. Aborting...")
        sid = transaction.savepoint()
        question_slug = "flaeche-m"
        question = Question.objects.get(slug=question_slug)
        question.type = question.TYPE_TEXT
        question.save()
        log.info("Question was updated")
        for answer in question.answers.iterator():
            answer.value = str(answer.value)
            if answer.meta.get("gis-value", None):
                answer.meta["gis-value"] = str(answer.meta["gis-value"])
            answer.save()
            log.info(f"Answer {answer.pk} was updated")
        if options["commit"]:
            transaction.savepoint_commit(sid)
            log.info("Changes have been saved")
        else:
            log.warning("This command was run without --commit so no changes were made")
            transaction.savepoint_rollback(sid)
