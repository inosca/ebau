from django.conf import settings
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
            filter_kwargs = {
                "file_attachment": "",
                "document_attachment__isnull": False,
            }
            file_attr = "document_attachment"
            data_attr = "path"
        else:
            filter_kwargs = {
                "file_attachment": "",
                "alexandria_file__isnull": False,
            }
            file_attr = "alexandria_file"
            data_attr = "content"

        for attachment in tqdm(
            CommunicationsAttachment.objects.filter(**filter_kwargs).iterator(),
            desc="Fixing file attachments",
        ):
            file_obj = getattr(attachment, file_attr)
            name = file_obj.name
            file_data = getattr(file_obj, data_attr)
            attachment.file_attachment.save(name, file_data)
