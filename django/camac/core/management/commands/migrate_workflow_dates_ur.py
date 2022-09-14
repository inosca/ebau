from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import WorkflowEntry, WorkflowItem

WORKFLOW_ITEM_EINGANG_ONLINE = 12000000
WORKFLOW_ITEM_DOSSIER_ERFASST = 12


class Command(BaseCommand):
    help = """Migrate the workflow-items of workflow-entries"""

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

        dossier_erfasst_workflow_entries = WorkflowEntry.objects.filter(
            workflow_item=WORKFLOW_ITEM_DOSSIER_ERFASST,
        )

        for workflow_entry in dossier_erfasst_workflow_entries:
            case = workflow_entry.instance.case
            _, created = case.document.answers.get_or_create(
                question_id="is-paper", defaults={"value": "is-paper-yes"}
            )

            if created:
                self.stdout.write(f"{case.instance.pk}: new 'is-paper' answer created")
            else:
                self.stdout.write(f"{case.instance.pk}: 'is-paper' answer updated")

        eingang_online_workflow_entries = WorkflowEntry.objects.filter(
            workflow_item=WORKFLOW_ITEM_EINGANG_ONLINE
        )
        for workflow_entry in eingang_online_workflow_entries:
            instance = workflow_entry.instance
            dossier_erfasst = WorkflowEntry.objects.filter(
                instance=instance,
                workflow_item=WORKFLOW_ITEM_DOSSIER_ERFASST,
            )

            if not dossier_erfasst.exists():
                self.stdout.write(
                    f"For the instance {instance.pk} the workflow entry {workflow_entry.pk} was chnanged from workflow item 'Eingang online' to workflow item 'Dossier erfasst'"
                )
                workflow_entry.workflow_item_id = WORKFLOW_ITEM_DOSSIER_ERFASST
                workflow_entry.save()
            else:
                self.stdout.write(
                    f"Skipping {instance.pk} {workflow_entry.pk} {workflow_entry.workflow_date} {dossier_erfasst.first().workflow_date}"
                )

        # Delete Worfklow Item "Eingang Online"
        self.stdout.write("Deleting workflow item 'Eingang Online'")
        WorkflowItem.objects.get(workflow_item_id=WORKFLOW_ITEM_EINGANG_ONLINE).delete()

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
