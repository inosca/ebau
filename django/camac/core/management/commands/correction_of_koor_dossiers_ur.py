from caluma.caluma_workflow.models import WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from camac.instance.models import Instance
from camac.user.models import Service

DOSSIER_LIST = [
    {"dossier_nr": "1203-24-028", "new_service": "1"},
    {"dossier_nr": "1203-24-026", "new_service": "1"},
    {"dossier_nr": "1205-24-012", "new_service": "350"},
    {"dossier_nr": "1222-20-013", "new_service": "302"},
    {"dossier_nr": "1222-20-009", "new_service": "302"},
    {"dossier_nr": "1222-21-012", "new_service": "302"},
    {"dossier_nr": "1206-20-138", "new_service": "1"},
    {"dossier_nr": "1222-21-020", "new_service": "524"},
    {"dossier_nr": "1222-21-022", "new_service": "524"},
    {"dossier_nr": "1222-21-019", "new_service": "302"},
    {"dossier_nr": "1222-22-013", "new_service": "302"},
    {"dossier_nr": "1222-22-021", "new_service": "302"},
    {"dossier_nr": "1222-22-022", "new_service": "302"},
    {"dossier_nr": "1222-21-005", "new_service": "302"},
    {"dossier_nr": "1222-21-004", "new_service": "524"},
    {"dossier_nr": "1222-21-001", "new_service": "302"},
    {"dossier_nr": "1222-22-025", "new_service": "302"},
    {"dossier_nr": "1222-22-026", "new_service": "524"},
    {"dossier_nr": "1222-21-003", "new_service": "302"},
    {"dossier_nr": "1221-21-007", "new_service": "302"},
    {"dossier_nr": "1222-21-013", "new_service": "524"},
    {"dossier_nr": "1222-21-014", "new_service": "524"},
    {"dossier_nr": "1221-23-001", "new_service": "302"},
    {"dossier_nr": "1222-21-015", "new_service": "302"},
    {"dossier_nr": "1222-21-017", "new_service": "524"},
    {"dossier_nr": "1222-21-021", "new_service": "302"},
    {"dossier_nr": "1222-22-002", "new_service": "524"},
    {"dossier_nr": "1222-22-001", "new_service": "524"},
    {"dossier_nr": "1222-22-007", "new_service": "302"},
    {"dossier_nr": "1222-22-004", "new_service": "302"},
    {"dossier_nr": "1221-23-003", "new_service": "302"},
    {"dossier_nr": "1222-21-002", "new_service": "302"},
    {"dossier_nr": "1222-22-016", "new_service": "302"},
    {"dossier_nr": "1222-22-017", "new_service": "524"},
    {"dossier_nr": "1222-22-024", "new_service": "302"},
    {"dossier_nr": "1221-23-010", "new_service": "302"},
    {"dossier_nr": "1221-23-007", "new_service": "302"},
    {"dossier_nr": "1221-23-013", "new_service": "302"},
    {"dossier_nr": "1221-23-012", "new_service": "302"},
    {"dossier_nr": "1222-23-001", "new_service": "524"},
    {"dossier_nr": "1221-23-014", "new_service": "302"},
    {"dossier_nr": "1221-20-020", "new_service": "302"},
    {"dossier_nr": "1222-20-002", "new_service": "524"},
    {"dossier_nr": "1221-23-015", "new_service": "302"},
    {"dossier_nr": "1222-23-002", "new_service": "302"},
    {"dossier_nr": "1222-19-004", "new_service": "302"},
    {"dossier_nr": "1222-19-003", "new_service": "302"},
    {"dossier_nr": "1222-23-003", "new_service": "302"},
    {"dossier_nr": "1222-23-004", "new_service": "302"},
    {"dossier_nr": "1222-19-008", "new_service": "302"},
    {"dossier_nr": "1222-20-004", "new_service": "302"},
    {"dossier_nr": "1221-19-006", "new_service": "524"},
    {"dossier_nr": "1222-18-006", "new_service": "302"},
    {"dossier_nr": "1222-18-004", "new_service": "302"},
    {"dossier_nr": "1222-19-001", "new_service": "302"},
    {"dossier_nr": "1222-18-001", "new_service": "302"},
    {"dossier_nr": "1222-18-005", "new_service": "302"},
    {"dossier_nr": "1222-18-003", "new_service": "302"},
    {"dossier_nr": "1222-19-013", "new_service": "302"},
    {"dossier_nr": "1221-23-016", "new_service": "302"},
    {"dossier_nr": "1222-20-006", "new_service": "302"},
    {"dossier_nr": "1222-19-012", "new_service": "302"},
    {"dossier_nr": "1222-19-014", "new_service": "302"},
    {"dossier_nr": "1222-20-008", "new_service": "302"},
    {"dossier_nr": "1221-24-004", "new_service": "302"},
    {"dossier_nr": "1221-23-017", "new_service": "302"},
    {"dossier_nr": "1221-23-018", "new_service": "302"},
    {"dossier_nr": "1221-23-019", "new_service": "302"},
    {"dossier_nr": "1221-23-020", "new_service": "302"},
    {"dossier_nr": "1221-24-014", "new_service": "302"},
    {"dossier_nr": "1221-24-015", "new_service": "302"},
    {"dossier_nr": "1213-24-098", "new_service": "302"},
    {"dossier_nr": "1221-24-016", "new_service": "302"},
    {"dossier_nr": "1221-23-021", "new_service": "302"},
    {"dossier_nr": "1221-24-010", "new_service": "302"},
    {"dossier_nr": "1221-24-011", "new_service": "302"},
    {"dossier_nr": "1221-24-002", "new_service": "302"},
    {"dossier_nr": "1221-24-003", "new_service": "302"},
]


class Command(BaseCommand):
    help = "Fix the assignement of KOOR dossiers according to a list of the customer"

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            dest="dry",
            action="store_true",
            default=False,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        # Change the instance_service
        for dossier in DOSSIER_LIST:
            instance = Instance.objects.get(
                **{"case__meta__dossier-number": dossier["dossier_nr"]}
            )
            old_service = instance.responsible_service()
            new_service = Service.objects.get(pk=dossier["new_service"])
            instance.instance_services.update(service=new_service)
            self.stdout.write(
                f'{dossier["dossier_nr"]}: old service: {old_service.pk}, new service: {new_service.pk}'
            )

            # Add service to addressed_groups and controlling_groups
            work_items = WorkItem.objects.filter(
                Q(case=instance.case) | Q(case__family=instance.case)
            ).exclude(status__in=["completed", "canceled"])

            for work_item in work_items:
                if str(old_service.pk) in work_item.addressed_groups:
                    work_item.addressed_groups = list(
                        map(
                            lambda x: str(new_service.pk)
                            if x == str(old_service.pk)
                            else x,
                            work_item.addressed_groups,
                        )
                    )

                if str(old_service.pk) in work_item.controlling_groups:
                    work_item.controlling_groups = list(
                        map(
                            lambda x: str(new_service.pk)
                            if x == str(old_service.pk)
                            else x,
                            work_item.controlling_groups,
                        )
                    )

                work_item.save()
                self.stdout.write(
                    f'{work_item.id}: new addressed groups: {new_service.pk}", new controlling groups: {new_service.pk}'
                )

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
