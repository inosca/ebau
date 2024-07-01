from alexandria.core.models import Document
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    """
    Remove public marks from documents that should not be public.

    Set sensitive mark to prevent it in the future.
    """

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        document_to_mark = Document.marks.through.objects.filter(
            mark_id__in=settings.ALEXANDRIA["MARK_VISIBILITY"]["PUBLIC"],
            document__metainfo__contains={"system-generated": True},
        )
        updated = document_to_mark.update(
            mark_id=settings.ALEXANDRIA["MARK_VISIBILITY"]["SENSITIVE"][0]
        )

        print(f"Unpublished {updated} documents.")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
