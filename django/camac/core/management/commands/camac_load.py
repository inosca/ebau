import os
import warnings
from glob import glob

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from camac.settings import dump as config


class Command(BaseCommand):
    help = "Load the camac configuration of the database"

    def add_arguments(self, parser):
        parser.add_argument(
            "--user",
            default=None,
            help="Username to set the namespace to. "
            "See settings.SEQUENCE_NAMESPACES",
            required=False,
        )
        parser.add_argument(
            "--no-data",
            action="store_true",
            dest="no_data",
            help="Don't load any data",
            required=False,
        )

    def get_fixtures_in_path(self, path):
        return sorted(glob(os.path.join(path, "*.json")))

    def handle(self, *args, **options):
        fixtures = self.get_fixtures_in_path(settings.APPLICATION_DIR("config"))

        if not options["no_data"]:
            model = get_user_model()
            try:
                # init.json only needs to be called when no admin user is
                # available in db
                model.objects.get(pk=1)
            except model.DoesNotExist:
                fixtures.append(settings.APPLICATION_DIR("init.json"))
                if settings.ENV != "production":
                    # load test data in dev setup
                    fixtures += self.get_fixtures_in_path(
                        settings.APPLICATION_DIR("data")
                    )

        self.stdout.write("Flushing 'pure' config models...")
        for model_name in set(config.DUMP_CONFIG_MODELS) - set(
            config.DUMP_CONFIG_EXCLUDED_MODELS
        ):
            (app_label, model_name) = model_name.split(".")
            model = apps.get_model(app_label=app_label, model_name=model_name)
            model.objects.all().delete()

        self.stdout.write("Loading fixtures...")
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="No fixture data found")
            call_command("loaddata", *fixtures)

        sequence_apps = settings.APPLICATION.get("SEQUENCE_NAMESPACE_APPS")
        if sequence_apps and options["user"]:
            self.stdout.write("Initializing sequence namespaces...")
            call_command(
                "sequencenamespace", *sequence_apps, user=options["user"], execute=True
            )
