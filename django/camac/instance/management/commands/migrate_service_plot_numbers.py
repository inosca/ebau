from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand


def transform_plot_number(old_value):
    # This is the first use-case (Kt. AG - Villachern -> Brugg).
    # Consider making this more generic once a few use-case have been collected.
    if int(old_value) < 7000:
        return int(old_value) + 7000
    return int(old_value)


class Command(BaseCommand):
    help = """Transforms plot numbers of migrated services.

    Requires migrated instances to be marked (see migrate_services.py 'log_to_case_meta')"""

    def add_arguments(self, parser):
        parser.add_argument(
            "-s",
            "--service",
            type=int,
            dest="service_id",
            help="Service PK",
            required=True,
        )
        parser.add_argument(
            "-e",
            "--execute",
            default=False,
            dest="exec",
            action="store_true",
            help="Execute the transformation instead of just logging",
        )

    def handle(self, *args, **options):
        service_id = options["service_id"]

        cases = Case.objects.filter(**{"meta__migrated-from-service": service_id})

        for case in cases:
            row_answer = case.document.answers.filter(question_id="parzelle").first()
            for row in row_answer.documents.all():
                answer = row.answers.filter(question_id="parzellennummer").first()
                prev_value = answer.value
                answer.value = transform_plot_number(answer.value)

                action = "Updated" if options["exec"] else "Would update"
                if options["exec"]:
                    answer.save()
                self.stdout.write(
                    f"{action} plot number in instance {case.instance.pk} from {prev_value} to {answer.value}"
                )
