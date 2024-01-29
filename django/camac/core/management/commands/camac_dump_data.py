import collections
import itertools
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand

from camac.settings import dump as config

from .camac_dump_config import CamacDumpSerializer


class Command(BaseCommand):
    help = "Output the data of the application as grouped fixtures"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groups = collections.defaultdict(list)

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            dest="output_dir",
            type=str,
            default=settings.APPLICATION_DIR("data"),
            help="Output dir for config files",
        )

    def dump(self, output_dir):
        serializer = CamacDumpSerializer()

        for group_name, querysets in self.groups.items():
            filename = os.path.join(output_dir, f"{group_name}.json")
            with open(filename, "w") as out:
                serializer.serialize(itertools.chain(*querysets), indent=2, stream=out)

    def get_groups(self):
        return {
            **config.DUMP_CONFIG_GROUPS,
            **settings.APPLICATION.get("DUMP_CONFIG_GROUPS", {}),
        }

    def handle(self, *app_labels, **options):
        excluded_models = set(
            config.DUMP_CONFIG_MODELS
            + config.DUMP_CONFIG_MODELS_REFERENCING_DATA
            + config.DUMP_DATA_EXCLUDED_MODELS
        ) - set(
            config.DUMP_CONFIG_EXCLUDED_MODELS
            + settings.APPLICATION.get("DUMP_CONFIG_EXCLUDED_MODELS", [])
        )

        for app_label in sorted(config.DUMP_DATA_APPS):
            app_config = apps.get_app_config(app_label)

            for model in app_config.get_models():
                model_identifier = f"{app_label}.{model.__name__}"
                excluded_pks = []

                if model_identifier in excluded_models or not model._meta.managed:
                    continue

                for filter_group, model_filters in self.get_groups().items():
                    if model_identifier in model_filters:
                        # exclude models that are used in config group
                        excluded_pks += list(
                            model.objects.exclude(pk__in=excluded_pks)
                            .filter(model_filters[model_identifier])
                            .order_by("pk")
                            .values_list("pk", flat=True)
                        )

                self.groups[app_label].append(
                    model.objects.exclude(pk__in=excluded_pks).order_by("pk")
                )

        self.dump(options["output_dir"])
