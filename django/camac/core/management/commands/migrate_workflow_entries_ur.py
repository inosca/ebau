from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import WorkflowEntry

SUBMIT_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S%z"
WORKFLOW_ITEM_EINGANG_POST = 10
WORKFLOW_ITEM_DOSSIER_IN_UREC_ERFASST = 12
WORKFLOW_ITEM_EINGANG_ONLINE = 12000000


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

        cases = (
            Case.objects.all().exclude(instance__instance_state__name="new").iterator()
        )

        for case in cases:
            try:
                internal_workflow_entries = WorkflowEntry.objects.filter(
                    instance=case.instance,
                    workflow_item=WORKFLOW_ITEM_DOSSIER_IN_UREC_ERFASST,
                )
                if internal_workflow_entries:
                    # No workflow entry migration because the work-item "Dossiereingang" was renamed to "Eingang Post" and the id didn't change

                    if "submit-date" not in case.meta:
                        case.meta[
                            "submit-date"
                        ] = internal_workflow_entries.first().workflow_date.strftime(
                            SUBMIT_DATE_FORMAT
                        )
                        case.save()

                        self.stdout.write(
                            f"For the instance {case.instance.pk} the submit date {case.meta['submit-date']} was written to the case meta"
                        )

                else:
                    workflow_entries = WorkflowEntry.objects.filter(
                        instance=case.instance,
                        workflow_item=WORKFLOW_ITEM_EINGANG_POST,
                    )

                    if workflow_entries:
                        if "submit-date" not in case.meta:
                            case.meta[
                                "submit-date"
                            ] = workflow_entries.first().workflow_date.strftime(
                                SUBMIT_DATE_FORMAT
                            )
                            case.save()

                            self.stdout.write(
                                f"For the instance {case.instance.pk} the submit date {case.meta['submit-date']} was written to the case meta"
                            )

                        workflow_entries.update(
                            workflow_item=WORKFLOW_ITEM_EINGANG_ONLINE
                        )

                        self.stdout.write(
                            f"For the instance {case.instance.pk} the workflow entries {[workflow_entry.workflow_entry_id for workflow_entry in workflow_entries]} where chnanged from workflow item Nr. 10 to workflow item Nr. 12000000"
                        )
            except Exception as e:  # pragma: no cover # noqa: B902
                self.stdout.write(f"Could not migrate case {case.id}: {e}")

        if options["dry"]:  # pragma: no cover
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
