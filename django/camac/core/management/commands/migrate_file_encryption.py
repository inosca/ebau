from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.files.storage import storages
from django.core.management.base import BaseCommand
from tqdm import tqdm

from camac.communications.models import CommunicationsAttachment


class Command(BaseCommand):
    help = "Swaps plain text file content to encrypted content"

    def handle(self, *args, **options):
        if not settings.EBAU_ENABLE_AT_REST_ENCRYPTION:
            return self.stdout.write(
                self.style.WARNING(
                    "Encryption is not enabled. Skipping encryption of files."
                )
            )

        failed_files = []
        # flip between default and encrypted storage to have the correct parameters in the requests
        query = CommunicationsAttachment.objects.filter(file_attachment__isnull=False)
        encrypted_storage = storages.create_storage(settings.STORAGES["default"])

        unencrypted_storage_setting = settings.STORAGES["default"]
        if (
            "OPTIONS" not in unencrypted_storage_setting
            or "object_parameters" not in unencrypted_storage_setting["OPTIONS"]
        ):
            raise ImproperlyConfigured("Storage is misconfigured for encryption")

        del unencrypted_storage_setting["OPTIONS"]["object_parameters"]
        unencrypted_storage = storages.create_storage(unencrypted_storage_setting)
        for file in tqdm(query.iterator(50), total=query.count()):
            # get original file content
            file.file_attachment.storage = unencrypted_storage
            try:
                content = file.file_attachment.open()

                # overwrite with encrypted content
                file.file_attachment.storage = encrypted_storage
                file.file_attachment.save(file.file_attachment.name, content)
            except Exception as e:
                self.stdout.write(
                    self.style.WARNING(f"Error for file {str(file.pk)}: {e}")
                )
                failed_files.append(str(file.pk))
                continue

        self.stdout.write(self.style.WARNING(f"These files failed:\n{failed_files}"))
