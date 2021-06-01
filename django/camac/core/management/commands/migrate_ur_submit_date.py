from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand

from camac.core.models import WorkflowEntry

DOSSIER_ERFASST_WORKFLOW_ITEM = 12
DOSSIER_EINGEREICHT_WORKFLOW_ITEM = 10


class Command(BaseCommand):
    help = "Add the workflow date to the case meta as submit date"

    def handle(self, *args, **kwargs):
        # for case in Case.objects.all().exclude(meta__has_key="submit-date"):
        for case in Case.objects.all():
            workflow_date = self.get_workflow_date(case)
            if workflow_date:
                case.meta.update(
                    {"submit-date": workflow_date.strftime("%Y-%m-%dT%H:%M:%S%z")}
                )
                # case.save()
                self.stdout.write(
                    f"The submit date for the case with instance_id {case.meta['camac-instance-id']} was set to {workflow_date}"
                )

    def get_workflow_date(self, case):
        try:
            workflow_entry_dossier_submitted = WorkflowEntry.objects.filter(
                instance_id=case.meta["camac-instance-id"],
                workflow_item_id=DOSSIER_EINGEREICHT_WORKFLOW_ITEM,
            )

            if workflow_entry_dossier_submitted:
                self.stdout.write("Dossier was submitted")
                return workflow_entry_dossier_submitted.first().workflow_date
            else:
                workflow_entry_dossier_created = WorkflowEntry.objects.get(
                    instance_id=case.meta["camac-instance-id"],
                    workflow_item_id=DOSSIER_ERFASST_WORKFLOW_ITEM,
                )
                self.stdout.write("Dossier was created")
                return workflow_entry_dossier_created.workflow_date

        except WorkflowEntry.DoesNotExist:
            return None
