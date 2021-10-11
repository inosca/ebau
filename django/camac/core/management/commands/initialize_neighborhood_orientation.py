from caluma.caluma_form.api import save_document
from caluma.caluma_form.models import Form
from caluma.caluma_workflow.models import Case, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = "Initialize work items for the neighborhood orientation"

    def add_arguments(self, parser):
        parser.add_argument("-d", "--dry-run", action="store_true", dest="dry")

    def handle(self, *args, **options):
        tid = transaction.savepoint()

        self.initialize_work_items()

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)

    @transaction.atomic
    def initialize_work_items(self):
        form = Form.objects.get(pk="neighborhood-orientation")

        cases = Case.objects.filter(
            instance__instance_state__name__in=[
                "circulation_init",
                "circulation",
                "coordination",
                "rejected",
            ],
        ).exclude(work_items__task_id="neighborhood-orientation")

        for i, case in enumerate(cases):
            service = case.instance.responsible_service(filter_type="municipality")

            if not service:
                self.stdout.write(
                    self.style.ERROR(
                        f"No responsible service for instance {case.instance.pk}"
                    )
                )
                continue

            WorkItem.objects.create(
                addressed_groups=[str(service.pk)],
                controlling_groups=[],
                task_id="neighborhood-orientation",
                document=save_document(form),
                case=case,
                status=WorkItem.STATUS_SUSPENDED
                if case.instance.instance_state.name == "rejected"
                else WorkItem.STATUS_READY,
                previous_work_item=case.work_items.filter(
                    task_id="ebau-number"
                ).first(),
            )

            if i % 100 == 0:
                self.stdout.write(f"[{i} / {cases.count()}]")
