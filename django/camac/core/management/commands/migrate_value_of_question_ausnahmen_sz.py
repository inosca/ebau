from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import FormField


class Command(BaseCommand):
    help = """Correct the typo for the question 'ausnahmen' in the question option."""

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

        form_fields = FormField.objects.filter(
            name="ausnahmen",
            value__contains="Unterschreitung Stassenabstand oder Verletzung Strassenbaulinie",
        )
        for form_field in form_fields:
            value = [
                val.replace("Stassenabstand", "Strassenabstand")
                for val in form_field.value
            ]
            form_field.value = value
            form_field.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
