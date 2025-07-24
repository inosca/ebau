from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.communications.models import CommunicationsAttachment


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--commit", help="Commit the changes", action="store_true")

    @transaction.atomic
    def handle(self, *args, **options):
        tid = transaction.savepoint()
        do_commit = options.get("commit")
        verbosity = options.get("verbosity", 1)

        attachments = (
            CommunicationsAttachment.objects.exclude(
                alexandria_file__variant="original"
            )
            .exclude(alexandria_file__isnull=True)
            .select_related("alexandria_file")
        )

        if verbosity >= 2:
            self.stdout.write(f"Processing {attachments.count()} attachment(s)")

        for attachment in tqdm(attachments):
            old_file = attachment.alexandria_file
            new_file = old_file.original

            if verbosity >= 2:
                print(
                    f" > Attachment {attachment.pk}: change '{old_file.pk}' ({old_file.variant}) to {new_file.pk} ({new_file.variant})"
                )

            attachment.alexandria_file = attachment.alexandria_file.original
            attachment.save()

        if do_commit:
            message = "Committing changes to database"
            transaction.savepoint_commit(tid)
        else:
            message = "Rolling back - no changes committed to DB"
            transaction.savepoint_rollback(tid)

        self.stdout.write(message)
        tqdm.write("Completed migration")
