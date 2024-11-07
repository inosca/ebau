import csv

from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

CATEGORIES = {
    "Hochbau": ("category", "category-hochbaute"),
    "Beheizte oder gekühlte Neu- und Umbauten": (
        "das-vorhaben-betrifft",
        "das-vorhaben-betrifft-beheizte-oder-gekuehlte-neu-und-umbauten",
    ),
    "Die Änderung der Gebäudehülle beheizter oder gekühlter Bauten": (
        "das-vorhaben-betrifft",
        "das-vorhaben-betrifft-aenderung-beheizter-oder-gekuehlter-bauten",
    ),
    "Die Installation / Änderung gebäudetechnischer Anlagen (Heizung, Lüftung, Klima- und / oder Kälteanlage)": (
        "das-vorhaben-betrifft",
        "das-vorhaben-betrifft-installation-technischer-anlagen",
    ),
}

BUILDING_TYPES = {
    "Einfamilienhaus freistehend": "art-der-hochbaute-einfamilienhaus",
    "Einfamilienhaus angebaut": "art-der-hochbaute-doppeleinfamilienhaus",
    "Mehrfamilienhaus": "art-der-hochbaute-mehrfamilienhaus",
    "Wohn- und Geschäftshaus": "art-der-hochbaute-wohn-und-geschaftshaus",
    "Industrie und Gewerbebaute": "art-der-hochbaute-industrie",
}

PROPOSALS = {
    "Neubau": "proposal-neubau",
    "Umbau": "proposal-umbau-erneuerung-sanierung",
}

RECONSTRUCTION = {
    "Energetische Sanierung": "umbau-energetische-sanierung",
    "Sanierung Heizsystem": "umbau-sanierung-des-heizsystems",
    "Photovoltaische Solaranlage": "umbau-photovoltaische-solaranlage",
}


class Command(BaseCommand):
    help = """Create a csv with statistics about instances"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        cases = Case.objects.filter(
            Q(**{"meta__submit-date__isnull": False})
            & Q(instance__isnull=False)
            & Q(instance__location__isnull=False)
        )

        data = []
        for counter, case in enumerate(cases):
            flat_answers = case.document.flat_answer_map()
            table_answer = flat_answers.get("gebaeude")

            entry = {
                "Jahr": case.meta["submit-date"][:4],
                "Gemeinde": case.instance.location.name,
            }

            for name, (key, expected) in CATEGORIES.items():
                entry[name] = (
                    1
                    if flat_answers.get(key) and expected in flat_answers.get(key)
                    else ""
                )

            if table_answer and table_answer[0]:
                for name, key in BUILDING_TYPES.items():
                    entry[name] = (
                        1 if table_answer[0].get("art-der-hochbaute") == key else ""
                    )

                for name, key in PROPOSALS.items():
                    entry[name] = (
                        1
                        if table_answer[0].get("proposal")
                        and key in table_answer[0].get("proposal")
                        else ""
                    )

                for name, key in RECONSTRUCTION.items():
                    entry[name] = (
                        1
                        if table_answer[0].get("umbau")
                        and key in table_answer[0].get("umbau")
                        else ""
                    )

            self.stdout.write(f"Prepared {counter} query")
            data.append(entry)

        with open("statistic.csv", "w", newline="") as csvfile:
            fieldnames = [
                "Jahr",
                "Gemeinde",
                "Hochbau",
                "Beheizte oder gekühlte Neu- und Umbauten",
                "Die Änderung der Gebäudehülle beheizter oder gekühlter Bauten",
                "Die Installation / Änderung gebäudetechnischer Anlagen (Heizung, Lüftung, Klima- und / oder Kälteanlage)",
                "Einfamilienhaus freistehend",
                "Einfamilienhaus angebaut",
                "Mehrfamilienhaus",
                "Wohn- und Geschäftshaus",
                "Industrie und Gewerbebaute",
                "Neubau",
                "Umbau",
                "Energetische Sanierung",
                "Sanierung Heizsystem",
                "Photovoltaische Solaranlage",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
