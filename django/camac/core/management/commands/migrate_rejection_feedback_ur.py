from django.core.management.base import BaseCommand
from django.db import transaction

from camac.constants import kt_uri as uri_constants
from camac.core.models import (
    Answer as CamacAnswer,
)


class Command(BaseCommand):
    help = """Migrate the old camac answers to the new caluma answers for the rejection feedback"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        camac_answers = CamacAnswer.objects.filter(
            chapter_id=uri_constants.REJECTION_FEEDBACK_CHAPTER_ID,
            question_id=uri_constants.REJECTION_FEEDBACK_QUESTION_ID,
        )

        counter = 0
        for answer in camac_answers:
            answer.instance.rejection_feedback = answer.answer
            answer.instance.save()
            self.stdout.write(
                f"Rejection feedback of instance {answer.instance.pk} was migrated"
            )
            counter += 1

        self.stdout.write(f"{counter} rejection feedbacks were migrated")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
