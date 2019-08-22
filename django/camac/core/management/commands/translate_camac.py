import csv

from django.core.management.base import BaseCommand

from camac.core.models import InstanceResourceT, ResourceT

config = [
    (
        ResourceT,
        "camac/core/translation_files/resource_t.csv",
        "resource_id",
        "Resources",
    ),
    (
        InstanceResourceT,
        "camac/core/translation_files/instance_resource_t.csv",
        "instance_resource_id",
        "Instance Resources",
    ),
]


def _load_csv(translation_file):
    """Load a csv file and return a list with translations."""
    with open(translation_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        data = []
        for item in csv_reader:
            if line_count == 0:
                pass  # skip header
            else:
                row = [item[0], item[1], item[2]]
                data.append(row)
            line_count += 1
        return data


class Command(BaseCommand):
    def handle(self, *args, **option):
        for (model, file, key, name) in config:
            self._write_translations(model, _load_csv(file), key, name)

    def _write_translations(self, model, translations, key, name):
        """Write french translations into the db."""
        model_objects = model.objects.all()
        count_skipped = 0
        count_created = 0
        for row in model_objects:
            try:
                match = next((t for t in translations if t[0] == row.name))
                additional_params = {key: getattr(row, key)}
                _, created = model.objects.get_or_create(
                    language="fr", name=match[1], **additional_params
                )
                if created:
                    count_created += 1
                else:
                    count_skipped += 1

            except (StopIteration):
                pass

        self.stdout.write(
            f"{count_created + count_skipped} {name} translations were processed ({count_created} created, {count_skipped} skipped)"
        )
