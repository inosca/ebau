from datetime import timedelta

from caluma.caluma_user.models import AnonymousUser
from caluma.caluma_workflow import api as caluma_workflow_api
from caluma.caluma_workflow.events import post_complete_work_item, post_skip_work_item
from caluma.caluma_workflow.models import Case, Task, WorkItem
from caluma.caluma_workflow.utils import get_jexl_groups
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count
from django.utils import timezone

from camac.caluma.api import CalumaApi
from camac.caluma.extensions.events.circulation import (
    post_complete_circulation_work_item,
)
from camac.core.models import Circulation
from camac.instance.models import Instance, InstanceResponsibility


class Command(BaseCommand):
    help = "Repair the eBau Schwyz workflow"

    def add_arguments(self, parser):
        parser.add_argument(
            "--verbose",
            dest="verbose",
            action="store_true",
            default=False,
        )

        parser.add_argument("--no-dry", dest="dry", action="store_false", default=True)

    @transaction.atomic
    def handle(self, *args, **options):
        self.verbose = options["verbose"]

        tid = transaction.savepoint()

        post_complete_work_item.disconnect(post_complete_circulation_work_item)
        post_skip_work_item.disconnect(post_complete_circulation_work_item)

        # Circulation repair block
        self.stdout.write("Start repairing circulations")
        for instance in Instance.objects.filter(instance_state__name="circ"):
            case = Case.objects.get(**{"meta__camac-instance-id": instance.pk})
            circ_work_items = WorkItem.objects.filter(
                task_id="circulation",
                case=case,
                status=WorkItem.STATUS_READY,
            )
            additional_circ_work_items = WorkItem.objects.filter(
                task_id="start-additional-circulation",
                case=case,
                status=WorkItem.STATUS_READY,
            )

            if len(circ_work_items) > 0 or len(additional_circ_work_items) == 1:
                continue

            if len(additional_circ_work_items) > 1:
                self.stdout.write(
                    f"Not possible, check manually (instance: {instance.pk}, case: {case.pk})"
                )
                continue

            if self.verbose:
                self.stdout.write(
                    f"No active circ workItem found in instance {instance.pk} (case {case.pk}), repairing"
                )

            self.repair_circulation(instance, case)

        # Skip circ workItems which have no open camac circulation
        self.skip_unfinished_circs()

        # Manual workItem and depreciate workItem repair block
        self.stdout.write("Start repairing manual and depreciate workItems")
        for instance_rmwi in Instance.objects.exclude(
            instance_state__name__in=["new", "arch"]
        ):  # _rmwi stands for "repair manual workItem"
            self.repair_missing_work_items(instance_rmwi)

        # Detect possible issues
        self.detect_duplicates()

        # Cleanup after repair is done
        post_complete_work_item.connect(post_complete_circulation_work_item)
        post_skip_work_item.connect(post_complete_circulation_work_item)

        if options["dry"]:
            self.stdout.write(
                "This was a dry run, if changes should be written use --no-dry"
            )
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)

    def repair_circulation(self, instance, case):
        anonymous_user = AnonymousUser()
        # create all circulation work items first
        for circulation in instance.circulations.all():
            self.create_work_item_from_task(
                case,
                "circulation",
                meta={"circulation-id": circulation.pk},
                instance=instance,
                context={"circulation-id": circulation.pk},
                additional_filters={"meta__circulation-id": circulation.pk},
            )

        # sync them later when all work items are created to avoid creating a
        # broken workflow state
        for circulation in instance.circulations.all():
            CalumaApi().sync_circulation(circulation, anonymous_user)

            for activation in circulation.activations.filter(
                circulation_state__name="REVIEW"
            ):
                work_item = WorkItem.objects.filter(
                    **{
                        "meta__activation-id": activation.pk,
                        "task_id": "write-statement",
                    }
                ).first()

                if not work_item.status == WorkItem.STATUS_READY:
                    # Check statement work item was already skipped - continue
                    continue

                caluma_workflow_api.skip_work_item(
                    work_item,
                    anonymous_user,
                    {"circulation-id": circulation.pk, "activation-id": activation.pk},
                )

                if self.verbose:
                    self.stdout.write(
                        f"Skipped work item 'check-statement' for activation {activation.pk} that's already in review"
                    )

    def repair_missing_work_items(self, instance):
        case = Case.objects.get(**{"meta__camac-instance-id": instance.pk})
        manual_work_item = WorkItem.objects.filter(
            task_id="create-manual-workitems",
            case=case,
            status=WorkItem.STATUS_READY,
        ).first()

        if not manual_work_item:
            if self.verbose:
                self.stdout.write(
                    f"No workItem 'create-manual-workitems' found in instance {instance.pk}, creating"
                )

            self.create_work_item_from_task(
                case,
                "create-manual-workitems",
                additional_filters={"status": WorkItem.STATUS_READY},
            )

        depreciate_work_item = WorkItem.objects.filter(
            task_id="depreciate-case", case=case, status=WorkItem.STATUS_READY
        ).first()
        if not depreciate_work_item:
            if self.verbose:
                self.stdout.write(
                    f"No workItem 'depreciate-case' found in instance {instance.pk}, creating"
                )

            self.create_work_item_from_task(
                case,
                "depreciate-case",
                additional_filters={"status": WorkItem.STATUS_READY},
            )

    def create_work_item_from_task(
        self,
        case,
        task_slug,
        meta={},
        child_case=None,
        context={},
        deadline=None,
        instance=None,
        applicant=False,
        additional_filters={},
    ):
        task = Task.objects.get(pk=task_slug)
        anonymous_user = AnonymousUser()

        if WorkItem.objects.filter(case=case, task=task, **additional_filters).exists():
            if self.verbose:
                self.stdout.write(
                    f"{task_slug} work item on case {case.pk} exists skipping"
                )
            return

        meta = {
            "migrated": True,
            "not-viewed": True,
            "notify-deadline": True,
            "notify-completed": False,
            **meta,
        }

        if not deadline and task.lead_time:
            deadline = timezone.now() + timedelta(seconds=task.lead_time)

        addressed_groups = get_jexl_groups(
            task.address_groups, task, case, anonymous_user, None, context
        )

        responsible_user = []
        if instance:
            responsibility = InstanceResponsibility.objects.filter(
                instance=instance, service__pk=addressed_groups[0]
            ).first()
            if responsibility:
                responsible_user = [responsibility.user.username]

        if applicant:
            addressed_groups.append("applicant")

        work_item = WorkItem.objects.create(
            case=case,
            task=task,
            meta=meta,
            name=task.name,
            status=WorkItem.STATUS_READY,
            child_case=child_case,
            deadline=deadline,
            addressed_groups=addressed_groups,
            controlling_groups=get_jexl_groups(
                task.control_groups, task, case, anonymous_user, None, context
            ),
            assigned_users=responsible_user,
        )

        if self.verbose:
            self.stdout.write(f"Created work item {work_item.pk} {work_item.name}")

        return work_item

    def detect_duplicates(self):
        dups = (
            WorkItem.objects.values("meta__circulation-id")
            .annotate(circ_item_count=Count("meta__circulation-id"))
            .filter(circ_item_count__gt=1)
        )

        self.stdout.write("Possible problems detected")
        for dup in dups:
            if dup["meta__circulation-id"] is not None:
                self.stdout.write(f"Multiple circulation work items: {dup}")

    def skip_unfinished_circs(self):
        anonymous_user = AnonymousUser()
        active_circ_wis = WorkItem.objects.filter(task="circulation", status="ready")
        for circ_wi in active_circ_wis:
            circ = Circulation.objects.get(
                circulation_id=circ_wi.meta["circulation-id"]
            )
            if (
                circ.activations.count() > 0
                and circ.activations.exclude(circulation_state__name="DONE").count()
                == 0
            ):
                self.stdout.write(
                    f"Active circ workItem ({circ_wi}) without active camac circ ({circ.pk}): skip"
                )
                caluma_workflow_api.skip_work_item(
                    circ_wi,
                    anonymous_user,
                    {"circulation-id": circ.pk},
                )
