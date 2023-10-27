from caluma.caluma_form.models import Form
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q


class Command(BaseCommand):
    help = """Change all questions in the special forms (except BAB, Betriebsleiterwohnhaus and Stallbau und Hofdünger) to not required."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        excluded_forms = [
            "bauten-ausserhalb-bauzone",
            "betriebsleiterwohnhaus",
            "stallbau-und-hofduengerlager",
        ]

        special_forms = (
            Form.objects.filter(slug="spezialformulare")
            .first()
            .questions.exclude(slug__in=excluded_forms)
        )

        for special_form in special_forms:
            questions = special_form.sub_form.questions.all().exclude(
                Q(type="static") | Q(type="table")
            )
            for question in questions:
                question.is_required = "false"
                question.save()

            table_questions = special_form.sub_form.questions.filter(
                type="table"
            ).exclude(row_form__slug="personalien-tabelle")
            for question in table_questions:
                question.is_required = "false"
                question.save()

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
