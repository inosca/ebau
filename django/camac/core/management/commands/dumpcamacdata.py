# TODO: delete this command as soon as open MRs are rebased
import io
import json

from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand

from .dumpconfig import (
    models_managed_by_customer,
    models_referencing_data,
    models_referencing_data_caluma_form,
    models_referencing_data_caluma_workflow,
    pure_config_models,
    pure_config_models_caluma_form,
    pure_config_models_caluma_workflow,
    view_models,
)


class Command(BaseCommand):
    help = "Output the camac data of the database as a fixture of the " "given format."

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            type=str,
            default=settings.APPLICATION_DIR("data.json"),
            help="Output file for camac data",
        )
        parser.add_argument(
            "--output-caluma-form",
            dest="output_caluma_form",
            type=str,
            default=settings.APPLICATION_DIR("data-caluma-form.json"),
            help="Output file for caluma form data",
        )

        parser.add_argument(
            "--output-caluma-workflow",
            dest="output_caluma_workflow",
            type=str,
            default=settings.APPLICATION_DIR("data-caluma-workflow.json"),
            help="Output file for caluma workflow data",
        )

        parser.add_argument(
            "--caluma",
            dest="caluma",
            action="store_true",
            help="Dump caluma data as well",
        )
        parser.add_argument(
            "--no-caluma",
            dest="caluma",
            action="store_false",
            help="Don't dump caluma data",
        )

        parser.set_defaults(
            caluma=settings.APPLICATION_NAME in ["kt_bern", "kt_schwyz"]
        )

    def dump_data(self, apps, exclude, output):
        tmp_output = io.StringIO()
        call_command("dumpdata", *apps, stdout=tmp_output, indent=2, exclude=exclude)
        tmp_output.seek(0)
        data = json.load(tmp_output)
        data = sorted(data, key=lambda k: (k["model"], k["pk"]))

        with open(output, "w") as f:
            json.dump(data, f, indent=2, sort_keys=True)
            f.flush()

    def handle(self, *app_labels, **options):
        self.dump_data(
            # apps which include data models
            (
                "circulation",
                "core",
                "document",
                "instance",
                "notification",
                "user",
                "applicants",
            ),
            # respect customer specific excludes
            [
                m
                for m in pure_config_models + models_referencing_data
                if m not in models_managed_by_customer[settings.APPLICATION_NAME]
            ]
            + view_models,
            options["output"],
        )

        if options["caluma"]:
            self.dump_data(
                ("caluma_form",),
                pure_config_models_caluma_form + models_referencing_data_caluma_form,
                options["output_caluma_form"],
            )
            self.dump_data(
                ("caluma_workflow",),
                pure_config_models_caluma_workflow
                + models_referencing_data_caluma_workflow,
                options["output_caluma_workflow"],
            )
