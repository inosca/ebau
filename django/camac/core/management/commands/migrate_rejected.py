from datetime import datetime

import pytz
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import create_work_items
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models.expressions import RawSQL

from camac.core.models import Publication
from camac.instance.models import Instance, InstanceState


class MigrationUser(BaseUser):
    def __str__(self):
        return "migration-user"


DATE_OF_MIGRATION = datetime(2020, 9, 22, 19, 0, 0, tzinfo=pytz.UTC)


class Command(BaseCommand):
    help = """Correct rejected instances."""

    def __init__(self, *args, **kwargs):
        self.user = MigrationUser()
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry",
            default=False,
            action="store_true",
            help="Don't apply changes",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.created = []

        # should not be possible, fix
        Instance.objects.filter(
            instance_state__name="rejected",
            previous_instance_state__name="coordination",
        ).update(
            previous_instance_state=InstanceState.objects.get(name="circulation_init")
        )

        instances = Instance.objects.filter(
            instance_state__name="rejected",
            previous_instance_state__name="circulation_init",
        )
        cases = Case.objects.filter(
            status="suspended",
            modified_at__lt=DATE_OF_MIGRATION,
            **{
                "meta__migrated": True,
                "meta__camac-instance-id__in": list(
                    instances.values_list("pk", flat=True)
                ),
            },
        )

        for instance in instances:
            case = cases.filter(**{"meta__camac-instance-id": instance.pk}).first()

            if not case:
                continue

            self.migrate_instance(instance, case)

        self.mark_created_as_migrated()
        self.suspend_ebau_number()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def mark_created_as_migrated(self):
        WorkItem.objects.filter(pk__in=self.created).update(
            meta=RawSQL("""jsonb_set(meta, '{"migrated"}', 'true', true)""", [])
        )

    def suspend_ebau_number(self):
        instance_ids = list(
            Instance.objects.filter(
                instance_state__name="rejected", previous_instance_state__name="subm"
            ).values_list("pk", flat=True)
        )

        fixable = WorkItem.objects.filter(
            **{
                "case__meta__camac-instance-id__in": instance_ids,
                "task_id": "ebau-number",
            }
        ).exclude(status=WorkItem.STATUS_SUSPENDED)

        self.stdout.write(f"Fixed status of {fixable.count()} ebau-number work items")

        fixable.update(
            status=WorkItem.STATUS_SUSPENDED,
            closed_at=None,
            closed_by_user=None,
            closed_by_group=None,
        )

    def migrate_instance(self, instance, case):
        initial_workitems = set(
            list(case.work_items.all().values_list("task", flat=True))
        )

        # pretend the case is still in previous state
        case.status = Case.STATUS_RUNNING
        case.save()
        instance_state = instance.previous_instance_state

        to_create = ["create-manual-workitems"]

        if (
            instance_state.name
            in [
                "circulation_init",
                "circulation",
            ]
            and not Publication.objects.filter(instance=instance.pk).exists()
        ):
            to_create.append("publication")

        if instance_state.name == "circulation_init":
            to_create += ["audit", "init-circulation", "skip-circulation"]

        self.create_work_items_from_tasks(
            case, [slug for slug in to_create if slug not in initial_workitems]
        )

        workflow_api.suspend_case(case, self.user)

        final_workitems = set(
            list(case.work_items.all().values_list("task", flat=True))
        )

        out = f"Importing {instance.pk:5} with previous state {instance_state.name} resulted in"
        if initial_workitems == final_workitems:
            wis = ", ".join(
                [
                    f"{x[0]} ({x[1]})"
                    for x in case.work_items.values_list("task_id", "status")
                ]
            )
            self.stdout.write(f"{out} same workitems: {wis}")

        else:
            added = ", ".join(final_workitems - initial_workitems)

            self.stdout.write(f"{out} added workitems: {added}")

    def create_work_items_from_tasks(self, case, task_slugs, context={}):
        if not task_slugs:
            return

        work_items = create_work_items(
            Task.objects.filter(pk__in=task_slugs), case, self.user, context=context
        )

        self.created += [wi.pk for wi in work_items]
