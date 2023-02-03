from caluma.caluma_form.models import Answer, Question
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Change the value of existing 'oereb-thema' answers to 'Gemeindliche Nutzungsplanung'."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        # change type of question from multiple-choice to single-choice
        question = Question.objects.get(slug="oereb-thema")
        question.type = "choice"
        question.save()

        answers = Answer.objects.filter(question_id="oereb-thema")
        for answer in answers:
            if len(answer.value) > 1:
                answer.value = "oereb-thema-gnp"
            else:
                answer.value = answer.value[0]
            answer.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
