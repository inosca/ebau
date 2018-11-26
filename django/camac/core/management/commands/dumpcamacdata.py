import io
import json

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from .dumpconfig import models_referencing_data, pure_config_models


class Command(BaseCommand):
    help = "Output the camac data of the database as a fixture of the " "given format."

    def handle(self, *app_labels, **options):
        options["indent"] = 2
        options["exclude"] = pure_config_models + models_referencing_data

        # apps which include data models
        apps = ("circulation", "core", "document", "instance", "notification", "user")

        try:
            output = options.pop("output")
        except KeyError:  # pragma: no cover
            output = settings.APPLICATION_DIR("data.json")
        tmp_output = io.StringIO()
        options["stdout"] = tmp_output
        call_command("dumpdata", *apps, **options)
        tmp_output.seek(0)
        data = json.load(tmp_output)
        data = sorted(data, key=lambda k: (k["model"], k["pk"]))

        with open(output, "w") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.flush()
