from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


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

        # default application config
        fixtures.append(settings.APPLICATION_DIR('config.json'))

        self.stdout.write('Loading config {0}'.format(', '.join(fixtures)))
        call_command('loaddata', *fixtures, **options)
