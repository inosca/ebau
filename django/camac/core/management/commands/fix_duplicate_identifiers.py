from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.utils.translation import gettext as _

from camac.core.models import HistoryActionConfig
from camac.core.utils import create_history_entry, generate_sort_key
from camac.instance.domain_logic import CreateInstanceLogic
from camac.tags.models import Keyword


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--add-history", dest="add_history", action="store_true", default=False
        )
        parser.add_argument(
            "--add-keyword", dest="add_keyword", action="store_true", default=False
        )
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)
        parser.add_argument(
            "--select",
            dest="select",
            type=str,
            default="",
            help="Comma-separated list of instance IDs to select for re-assignment for each duplicate. If not provided, the newer identifiers will be selected automatically.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        """Re-assign dossier numbers where there are collisions.

        Collisions should never happen, this fixes situations where it did anyway automatically
        by assigning the next available number to cases with duplicate numbers.
        """
        sid = transaction.savepoint()

        select_list = [x.strip() for x in options["select"].split(",") if x.strip()]

        dupes = (
            Case.objects.values("meta__dossier-number")
            .annotate(Count("id"))
            .filter(**{"meta__dossier-number__isnull": False})
            .filter(id__count__gt=1)
            .order_by("meta__dossier-number")
        )
        for dupe in dupes:
            if select_list:
                # when selecting manually, only one case should be found for each duplicate.
                cases = Case.objects.filter(
                    **{"meta__dossier-number": dupe["meta__dossier-number"]}
                ).filter(instance__pk__in=select_list)

                if cases.count() > 1:  # pragma: no cover
                    raise ValueError(
                        f"When using --select, only one case should be found for each duplicate, but {cases.count()} were found for {dupe['meta__dossier-number']} -> {', '.join([str(c.instance.pk) for c in cases])}"
                    )
            else:
                # when selecting automatically, skip the first case and replace the newer
                # identifiers.
                cases = Case.objects.filter(
                    **{"meta__dossier-number": dupe["meta__dossier-number"]}
                ).order_by("meta__submit-date")[1:]

            for case in cases:
                old_identifier = case.meta["dossier-number"]
                prev_year = int(old_identifier[:4])
                identifier = CreateInstanceLogic.generate_identifier(
                    case.instance, year=prev_year
                )
                instance_id = case.family.instance.pk
                print(
                    f"reassigning case ID {identifier} (instance {instance_id}) to case {case.id} (previously {old_identifier})"
                )
                case.meta["dossier-number"] = identifier
                case.meta["dossier-number-sort"] = generate_sort_key(identifier)
                case.save()

                instance = case.family.instance

                # add a history entry to document the change.
                if options["add_history"]:
                    create_history_entry(
                        instance=instance,
                        user=None,
                        text=_(
                            "Reassigned dossier number from %(old_identifier)s to %(new_identifier)s."
                        )
                        % {
                            "old_identifier": old_identifier,
                            "new_identifier": identifier,
                        },
                        history_type=HistoryActionConfig.HISTORY_TYPE_NOTIFICATION,
                    )

                # add a keyword for search with the original identifier.
                if options["add_keyword"]:
                    instance.keywords.add(
                        Keyword.objects.get_or_create(
                            name=old_identifier, service=instance.responsible_service()
                        )[0]
                    )

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
