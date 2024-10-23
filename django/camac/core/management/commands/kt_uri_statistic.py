import csv

from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Q


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
        for case in cases:
            data.append(
                {
                    "Jahr": case.meta["submit-date"][:4],
                    "Gemeinde": case.instance.location.name,
                    "Hochbau": "X"
                    if case.document.answers.filter(
                        question_id="category", value__contains="category-hochbaute"
                    ).first()
                    else "",
                    "Beheizte oder gekühlte Neu- und Umbauten": "X"
                    if case.document.answers.filter(
                        question_id="das-vorhaben-betrifft",
                        value__contains="das-vorhaben-betrifft-beheizte-oder-gekuehlte-neu-und-umbauten",
                    ).first()
                    else "",
                    "Die Änderung der Gebäudehülle beheizter oder gekühlter Bauten": "X"
                    if case.document.answers.filter(
                        question_id="das-vorhaben-betrifft",
                        value__contains="das-vorhaben-betrifft-aenderung-beheizter-oder-gekuehlter-bauten",
                    ).first()
                    else "",
                    "Die Installation / Änderung gebäudetechnischer Anlagen (Heizung, Lüftung, Klima- und / oder Kälteanlage)": "X"
                    if case.document.answers.filter(
                        question_id="das-vorhaben-betrifft",
                        value__contains="das-vorhaben-betrifft-installation-technischer-anlagen",
                    ).first()
                    else "",
                }
            )

        with open("statistic.csv", "w", newline="") as csvfile:
            fieldnames = [
                "Jahr",
                "Gemeinde",
                "Hochbau",
                "Beheizte oder gekühlte Neu- und Umbauten",
                "Die Änderung der Gebäudehülle beheizter oder gekühlter Bauten",
                "Die Installation / Änderung gebäudetechnischer Anlagen (Heizung, Lüftung, Klima- und / oder Kälteanlage)",
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
