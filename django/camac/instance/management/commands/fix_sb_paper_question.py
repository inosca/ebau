from logging import getLogger

from caluma.caluma_form.models import Document
from django.core.management.base import BaseCommand
from django.db import transaction

log = getLogger(__name__)


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", action="store_true", dest="dry")

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()
        fix_count = 0

        for sb_document in Document.objects.filter(form_id__in=["sb1", "sb2"]):
            if sb_document.answers.filter(question_id="papierdossier").exists():
                continue

            case = sb_document.work_item.case

            log.warn(
                f"Question 'papierdossier' was not filled for '{sb_document.form_id}' form on instance {case.meta.get('camac-instance-id')} -- fixing"
            )

            sb_document.answers.create(
                question_id="papierdossier",
                value=case.document.answers.get(question_id="papierdossier").value,
            )

            fix_count += 1

        if fix_count:
            log.warn("")
            log.warn(f"Fixed {fix_count} instances")

        if options.get("dry"):
            transaction.savepoint_rollback(tid)
        else:
            transaction.savepoint_commit(tid)
