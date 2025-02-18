import datetime

from caluma.caluma_workflow.models import Task, WorkItem
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef

from camac.instance.models import Instance, InstanceState
from camac.responsible.models import ResponsibleService


class Command(BaseCommand):
    help = "Reopen/recreate archive-instance work items on instances in completed state"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.task_complete_instance = Task.objects.get(pk="complete-instance")
        self.task_archive_instance = Task.objects.get(pk="archive-instance")
        self.instance_state_instance_completed = InstanceState.objects.get(
            name="instance-completed",
        )
        self.responsible_services = {}

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Create work items for real",
        )

    def handle(self, *args, **options):
        # Get instances that are currently in 'instance-completed' state but do
        # not have an 'archive-instance' work item in ready state:
        instances = Instance.objects.filter(
            ~Exists(
                WorkItem.objects.filter(
                    task=self.task_archive_instance,
                    status=WorkItem.STATUS_READY,
                    case_id=OuterRef("case__pk"),
                ),
            ),
            instance_state=self.instance_state_instance_completed,
        )

        # For each of those instances, ensure we end up with a ready
        # 'archive-instance' work item:
        for instance in instances:
            # We want the previous work item to be 'complete-instance', so first
            # get that one:
            work_items_complete_instance = instance.case.work_items.filter(
                task=self.task_complete_instance,
                status=WorkItem.STATUS_COMPLETED,
            )
            if work_items_complete_instance.count() != 1:
                raise Exception(
                    f"Instance {instance.identifier} has {work_items_complete_instance.count()} complete-instance work items"
                )
            work_item_complete_instance = work_items_complete_instance.first()

            # Next, get the 'archive-instance' work items with the previous work
            # item being 'complete-instance':
            work_items_archive_instance = instance.case.work_items.filter(
                task=self.task_archive_instance,
                previous_work_item__task=self.task_complete_instance,
            )

            if not work_items_archive_instance:
                # There is no such work item; create a new one:
                self.create_missing_work_item(
                    instance, work_item_complete_instance, options["commit"]
                )
            elif work_items_archive_instance.count() == 1:
                # There is one such work item; reopen it:
                self.reopen_work_item(
                    instance, work_items_archive_instance.first(), options["commit"]
                )
            else:
                # There is more than one such work item, which is weird; we should have
                # a look at it:
                raise Exception(
                    f"Instance {instance.identifier} has {work_items_archive_instance.count()} archive-instance work items with complete-instance as previous work item"
                )

    def reopen_work_item(self, instance, work_item, commit):
        print(
            f"{instance.identifier}: Setting {work_item.task_id} to {WorkItem.STATUS_READY}"
        )
        if commit:
            work_item.status = WorkItem.STATUS_READY
            work_item.meta.update(self.get_migration_meta())
            work_item.save()

    def create_missing_work_item(self, instance, previous_work_item, commit):
        responsible_service = str(instance.responsible_service().pk)
        responsible_users = self.get_responsible_users(instance, responsible_service)

        print(
            f"{instance.identifier}: Creating new archive-instance work item with responsible service {responsible_service} and responsible users {responsible_users}"
        )
        if commit:
            wi = WorkItem.objects.create(
                task=self.task_archive_instance,
                name=self.task_archive_instance.name,
                addressed_groups=[responsible_service],
                assigned_users=responsible_users,
                case=instance.case,
                status=WorkItem.STATUS_READY,
                closed_at=None,
                previous_work_item=previous_work_item,
                meta={
                    "not-viewed": True,
                    "notify-completed": False,
                    "notify-deadline": False,
                    **(self.get_migration_meta()),
                },
                deadline=None,
            )
            wi.created_at = previous_work_item.closed_at
            wi.save()

    def get_migration_meta(self):
        return {
            "migration-date-utc": datetime.datetime.now(
                tz=datetime.timezone.utc,
            ).isoformat(),
            "migration-mr": "!9374",
        }

    def get_responsible_users(self, instance, service_id):
        users = self.responsible_services.get((instance.pk, service_id))

        if not users:
            users = list(
                ResponsibleService.objects.filter(
                    instance=instance, service_id=service_id
                ).values_list("responsible_user__username", flat=True)
            )
            self.responsible_services[(instance.pk, service_id)] = users

        return users
