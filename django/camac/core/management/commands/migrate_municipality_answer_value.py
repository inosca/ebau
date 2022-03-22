from caluma.caluma_form.models import Answer, DynamicOption
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import Location


class Command(BaseCommand):
    help = """Migrate the answers of the municipality question from location ids to communal federal numbers."""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        municipality_answers = Answer.objects.filter(
            question_id="municipality", value__isnull=False
        )

        answer_counter = 0
        for answer in municipality_answers.iterator():
            answer.value = Location.objects.get(
                pk=int(answer.value)
            ).communal_federal_number
            answer.save()
            answer_counter += 1

        self.stdout.write(f"{answer_counter} municipality answer values were migrated")

        municipality_dynamic_options = DynamicOption.objects.filter(
            question_id="municipality"
        )

        dynamic_option_counter = 0
        for dynamic_option in municipality_dynamic_options.iterator():
            dynamic_option.slug = Location.objects.get(
                pk=int(dynamic_option.slug)
            ).communal_federal_number
            dynamic_option.save()
            dynamic_option_counter += 1

        self.stdout.write(f"{dynamic_option_counter} dynamic options were migrated")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
