from caluma.caluma_form.models import Form, Option, Question
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count


class Command(BaseCommand):
    help = "Deletes dangling questions and options from the caluma config"

    def add_arguments(self, parser):
        parser.add_argument(
            "-d", "--dry", action="store_true", help="Dry run only, no changes"
        )

    @transaction.atomic
    def handle(self, *args, **options):
        dry = options["dry"]
        sid = transaction.savepoint()

        questions = Question.objects.annotate(count=Count("forms__pk")).filter(count=0)
        self._log(questions, "questions")
        questions.delete()

        options = Option.objects.annotate(count=Count("questions__pk")).filter(count=0)
        self._log(options, "options")
        options.delete()

        row_forms = Question.objects.filter(row_form__isnull=False).values_list(
            "row_form_id", flat=True
        )
        sub_forms = Question.objects.filter(sub_form__isnull=False).values_list(
            "sub_form_id", flat=True
        )
        excluded_forms = [
            "dashboard"
        ]  # this is being used without workflow or other forms

        forms = (
            Form.objects.exclude(pk__in=[*row_forms, *sub_forms, *excluded_forms])
            .annotate(
                workflow_count=Count("workflows__pk"), task_count=Count("tasks__pk")
            )
            .filter(workflow_count=0, task_count=0)
        )
        self._log(forms, "forms")
        forms.delete()

        if dry:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def _log(self, objects, name):
        print(f"{objects.count()} {name} will be deleted:\n")
        print(
            "".join(
                [
                    f"- {pk}\n"
                    for pk in objects.order_by("pk").values_list("pk", flat=True)
                ]
            )
        )
