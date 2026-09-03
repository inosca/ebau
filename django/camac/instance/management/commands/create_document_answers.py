import json
from uuid import UUID

from caluma.caluma_form.models import Answer, Document, DynamicOption, Question
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Exists, OuterRef, Q


def uuid(string: str) -> UUID:
    return UUID(string)


class Command(BaseCommand):
    help = "Populates empty form questions with a given answer value"

    def add_arguments(self, parser):
        parser.add_argument(
            "--document",
            type=uuid,
            dest="document_id",
            help="UUID of target document",
            required=False,
        )
        parser.add_argument(
            "--form",
            type=str,
            dest="form_id",
            help="Slug of target form type",
            required=True,
        )
        parser.add_argument(
            "--question",
            type=str,
            dest="question_id",
            help="Slug of target question",
            required=True,
        )
        parser.add_argument(
            "--value",
            type=str,
            dest="value",
            help="Value of target answer",
            required=True,
        )
        parser.add_argument(
            "--label",
            type=json.loads,
            dest="label",
            help='Translation label of target answer in JSON form: \'{"de": "Label", "fr": null, "it": null}\'',
            required=False,
        )
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        question = Question.objects.get(pk=options["question_id"])

        document_filter = (
            {"pk": options["document_id"]} if options["document_id"] else {}
        )

        answer_exists = Answer.objects.filter(
            document=OuterRef("pk"), question=question
        )

        documents = Document.objects.filter(
            Q(form_id=options["form_id"], **document_filter) & ~Exists(answer_exists)
        )

        username = settings.APPLICATION["SYSTEM_USER"] or "service-account-camac-admin"

        answer_dict = {
            "question": question,
            "created_by_user": username,
        }
        dynamic_option_dict = {
            "question": question,
            "created_by_user": username,
        }
        answer_values = []
        dynamic_option_values = []

        if question.type in [
            Question.TYPE_DYNAMIC_CHOICE,
            Question.TYPE_DYNAMIC_MULTIPLE_CHOICE,
        ]:
            dynamic_option_dict.update(
                {
                    "slug": options["value"],
                    "label": options["label"] or options["value"],
                }
            )

        # TODO: Add support for linked answers
        if question.type in [Question.TYPE_FORM, Question.TYPE_TABLE]:
            raise CommandError(f"Unsupported question type: {question.type}")
        elif question.type == Question.TYPE_DATE:
            answer_dict.update({"date": options["value"]})
        else:
            answer_dict.update({"value": options["value"]})

        for document in documents:
            answer_values.append(Answer(document=document, **answer_dict))

            if question.type in [
                Question.TYPE_DYNAMIC_CHOICE,
                Question.TYPE_DYNAMIC_MULTIPLE_CHOICE,
            ]:
                dynamic_option_values.append(
                    DynamicOption(document=document, **dynamic_option_dict)
                )

        DynamicOption.objects.bulk_create(dynamic_option_values)
        Answer.objects.bulk_create(answer_values)

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)
