from caluma.caluma_form.models import Document
from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef

from camac.caluma.api import CalumaApi
from camac.caluma.extensions.events.decision import copy_municipality_tags
from camac.instance.models import Instance
from camac.instance.utils import set_construction_control


class Command(BaseCommand):
    help = """Command to fix instances with a decision but no SB1 work item /
    document because of a bug in the eCH-0211 API."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            default=False,
            dest="dry",
            action="store_true",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        sb1_task = Task.objects.get(pk="sb1")
        caluma_api = CalumaApi()

        instances = (
            Instance.objects.filter(instance_state__name="sb1")
            .exclude(
                Exists(WorkItem.objects.filter(task=sb1_task, case=OuterRef("case")))
            )
            .order_by("pk")
        )

        for instance in instances:
            municipality = instance.responsible_service(filter_type="municipality")
            name = f"{instance.case.document.form.name} {instance.pk} ({municipality.get_name()})"
            self.stdout.write(self.style.SUCCESS(f"Fix SB1 for {name}"))

            # Set construction control correctly
            if not instance.responsible_service(filter_type="construction_control"):
                construction_control = set_construction_control(instance)
                copy_municipality_tags(instance, construction_control)
                self.stdout.write(
                    f"\t- Set construction control: {construction_control.get_name()}"
                )

            # Set case status to running
            if not instance.case.status == Case.STATUS_RUNNING:
                instance.case.status = Case.STATUS_RUNNING
                instance.case.save()
                self.stdout.write(f"\t- Set case status: {instance.case.status}")

            # Create missing SB1 work item
            decision = instance.case.work_items.get(
                task_id="decision", status=WorkItem.STATUS_COMPLETED
            )
            user = BaseUser(
                username=decision.closed_by_user, group=decision.closed_by_group
            )
            sb1 = instance.case.work_items.create(
                task=sb1_task,
                name=sb1_task.name,
                status=WorkItem.STATUS_READY,
                addressed_groups=[],
                controlling_groups=[],
                created_at=decision.closed_at,
                created_by_user=decision.closed_by_user,
                created_by_group=decision.closed_by_group,
                previous_work_item=decision,
                document=Document.objects.create_document_for_task(sb1_task, user),
            )
            # Copy paper answer
            sb1.document.answers.update_or_create(
                question_id="is-paper",
                defaults={
                    "value": instance.case.document.answers.get(
                        question_id="is-paper"
                    ).value
                },
            )
            # Copy personal data
            caluma_api.copy_table_answer(
                source_document=instance.case.document,
                target_document=sb1.document,
                source_question="personalien-sb",
                target_question="personalien-sb1-sb2",
                source_question_fallback="personalien-gesuchstellerin",
            )

            self.stdout.write("\t- Create missing SB1 work item")

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
