from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import Case
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", action="store_true", dest="dry")

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        documents_without_family = Document.objects.filter(family__isnull=True)
        if documents_without_family.exists():
            self.stdout.write(
                self.style.WARNING(
                    f"Add missing family of {documents_without_family.count()} documents"
                )
            )
            documents_without_family.update(family_id=F("pk"))

        cases_to_delete = Case.objects.filter(family__instance__isnull=True)
        self.stdout.write(
            self.style.WARNING(
                f"Deleted {cases_to_delete.count()} cases and {cases_to_delete.values('work_items').count()} related work items"
            )
        )
        cases_to_delete.delete()

        documents_to_delete = Document.objects.exclude(form_id="dashboard").filter(
            family__case__isnull=True, family__work_item__isnull=True
        )
        self.stdout.write(
            self.style.WARNING(
                f"Deleted {documents_to_delete.count()} documents and {documents_to_delete.values('answers').count()} related answers"
            )
        )
        documents_to_delete.delete()

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
