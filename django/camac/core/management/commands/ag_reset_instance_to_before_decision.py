from caluma.caluma_workflow.models import Case, WorkItem
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from camac.instance.models import Instance


class Command(BaseCommand):
    help = """
    Reset a completed instance to the state before the decision.

    The command does the following:
    - Sets the "decision" work item (Entscheid / Stellungnahme erstellen) to 'ready'
    - Sets all work items created after the decision work item to 'canceled'
    - Sets the "building-permit" case to 'running'
    - Sets the instance_state to 'decision' (Entscheid ausstehend)
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "instance_id",
            type=int,
            help="The ID of the instance to reset",
        )
        parser.add_argument(
            "--commit",
            action="store_true",
            help="Actually perform the changes (default is dry-run)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        instance_id = options["instance_id"]
        dry_run = not options.get("commit", False)

        if dry_run:
            self.stdout.write(self.style.WARNING("DRY RUN - no changes will be made"))

        try:
            instance = Instance.objects.select_related("case", "instance_state").get(
                pk=instance_id
            )
        except Instance.DoesNotExist:
            raise CommandError(f"Instance with ID {instance_id} does not exist")

        # Check if the instance has a building-permit workflow
        if instance.case.workflow_id != "building-permit":
            raise CommandError(
                f"Instance {instance_id} does not have the 'building-permit' workflow, "
                f"but '{instance.case.workflow_id}'"
            )

        self.stdout.write(
            f"Processing instance {instance_id} "
            f"(current state: {instance.instance_state.name})"
        )

        # Find the decision work item
        try:
            decision_work_item = instance.case.work_items.get(
                task_id="decision",
                status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
            )
        except WorkItem.DoesNotExist:
            raise CommandError(
                f"No completed decision work item found for instance {instance_id}"
            )

        decision_created_at = decision_work_item.created_at
        self.stdout.write(
            f"  Decision work item found (created at: {decision_created_at})"
        )

        # Find all work items created after the decision work item
        # Exclude manual work items and already canceled items
        work_items_to_cancel = (
            instance.case.work_items.filter(
                created_at__gt=decision_created_at,
            )
            .exclude(status=WorkItem.STATUS_CANCELED)
            .exclude(task_id="create-manual-workitems")
        )

        self.stdout.write(
            f"  {work_items_to_cancel.count()} work item(s) will be set to 'canceled':"
        )
        for wi in work_items_to_cancel:
            child_case_info = (
                f" (has child case: {wi.child_case_id})" if wi.child_case_id else ""
            )
            self.stdout.write(
                f"    - {wi.task_id} (status: {wi.status}, created: {wi.created_at}){child_case_info}"
            )

        # Check current case status
        self.stdout.write(f"  Case status: {instance.case.status}")

        if dry_run:
            self.stdout.write(
                self.style.WARNING("\nDRY RUN completed - no changes were made")
            )
            self.stdout.write("Run the command with --commit to apply the changes")
            return

        # Reset the decision work item to ready
        decision_work_item.status = WorkItem.STATUS_READY
        decision_work_item.closed_at = None
        decision_work_item.closed_by_user = None
        decision_work_item.closed_by_group = None
        decision_work_item.save()
        self.stdout.write(self.style.SUCCESS("  Decision work item reset to 'ready'"))

        # Cancel all subsequent work items
        now = timezone.now()
        cancel_count = work_items_to_cancel.count()
        work_items_to_cancel.update(
            status=WorkItem.STATUS_CANCELED,
            closed_at=now,
        )

        self.stdout.write(
            self.style.SUCCESS(f"  {cancel_count} work item(s) set to 'canceled'")
        )

        # Set the case to running
        if instance.case.status != Case.STATUS_RUNNING:
            instance.case.status = Case.STATUS_RUNNING
            instance.case.closed_at = None
            instance.case.save()
            self.stdout.write(self.style.SUCCESS("  Case set to 'running'"))
        else:
            self.stdout.write("  Case is already 'running'")

        # Set the instance_state to decision (Entscheid ausstehend)
        # (the state before decision in the Aargau workflow)
        from camac.instance.models import InstanceState

        decision_state = InstanceState.objects.get(name="decision")
        old_state = instance.instance_state.name
        instance.previous_instance_state = instance.instance_state
        instance.instance_state = decision_state
        instance.save()
        self.stdout.write(
            self.style.SUCCESS(
                f"  Instance state changed from '{old_state}' to 'decision'"
            )
        )

        self.stdout.write(
            self.style.SUCCESS(f"\nInstance {instance_id} successfully reset")
        )
