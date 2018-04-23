from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from camac.core.management.commands.dumpconfig import pure_config_models


class Command(BaseCommand):
    help = (
        "Load the camac configuration of the database"
    )

    def handle(self, *args, **options):
        fixtures = []

        model = get_user_model()
        try:
            # init.json only needs to be called when no admin user is
            # available in db
            model.objects.get(pk=1)
        except model.DoesNotExist:
            fixtures.append(settings.APPLICATION_DIR('init.json'))
            if settings.ENV != 'production':
                # load test data in dev setup
                fixtures.append(settings.APPLICATION_DIR('data.json'))

        # default application config
        fixtures.append(settings.APPLICATION_DIR('config.json'))

        print("Flushing 'pure' config models")
        for model_name in pure_config_models:
            self.stdout.write('Deleting config table {0}'.format(model_name))
            (app_label, model_name) = model_name.split(".")
            model = apps.get_model(app_label=app_label, model_name=model_name)
            model.objects.all().delete()

        self.stdout.write('Loading config {0}'.format(', '.join(fixtures)))
        call_command('loaddata', *fixtures, **options)
