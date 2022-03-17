from collections import defaultdict

from caluma.caluma_core.events import send_event
from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow.api import cancel_case, cancel_work_item, suspend_case
from caluma.caluma_workflow.events import post_create_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import create_work_items
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, F
from django.db.models.expressions import Q
from django.utils.timezone import now

from camac.caluma.api import CalumaApi
from camac.core.models import Activation, Circulation, DocxDecision
from camac.instance.models import Instance, InstanceState

REQUIRED_CONFIG = {
    "subm": {"tasks": ["ebau-number"]},
    "circulation_init": {
        "tasks": ["skip-circulation", "init-circulation"],
        "condition": lambda case: not case.work_items.filter(
            task_id="circulation", status=WorkItem.STATUS_READY
        ).exists(),
        "ignored_tasks": [
            "nfd",
            "publication",
            "audit",
            "fill-publication",
            "create-publication",
        ],
    },
    "circulation": {
        "tasks": ["start-circulation", "start-decision"],
        "condition": lambda case: not case.work_items.filter(
            task_id="circulation", status=WorkItem.STATUS_READY
        ).exists(),
        "ignored_tasks": [
            "nfd",
            "publication",
            "audit",
            "fill-publication",
            "create-publication",
        ],
    },
    "coordination": {
        "tasks": ["decision", "reopen-circulation"],
        "ignored_tasks": [
            "nfd",
            "publication",
            "audit",
            "fill-publication",
            "create-publication",
        ],
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
        parser.add_argument(
            "--premature-decision", action="store_true", dest="premature_decision"
        )
        parser.add_argument(
            "--duplicated-sb1", action="store_true", dest="duplicated_sb1"
        )

    def get_instance_filters(self, path="pk"):
        return {path: self.instance} if self.instance else {}

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        self.instance = options["instance"]

        self.fix_status_circulation_init_and_circulation()
        self.fix_circulation_leftovers()
        self.fix_circulation_work_items()
        self.fix_closed()
        self.fix_wrongly_closed_cases()
        self.fix_suspended_cases()
        self.fix_circulation_addressed_group()
        if options["sync_circulation"]:
            self.fix_circulation()
        if options["premature_decision"]:
            self.fix_premature_decision()
        if options["duplicated_sb1"]:
            self.fix_duplicated_sb1()
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

    def fix_closed(self):
        count = 0
        for instance in Instance.objects.filter(
            instance_state__name__in=["evaluated", "finished", "finished_internal"],
            pk__in=list(
                Case.objects.filter(
                    work_items__status=WorkItem.STATUS_READY,
                    **self.get_instance_filters("meta__camac-instance-id"),
                ).values_list("meta__camac-instance-id", flat=True)
            ),
            **self.get_instance_filters(),
        ):
            case = instance.case

            count += 1
            if case.status == Case.STATUS_RUNNING:
                cancel_case(case, self.user)
            else:
                for work_item in case.work_items.filter(status=WorkItem.STATUS_READY):
                    cancel_work_item(work_item, self.user)

            self.fixed_instances[instance.pk].append("Closed work items")

        self.stdout.write(
            self.style.WARNING(f"Canceled {count} cases of closed instances")
        )

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
            case = instance.case

            for work_item in case.work_items.filter(
                task_id__in=["init-circulation", "skip-circulation"],
                status=WorkItem.STATUS_READY,
            ):
                cancel_work_item(work_item, self.user)

            for circulation in instance.circulations.all():
                if not case.work_items.filter(
                    **{"meta__circulation-id": circulation.pk}
                ).exists():
                    created_work_items = create_work_items(
                        tasks=Task.objects.filter(pk="circulation"),
                        case=instance.case,
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

        circulation_work_items.delete()
        activation_work_items.delete()

        self.stdout.write(
            self.style.WARNING(f"Deleted {count} circulation and activation work items")
        )

    def fix_required_tasks(self):
        for instance in Instance.objects.filter(
            instance_state__name__in=REQUIRED_CONFIG.keys(),
            **self.get_instance_filters(),
        ).order_by("instance_state__name"):
            case = instance.case

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

                created_work_items = create_work_items(
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

    def fix_wrongly_closed_cases(self):
        count = 0

        for instance in Instance.objects.exclude(
            instance_state__name__in=[
                "evaluated",
                "finished",
                "finished_internal",
                "archived",
            ],
        ).filter(
            pk__in=list(
                Case.objects.filter(
                    status__in=[Case.STATUS_CANCELED, Case.STATUS_COMPLETED],
                    work_items__status=WorkItem.STATUS_READY,
                ).values_list("meta__camac-instance-id", flat=True)
            ),
            **self.get_instance_filters(),
        ):
            case = instance.case

            count += 1

            case.status = Case.STATUS_RUNNING
            case.closed_at = None
            case.closed_by_group = None
            case.closed_by_user = None
            case.save()

            self.fixed_instances[instance.pk].append("Wrongly closed case")

        self.stdout.write(self.style.WARNING(f"Reopened {count} wrongly closed cases"))

    def fix_suspended_cases(self):
        count = 0

        for case in Case.objects.exclude(status=Case.STATUS_SUSPENDED).filter(
            **{
                "meta__camac-instance-id__in": list(
                    Instance.objects.filter(
                        instance_state__name__in=["correction", "rejected"],
                        **self.get_instance_filters(),
                    ).values_list("pk", flat=True)
                )
            }
        ):
            suspend_case(case, self.user)
            count += 1
            self.fixed_instances[case.meta.get("camac-instance-id")].append(
                "Case not suspended"
            )

        self.stdout.write(
            self.style.WARNING(f"Suspended {count} rejected or in correction cases")
        )

    def fix_circulation_addressed_group(self):
        unassigned_circulation_work_items = WorkItem.objects.filter(
            addressed_groups=[],
            task_id="circulation",
            **self.get_instance_filters("case__family__meta__camac-instance-id"),
        )

        for work_item in unassigned_circulation_work_items:
            circulation = Circulation.objects.get(
                pk=work_item.meta.get("circulation-id")
            )

            work_item.addressed_groups = [circulation.service_id]
            work_item.save()

            self.fixed_instances[
                work_item.case.family.meta.get("camac-instance-id")
            ].append("Circulation not assigned")

        self.stdout.write(
            self.style.WARNING(
                f"Assigned {unassigned_circulation_work_items.count()} circulation work items"
            )
        )

    def fix_premature_decision(self):
        """Fix instances where the decision WI was created prematurely.

        Fix decided cases where instances don't have a DocxDecision.
        See EBAUBEOPS-141
        """

        completed = set(
            WorkItem.objects.filter(task_id="decision", status="completed").values_list(
                "case__meta__camac-instance-id", flat=True
            )
        )

        decided = set(
            DocxDecision.objects.filter(instance__pk__in=completed).values_list(
                "instance__pk", flat=True
            )
        )

        broken = completed - decided

        if not broken:
            self.stdout.write(self.style.NOTICE("No prematurely decided cases found."))
            return

        work_items = WorkItem.objects.filter(
            task_id__in=["create-publication", "create-manual-workitems", "decision"],
            **{"case__meta__camac-instance-id__in": broken},
        )
        work_items.update(
            status=WorkItem.STATUS_READY,
            closed_at=None,
            closed_by_user=None,
            closed_by_group=None,
        )

        instances = Instance.objects.filter(pk__in=broken)
        instances.update(instance_state=F("previous_instance_state"))

        cases = Case.objects.filter(**{"meta__camac-instance-id__in": broken})
        cases.update(
            status=Case.STATUS_RUNNING,
            closed_at=None,
            closed_by_user=None,
            closed_by_group=None,
        )

        for pk in broken:
            self.fixed_instances[pk].append("Premature decision")

        self.stdout.write(
            self.style.WARNING(f"Reopened {len(broken)} prematurely decided cases.")
        )

    def fix_duplicated_sb1(self):
        """Fix instances where sb1 is duplicated.

        Remove canceled version, if there is another one in "ready" status.
        See EBAUBEOPS-149, but there are more cases.
        """

        cases = (
            Case.objects.prefetch_related("work_items")
            .annotate(
                sb1_count=Count("work_items__pk", filter=Q(work_items__task_id="sb1"))
            )
            .filter(sb1_count__gte=2)
        )

        broken = []
        for case in cases:
            if not case.work_items.filter(task_id="sb1", status="ready").exists():
                continue

            pk = case.meta["camac-instance-id"]
            broken.append(pk)
            self.fixed_instances[pk].append("Duplicated sb1")
            case.work_items.filter(task_id="sb1").exclude(status="ready").delete()

        self.stdout.write(
            self.style.WARNING(f"Fixed {len(broken)} duplicated sb1 work items.")
        )
