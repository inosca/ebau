from alexandria.core.models import Document
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """Change the type of the camac-instance-id value in alexandria document metainfo from integer to string"""

    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        alexandria_documents = Document.objects.all()

        for document in alexandria_documents:
            document.metainfo["camac-instance-id"] = str(
                document.metainfo["camac-instance-id"]
            )
            document.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
