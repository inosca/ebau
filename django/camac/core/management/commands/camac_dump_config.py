import collections
import itertools
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import Serializer

from camac import dump_settings as config


class CamacDumpSerializer(Serializer):
    def handle_m2m_field(self, obj, field):
        super().handle_m2m_field(obj, field)

        if field.name in self._current:
            self._current[field.name] = sorted(self._current[field.name])


class Command(BaseCommand):
    help = "Output the configuration of the application as grouped fixtures"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.groups = collections.defaultdict(list)

    def add_arguments(self, parser):
        parser.add_argument(
            "--output-dir",
            dest="output_dir",
            type=str,
            default=settings.APPLICATION_DIR("config"),
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

    def get_models(self):
        config_models = set(
            config.DUMP_CONFIG_MODELS + config.DUMP_CONFIG_MODELS_REFERENCING_DATA
        ) - set(
            config.DUMP_CONFIG_EXCLUDED_MODELS
            + settings.APPLICATION.get("DUMP_CONFIG_EXCLUDED_MODELS", [])
        )
        group_models = set(itertools.chain(*self.get_groups().values())) - config_models

        return [
            (
                identifier,
                *identifier.split("."),
                identifier in group_models,
            )
            for identifier in sorted(config_models | group_models)
        ]

    def handle(self, *app_labels, **options):
        for model_identifier, app_label, model_label, group_only in self.get_models():
            model = apps.get_model(app_label, model_label)

            if not model._meta.managed:  # pragma: no cover
                continue

            excluded_pks = []

            for filter_group, model_filters in self.get_groups().items():
                if model_identifier in model_filters:
                    filtered_queryset = (
                        model.objects.exclude(pk__in=excluded_pks)
                        .filter(model_filters[model_identifier])
                        .order_by("pk")
                    )

                    excluded_pks += list(filtered_queryset.values_list("pk", flat=True))

                    self.groups[filter_group].append(filtered_queryset)

            if not group_only:
                self.groups[app_label].append(
                    model.objects.exclude(pk__in=excluded_pks).order_by("pk")
                )

        self.dump(options["output_dir"])
