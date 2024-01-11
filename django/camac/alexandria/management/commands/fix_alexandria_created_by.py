from alexandria.core.models import Document, File
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import F, OuterRef, Q, Subquery


class Command(BaseCommand):
    """
    Fix mismatched created_by_user and created_by_group fields on documents.

    Fixing it by taking the first file's created_by_user and created_by_group.
    """

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        document_files = File.objects.filter(document_id=OuterRef("pk")).order_by(
            "created_at"
        )

        mismatched = (
            Document.objects.annotate(
                file_created_by_user=Subquery(
                    document_files.values("created_by_user")[:1]
                ),
                file_created_by_group=Subquery(
                    document_files.values("created_by_group")[:1]
                ),
            )
            .filter(
                (
                    ~Q(created_by_user=F("file_created_by_user"))
                    & Q(created_by_user__isnull=False)
                    & Q(file_created_by_user__isnull=False)
                )
                | (
                    ~Q(created_by_group=F("file_created_by_group"))
                    & Q(created_by_group__isnull=False)
                    & Q(file_created_by_group__isnull=False)
                )
            )
            .update(
                created_by_user=F("file_created_by_user"),
                created_by_group=F("file_created_by_group"),
            )
        )
        print(f"Fixed created_by for {mismatched} documents.")

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
