import csv

import magic
from django.core.management.base import BaseCommand

from camac.user.models import ServiceT


def _load_csv():
    data = []
    file = "camac/core/translation_files/GR_SERVICES/Service_name_it.csv"

    blob = open(file, "rb").read()
    m = magic.open(magic.MAGIC_MIME_ENCODING)
    m.load()
    encoding = m.buffer(blob)
    print(f"detected encoding of {file} as {encoding}")
    with open(file, encoding=encoding) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        line_count = 0
        for item in csv_reader:
            if line_count == 0:
                pass
            else:
                data.append({"pk": item[0], "de_name": item[1], "translation": item[2]})
            line_count += 1
    return data


def _upload_data(data):
    for row in data:
        try:
            if ServiceT.objects.filter(service_id=row["pk"]).exists():
                _, created = ServiceT.objects.update_or_create(
                    language="it", name=row["translation"], service_id=row["pk"]
                )
            else:
                service = ServiceT.objects.filter(name=row["de_name"]).first()

                if not service:
                    print(
                        f"Service {row['de_name']} not found",
                    )
                    continue

                _, created = ServiceT.objects.update_or_create(
                    language="it", name=row["translation"], service_id=service.pk
                )
            if created:
                print(f"ServiceT({row['pk']}) was created: {row}")

        except Exception:
            breakpoint()
            pass


class Command(BaseCommand):
    def handle(self, *args, **option):
        print("importing Service")
        _upload_data(_load_csv())
