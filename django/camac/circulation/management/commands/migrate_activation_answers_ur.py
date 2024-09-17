from caluma.caluma_form.models import Answer
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.core.models import ActivationAnswer
from camac.user.models import Service


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--reset", dest="reset", action="store_true", default=False)

    def reset(self):
        Answer.objects.filter(
            **{"meta__migrated-actvation-answer__isnull": False}
        ).delete()

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("reset"):
            self.reset()

        fill_inquiry_work_items = WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
        )

        for work_item in tqdm(fill_inquiry_work_items, mininterval=1, maxinterval=2):
            addressed_service = Service.objects.get(pk__in=work_item.addressed_groups)

            message_to_applicant = ActivationAnswer.objects.filter(
                question_id=242,  # "Mitteilung an Gesuchsteller"
                activation__service=addressed_service,
                activation__circulation__instance=work_item.case.family.instance,
            ).first()

            if message_to_applicant:
                answer, _created = Answer.objects.get_or_create(
                    question_id="inquiry-answer-applicant-message",
                    document=work_item.case.document,
                    meta={"migrated-activation-answer": message_to_applicant.pk},
                )
                answer.value = message_to_applicant.answer
                answer.save()

                tqdm.write(f"Migrated activation answer #{message_to_applicant.pk}")

        tqdm.write("Completed migration")
