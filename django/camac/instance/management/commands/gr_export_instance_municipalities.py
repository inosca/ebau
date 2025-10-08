import csv
import sys

from django.core.management.base import BaseCommand

from camac.instance.master_data import MasterData
from camac.instance.models import Instance


class Command(BaseCommand):
    """Management command to generate a statistic for the Kt. GR.

    This management shows for all instances excluding those in state "new":
    - Dossier number
    - Municipality
    - Responsible service
    - Application type
    - Submit date
    - Current state

    This statistics was needed in GR to get an overview of instances.
    """

    def handle(self, *args, **options):
        qs = Instance.objects.exclude(instance_state__name="new").order_by(
            "case__meta__dossier-number"
        )
        writer = csv.writer(
            sys.stdout, delimiter=";", quotechar='"', quoting=csv.QUOTE_ALL
        )

        print(f"\n# Auswertung Baugesuche Gemeinden - {qs.count()} dossier(s)")
        print("")
        writer.writerow(
            [
                "Dossier-Nummer",
                "Gemeinde",
                "Zuständige",
                "Verfahrensart",
                "Eingereicht am",
                "Status",
            ]
        )
        for instance in qs.iterator(chunk_size=50):
            master_data = MasterData(instance.case)
            instance_name = (
                instance.case.meta.get("dossier-number")
                if instance.case and instance.case.meta.get("dossier-number")
                else f"instance-{str(instance.pk)}"
            )

            writer.writerow(
                [
                    instance_name,
                    master_data.municipality_name,
                    instance.responsible_service().get_name(),
                    master_data.application_type,
                    master_data.submit_date,
                    instance.instance_state.get_name(),
                ]
            )

        self.stdout.write("")
        self.stdout.write(self.style.SUCCESS("Export complete"))
