from caluma.caluma_form.models import Answer
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Migrate all answers from question 'proposal-description' on 'bgbb' forms to new question 'beschrieb-verfahren' """

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        Answer.objects.filter(
            question_id="proposal-description", document__form_id="bgbb"
        ).update(question_id="beschrieb-verfahren")

        category_answers = Answer.objects.filter(
            question_id="category", document__form_id="bgbb"
        )

        for answer in category_answers:
            if "category-hochbaute" in answer.value:
                Answer.objects.create(
                    question_id="hochbauten-betroffen",
                    document=answer.document,
                    value="hochbauten-betroffen-ja",
                )
                self.stdout.write(
                    f"Question with slug 'hochbauten-betroffen' was created for Instance {answer.document.case.instance.pk}"
                )
            elif [
                category
                for category in answer.value
                if category
                in ["category-tiefbaute", "category-spezielle-bauten-und-anlagen"]
            ]:
                Answer.objects.create(
                    question_id="hochbauten-betroffen",
                    document=answer.document,
                    value="hochbauten-betroffen-nein",
                )
                self.stdout.write(
                    f"Question with slug 'hochbauten-betroffen' was created for Instance {answer.document.case.instance.pk}"
                )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
