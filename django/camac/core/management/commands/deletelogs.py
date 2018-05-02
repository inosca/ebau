from datetime import timedelta

from django.apps import apps
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone

log_models = (
    'core.InstanceLog',
    'core.InstanceLocationLog',
    'core.NoticeLog',
    'core.ActivationAnswerLog',
    'core.ActivationLog',
    'core.AnswerLog',
    'core.CirculationLog',
)


class Command(BaseCommand):
    help = "Deletes logs of all Camac resources."

    def add_arguments(self, parser):
        parser.add_argument(
            "--days",
            default=180,
            type=int,
            help="Delete only logs older than the specified number of days.",
        )

    def handle(self, *args, **options):
        days = options["days"]
        clean_till = timezone.now() - timedelta(days=days)
        for model_name in log_models:
            self.stdout.write('Clean logs table {0}'.format(model_name))
            (app_label, model_name) = model_name.split(".")
            model = apps.get_model(app_label=app_label, model_name=model_name)

            model.objects.filter(modification_date__lt=clean_till).delete()

        call_command('deleterevisions', *args, **options)
