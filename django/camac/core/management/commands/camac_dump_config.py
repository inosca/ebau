import collections
import itertools
import os

from django.apps import apps
from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.serializers.json import Serializer
from django.db.models import Q

from camac.settings.modules.dump import DumpConfig


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

    def get_models(self):
        config = settings.DUMP["CONFIG"]
        config_models = set(config["MODELS"] + config["MODELS_REFERENCING_DATA"]) - set(
            config["EXCLUDED_MODELS"]
        )

        group_models = set(itertools.chain(*config["GROUPS"].values())) - config_models

        return [
            (
                identifier,
                *identifier.split("."),
                identifier in group_models,
            )
            for identifier in sorted(config_models | group_models)
        ]

    def handle(self, *app_labels, **options):
        dump_config = settings.DUMP["CONFIG"]
        filter_list = [
            (
                name,
                filters,
            )
            for name, filters in dump_config["GROUPS"].items()
        ]
        for model_identifier, app_label, model_label, group_only in self.get_models():
            model = apps.get_model(app_label, model_label)

            if not model._meta.managed:  # pragma: no cover
                continue

            excluded_pks = []

            for (
                filter_group,
                model_filters,
            ) in self.get_filter_groups_ordered_by_complexity(
                model_identifier, filter_list
            ):
                filtered_queryset = (
                    model.objects.exclude(pk__in=excluded_pks)
                    .filter(model_filters)
                    .distinct()
                    .order_by("pk")
                )

                excluded_pks += list(filtered_queryset.values_list("pk", flat=True))

                self.groups[filter_group].append(filtered_queryset)

            if not group_only:
                self.groups[app_label].append(
                    model.objects.exclude(pk__in=excluded_pks).order_by("pk")
                )

        self.dump(options["output_dir"])

    def get_filter_groups_ordered_by_complexity(
        self,
        model_identifier: str,
        filters: list[tuple[str, dict[str, Q] | DumpConfig]],
    ) -> list[tuple[str, Q]]:
        filter_list: list[tuple[str, Q]] = [
            (
                name,
                config[model_identifier],
            )
            for name, config in filters
            if model_identifier in config
        ]

        if not filter_list:
            return filter_list

        sorted_filter_list = sorted(
            filter_list,
            key=lambda tpl: self.get_condition_complexity_score(tpl[1]),
            reverse=True,
        )

        # The followign code block essentially just inserts the
        # dependencies in front of the groups defining them.
        filters_with_dependency: list[tuple[str, DumpConfig]] = [
            tpl for tpl in filters if isinstance(tpl[1], DumpConfig)
        ]
        for name, config in filters_with_dependency:
            try:
                config_index = next(
                    index
                    for index, config in enumerate(sorted_filter_list)
                    if config[0] == name
                )
                dependency_index, dependency_config = next(
                    (index, dependency_config)
                    for index, dependency_config in enumerate(sorted_filter_list)
                    if dependency_config[0] == config.dependency
                )
            except StopIteration:
                # A dependency is defined but the dependency has no
                # filters for the current model_identifier.
                continue

            del sorted_filter_list[dependency_index]
            sorted_filter_list.insert(config_index, dependency_config)

        return sorted_filter_list

    def get_condition_complexity_score(self, condition: Q) -> int:
        score = 0

        for child in condition.children:
            if isinstance(child, Q):  # pragma: no cover
                # This is not needed yet as we don't have any nested conditions.
                # However, we should leave it as otherwise no one will get why
                # it doesn't work as expected as soon as we have the use case.
                score += self.get_condition_complexity_score(child)
            else:
                score += 1

        return score
