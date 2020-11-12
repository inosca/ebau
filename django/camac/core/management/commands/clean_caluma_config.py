from caluma.caluma_form.models import Answer, Document, Form, Option, Question
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count


class Command(BaseCommand):
    help = "Deletes dangling questions and options from the caluma config"

    def add_arguments(self, parser):
        parser.add_argument(
            "-d", "--dry", action="store_true", help="Dry run only, no changes"
        )
        parser.add_argument(
            "-c",
            "--cascade",
            dest="cascade",
            action="store_true",
            help="Cascade answers and documents of removed questions and forms",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.questions = []
        self.answers = []
        self.options = []
        self.forms = []
        self.documents = []

    @transaction.atomic
    def handle(self, *args, **options):
        self.cascade = options["cascade"]

        sid = transaction.savepoint()

        while any([self.clean_questions(), self.clean_options(), self.clean_forms()]):
            pass

        self.log((self.questions, "questions"), (self.answers, "answers"))
        self.log((self.options, "options"))
        self.log((self.forms, "forms"), (self.documents, "documents"))

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def log(self, blueprint_tuple, data_tuple=None):
        blueprint_pks, blueprint_name = blueprint_tuple

        if data_tuple:
            data_pks, data_name = data_tuple

        if self.cascade and data_tuple:
            text = f"Deleted {len(blueprint_pks)} {blueprint_name} and {len(data_pks)} related {data_name}:"
        else:
            text = f"Deleted {len(blueprint_pks)} {blueprint_name}:"

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS(text))

        if len(blueprint_pks):
            self.stdout.write("")
            self.stdout.write("\n".join([f"- {pk}" for pk in blueprint_pks]))

    def clean_questions(self):
        questions = Question.objects.annotate(count=Count("forms__pk")).filter(count=0)
        retval = questions.exists()
        self.questions.extend(questions.values_list("pk", flat=True))

        if self.cascade:
            answers = Answer.objects.filter(question__in=questions)
            self.answers.extend(answers.values_list("pk", flat=True))
            answers.delete()

        questions.delete()

        return retval

    def clean_options(self):
        options = Option.objects.annotate(count=Count("questions__pk")).filter(count=0)
        retval = options.exists()
        self.options.extend(options.values_list("pk", flat=True))
        options.delete()

        return retval

    def clean_forms(self):
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
        retval = forms.exists()
        self.forms.extend(forms.values_list("pk", flat=True))

        if self.cascade:
            documents = Document.objects.filter(form__in=forms)
            self.documents.extend(documents.values_list("pk", flat=True))
            documents.delete()

        forms.delete()

        return retval
