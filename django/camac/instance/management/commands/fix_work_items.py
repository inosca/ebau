from collections import defaultdict

from caluma.caluma_core.events import send_event
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.api import cancel_work_item
from caluma.caluma_workflow.events import post_create_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import bulk_create_work_items
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.utils.timezone import now

from camac.caluma.api import CalumaApi
from camac.core.models import Activation, Circulation
from camac.instance.models import Instance, InstanceState

REQUIRED_CONFIG = {
    "circulation_init": {
        "tasks": ["skip-circulation", "init-circulation"],
        "condition": lambda case: not case.work_items.filter(
            task_id="circulation", status=WorkItem.STATUS_READY
        ).exists(),
        "ignored_tasks": ["nfd", "publication", "audit"],
    },
    "circulation": {
        "tasks": ["start-circulation", "start-decision"],
        "condition": lambda case: not case.work_items.filter(
            task_id="circulation", status=WorkItem.STATUS_READY
        ).exists(),
        "ignored_tasks": ["nfd", "publication", "audit"],
    },
    "coordination": {
        "tasks": ["decision", "reopen-circulation"],
        "ignored_tasks": ["nfd", "publication", "audit"],
    },
    "sb1": {"tasks": ["sb1"]},
    "sb2": {"tasks": ["sb2"]},
    "conclusion": {
        "tasks": ["complete"],
    },
}


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.user = AnonymousUser(username="admin")
        self.fixed_instances = defaultdict(list)

    def add_arguments(self, parser):
        parser.add_argument("--dry", action="store_true", dest="dry")
        parser.add_argument("--instance", default=None, type=int)
        parser.add_argument(
            "--sync-circulation", action="store_true", dest="sync_circulation"
        )

    def get_instance_filters(self, path="pk"):
        return {path: self.instance} if self.instance else {}

    def get_case(self, instance):
        try:
            return Case.objects.get(**{"meta__camac-instance-id": instance.pk})
        except Case.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f"No case for instance {instance.pk} found")
            )

        return None

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        self.instance = options["instance"]

        self.fix_status_circulation_init_and_circulation()
        self.fix_circulation_leftovers()
        self.fix_circulation_work_items()
        if options["sync_circulation"]:
            self.fix_circulation()
        self.fix_required_tasks()

        if len(self.fixed_instances.keys()):
            self.stdout.write("")
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed {len(self.fixed_instances.keys())} instances:"
                )
            )
            for instance_id, reasons in sorted(self.fixed_instances.items()):
                instance = Instance.objects.get(pk=instance_id)
                municipality = instance.responsible_service(filter_type="municipality")

                self.stdout.write(
                    "- "
                    + self.style.SUCCESS(str(instance.pk))
                    + f", {instance.instance_state.get_name()}, {municipality.get_name()}, "
                    + self.style.ERROR(", ".join(reasons))
                )

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)

    def fix_status_circulation_init_and_circulation(self):
        status_count = 0
        work_item_count = 0

        instances_with_circulation = Instance.objects.annotate(
            circulation_count=Count("circulations__pk")
        ).filter(
            instance_state__name__in=["circulation", "circulation_init"],
            circulation_count__gt=0,
            **self.get_instance_filters(),
        )

        for instance in instances_with_circulation.filter(
            instance_state__name="circulation_init",
            circulations__activations__email_sent=1,
        ):
            instance.previous_instance_state = InstanceState.objects.get(
                name="circulation_init"
            )
            instance.instance_state = InstanceState.objects.get(name="circulation")
            instance.save()

            status_count += 1

            self.fixed_instances[instance.pk].append("Wrong instance state")

        self.stdout.write(
            self.style.WARNING(f"Fixed {status_count} wrong instances states")
        )

        for instance in instances_with_circulation.exclude(
            circulations__pk__in=list(
                WorkItem.objects.filter(
                    task_id="circulation",
                    **self.get_instance_filters("case__meta__camac-instance-id"),
                ).values_list("meta__circulation-id", flat=True)
            ),
        ).filter(circulations__activations__circulation_state__name="RUN"):
            work_item_count += 1
            case = self.get_case(instance)

            for work_item in case.work_items.filter(
                task_id__in=["init-circulation", "skip-circulation"],
                status=WorkItem.STATUS_READY,
            ):
                cancel_work_item(work_item, self.user)

            for circulation in instance.circulations.all():
                if not case.work_items.filter(
                    **{"meta__circulation-id": circulation.pk}
                ).exists():
                    created_work_items = bulk_create_work_items(
                        tasks=Task.objects.filter(pk="circulation"),
                        case=self.get_case(instance),
                        user=self.user,
                        context={"circulation-id": circulation.pk},
                    )

                    for created_work_item in created_work_items:
                        send_event(
                            post_create_work_item,
                            sender=self,
                            work_item=created_work_item,
                            user=self.user,
                            context={"circulation-id": circulation.pk},
                        )

            self.fixed_instances[instance.pk].append(
                "Missing work item for circulation"
            )

        self.stdout.write(
            self.style.WARNING(
                f"Fixed {work_item_count} missing circulation work items"
            )
        )

    def fix_circulation(self):
        count = 0
        api = CalumaApi()

        for circulation in Circulation.objects.filter(
            instance__instance_state__name="circulation",
            pk__in=list(
                WorkItem.objects.filter(
                    task_id="circulation",
                    status=WorkItem.STATUS_READY,
                    **self.get_instance_filters("case__meta__camac-instance-id"),
                ).values_list("meta__circulation-id", flat=True)
            ),
            **self.get_instance_filters("instance_id"),
        ):
            api.sync_circulation(circulation, self.user)
            count += 1

        self.stdout.write(self.style.WARNING(f"Synced {count} circulations"))

    def fix_circulation_work_items(self):
        work_items = WorkItem.objects.exclude(
            case__parent_work_item__status=WorkItem.STATUS_READY
        ).filter(
            task_id="activation",
            status=WorkItem.STATUS_READY,
            **self.get_instance_filters("case__meta__camac-instance-id"),
        )
        count = work_items.count()

        work_items.update(status=WorkItem.STATUS_CANCELED, closed_at=now())

        self.stdout.write(
            self.style.WARNING(
                f"Canceled {count} activation work items of finished circulations"
            )
        )

    def fix_circulation_leftovers(self):
        circulation_work_items = WorkItem.objects.filter(
            task_id="circulation",
            **self.get_instance_filters("case__meta__camac-instance-id"),
        ).exclude(
            **{
                "meta__circulation-id__in": list(
                    Circulation.objects.filter(
                        **self.get_instance_filters("instance_id")
                    ).values_list("pk", flat=True)
                )
            }
        )
        activation_work_items = WorkItem.objects.filter(
            task_id="activation",
            **self.get_instance_filters("case__meta__camac-instance-id"),
        ).exclude(
            **{
                "meta__activation-id__in": list(
                    Activation.objects.filter(
                        **self.get_instance_filters("circulation__instance_id")
                    ).values_list("pk", flat=True)
                )
            }
        )
        count = circulation_work_items.count() + activation_work_items.count()

        circulation_work_items.union(activation_work_items).delete()

        self.stdout.write(
            self.style.WARNING(f"Deleted {count} circulation and activation work items")
        )

    def fix_required_tasks(self):
        for instance in Instance.objects.filter(
            instance_state__name__in=REQUIRED_CONFIG.keys(),
            **self.get_instance_filters(),
        ).order_by("instance_state__name"):
            case = self.get_case(instance)
            if not case:
                continue

            config = REQUIRED_CONFIG[instance.instance_state.name]

            condition = config.get("condition", lambda case: True)
            required_tasks = config["tasks"]
            ignored_tasks = config.get("ignored_tasks", [])

            if not condition(case):
                continue

            canceled = []
            created = []

            for required_task in required_tasks:
                if case.work_items.filter(
                    status=WorkItem.STATUS_READY, task_id=required_task
                ).exists():
                    continue

                cancel_work_items = case.work_items.filter(
                    status=WorkItem.STATUS_READY
                ).exclude(
                    task_id__in=["create-manual-workitems"]
                    + required_tasks
                    + ignored_tasks
                )

                for work_item in cancel_work_items:
                    canceled.append(work_item.task_id)
                    cancel_work_item(work_item=work_item, user=self.user)

                created_work_items = bulk_create_work_items(
                    Task.objects.filter(pk=required_task), case, self.user
                )
                created.append(required_task)

                for created_work_item in created_work_items:
                    send_event(
                        post_create_work_item,
                        sender=self,
                        work_item=created_work_item,
                        user=self.user,
                        context={},
                    )

            if len(created):
                self.fixed_instances[instance.pk].append("Missing work items")
                self.stdout.write(
                    self.style.WARNING(
                        f"{instance.pk} ({instance.instance_state.get_name()}):"
                    )
                )
                created_slugs = ", ".join(map(lambda s: f"'{s}'", created))
                self.stdout.write(self.style.SUCCESS(f"\tCreated: {created_slugs}"))

                if len(canceled):
                    canceled_slugs = ", ".join(map(lambda s: f"'{s}'", canceled))
                    self.stdout.write(self.style.ERROR(f"\tCanceled: {canceled_slugs}"))
