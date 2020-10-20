# TODO: delete this command as soon as open MRs are rebased
from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand

from camac.core.management.commands.dumpconfig import (
    pure_config_models,
    pure_config_models_caluma_form,
    pure_config_models_caluma_workflow,
)


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
            "--caluma",
            dest="caluma",
            action="store_true",
            default=True,
            help="Load caluma config and data as well",
        )
        parser.add_argument(
            "--no-caluma",
            dest="caluma",
            action="store_false",
            help="Don't load caluma config and data",
        )

    def handle(self, *args, **options):
        config_fixtures = []
        data_fixtures = []

        model = get_user_model()
        try:
            # init.json only needs to be called when no admin user is
            # available in db
            model.objects.get(pk=1)
        except model.DoesNotExist:
            data_fixtures.append(settings.APPLICATION_DIR("init.json"))
            if settings.ENV != "production":
                # load test data in dev setup
                data_fixtures.append(settings.APPLICATION_DIR("data.json"))
                if options["caluma"]:
                    data_fixtures.append(
                        settings.APPLICATION_DIR("data-caluma-form.json")
                    )
                    data_fixtures.append(
                        settings.APPLICATION_DIR("data-caluma-workflow.json")
                    )

        # default application config
        config_fixtures.append(settings.APPLICATION_DIR("config.json"))
        if options["caluma"]:
            config_fixtures.append(settings.APPLICATION_DIR("config-caluma-form.json"))
            config_fixtures.append(
                settings.APPLICATION_DIR("config-caluma-workflow.json")
            )

        self.stdout.write("Flushing 'pure' config models")
        for model_name in (
            pure_config_models
            + pure_config_models_caluma_form
            + pure_config_models_caluma_workflow
        ):
            self.stdout.write("Deleting config table {0}".format(model_name))
            (app_label, model_name) = model_name.split(".")
            model = apps.get_model(app_label=app_label, model_name=model_name)
            model.objects.all().delete()

        fixtures = config_fixtures + data_fixtures
        self.stdout.write("Loading config {0}".format(", ".join(fixtures)))
        call_command("loaddata", *fixtures)

        sequence_apps = settings.APPLICATION.get("SEQUENCE_NAMESPACE_APPS")
        if sequence_apps:
            call_command(
                "sequencenamespace", *sequence_apps, user=options["user"], execute=True
            )
