from django.conf import settings
from django.core.management.commands import dumpdata

from .dumpconfig import models_referencing_data, pure_config_models


class Command(dumpdata.Command):
    help = (
        "Output the camac data of the database as a fixture of the "
        "given format."
    )

    def handle(self, *app_labels, **options):
        options['indent'] = 2
        options['exclude'] = pure_config_models + models_referencing_data
        options['output'] = (
            options.get('output') or settings.APPLICATION_DIR('data.json')
        )

        # apps which include data models
        apps = (
            'circulation',
            'core',
            'document',
            'instance',
            'notification',
            'user',
        )

        super().handle(
            *apps,
            **options
        )
