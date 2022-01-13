import functools

from caluma.caluma_form.models import Answer, Document, Question
from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from simple_history.utils import bulk_create_with_history

from camac.core.models import Answer as CamacAnswer

# item, chapter, question
ANSWER_MAPPING = {
    "ebau-number-has-existing": (1, 20000, 20034),
    "ebau-number-existing": (1, 20000, 20035),
}


def icq_dict(icq_tuple):
    item, chapter, question = icq_tuple
    return {"item": item, "chapter": chapter, "question": question}


def get_answers_by_mapping(instance, mapping):
    raw_filters = [Q(**icq_dict(icq_tuple)) for icq_tuple in mapping.values()]

    filters = functools.reduce(lambda a, b: a | b, raw_filters)

    return CamacAnswer.objects.filter(Q(instance=instance) & filters)


def get_question_slug(mapping, question_id):
    for slug, icq_tuple in mapping.items():
        if icq_dict(icq_tuple).get("question") == question_id:
            return slug

    raise Exception(f"No slug for question '{question_id}' found")


class Command(BaseCommand):
    help = "Migrates the old camac form for 'ebau nummer vergeben' to a caluma form"

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        ebau_number_work_items = WorkItem.objects.filter(task_id="ebau-number")

        count = ebau_number_work_items.count()

        for i, work_item in enumerate(ebau_number_work_items):
            instance = work_item.case.instance

            assign_ebau_number_document = Document.objects.create(form_id="ebau-number")

            work_item.document = assign_ebau_number_document
            work_item.save()

            self._migrate_assign_ebau_number(instance, assign_ebau_number_document)

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully migrated the form 'assign ebau number' of instance {instance.pk}\t({i+1} / {count})"
                )
            )

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _migrate_assign_ebau_number(self, instance, document):
        answers = get_answers_by_mapping(instance, ANSWER_MAPPING)

        if not answers.exists():
            return

        caluma_answers = []

        for answer in answers:
            question = Question.objects.get(
                pk=get_question_slug(ANSWER_MAPPING, answer.question_id)
            )
            if answer.answer in ["yes", "no"]:
                suffix = {
                    "yes": "-ja",
                    "no": "-nein",
                }
                option = question.pk + suffix[answer.answer]
                value = question.options.get(pk=option).pk
            else:
                value = answer.answer

            caluma_answers.append(
                Answer(
                    document=document,
                    question=question,
                    value=value,
                )
            )

        bulk_create_with_history(caluma_answers, Answer)
