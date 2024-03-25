from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count

from camac.core.utils import generate_sort_key
from camac.instance.domain_logic import CreateInstanceLogic


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        """Re-assign dossier numbers where there are collisions.

        Collisions should never happen, this fixes situations where it did anyway automatically
        by assigning the next available number to cases with duplicate numbers.
        """
        sid = transaction.savepoint()

        dupes = (
            Case.objects.values("meta__dossier-number")
            .annotate(Count("id"))
            .filter(**{"meta__dossier-number__isnull": False})
            .filter(id__count__gt=1)
        )
        for dupe in dupes:
            cases = Case.objects.filter(
                **{"meta__dossier-number": dupe["meta__dossier-number"]}
            ).order_by("meta__submit-date")[1:]
            for case in cases:
                prev_year = int(case.meta["dossier-number"][:4])
                identifier = CreateInstanceLogic.generate_identifier(
                    case.instance, year=prev_year
                )
                print(
                    f"reassigning case ID {identifier} to case {case.id} (previously {case.meta['dossier-number']})"
                )
                case.meta["dossier-number"] = identifier
                case.meta["dossier-number-sort"] = generate_sort_key(identifier)
                case.save()

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
