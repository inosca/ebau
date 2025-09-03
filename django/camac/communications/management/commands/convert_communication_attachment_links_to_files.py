import os

from django.conf import settings
from django.core.files.storage import Storage
from django.core.management.base import BaseCommand
from tqdm import tqdm

from camac.communications.models import CommunicationsAttachment


class Command(BaseCommand):
    """
    Converts communications attachment files from links to copies.

    Creates files which were previously deleted from moving files to the document module.
    """

    def handle(self, *args, **options):
        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            filters = {"file_attachment": "", "document_attachment__isnull": False}
        else:
            filters = {"file_attachment": "", "alexandria_file__isnull": False}

        storage = Storage()
        success = 0
        fail = 0
        for attachment in tqdm(
            CommunicationsAttachment.objects.filter(**filters).iterator(),
            desc="Fixing file attachments",
        ):
            try:
                if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
                    file_obj = getattr(attachment, "document_attachment")
                    orig_name = file_obj.name
                    display_name = file_obj.context.get("displayName") or orig_name
                    file_data = getattr(file_obj, "path")
                else:
                    file_obj = getattr(attachment, "alexandria_file")
                    orig_name = file_obj.name
                    display_name = file_obj.document.title or orig_name
                    file_data = getattr(file_obj, "content")
                _, ext = os.path.splitext(orig_name)
                if not display_name.endswith(ext):
                    new_name = f"{display_name}{ext}"
                else:
                    new_name = display_name

                # Convert invalid display names into valid ones
                new_name = storage.get_valid_name(new_name)

                attachment.file_attachment.save(new_name, file_data)
                success += 1
            except Exception as e:
                self.stderr.write(
                    f"Error processing attachment {attachment.pk} ({attachment.message.topic.instance_id}): {e}"
                )
                fail += 1

        self.stdout.write(
            f"Migrated {success} communications attachments, failed: {fail}"
        )
