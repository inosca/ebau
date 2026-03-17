import boto3
from alexandria.core.models import File as AlexandriaFile
from django.conf import settings
from django.core.management.base import BaseCommand

S3_ACCESS_KEY_ID = settings.ALEXANDRIA_S3_ACCESS_KEY
S3_SECRET_ACCESS_KEY = settings.ALEXANDRIA_S3_SECRET_KEY
S3_ENDPOINT_URL = settings.ALEXANDRIA_S3_ENDPOINT_URL
S3_BUCKET = settings.ALEXANDRIA_S3_BUCKET_NAME


class Command(BaseCommand):
    help = "Reports inconsistencies between Alexandria and the S3 storage"

    def get_object_keys(self) -> list[str]:
        keys = []
        have_next = True
        continuation_token = None
        while have_next:
            data = self.s3_client.list_objects_v2(
                Bucket=S3_BUCKET,
                **(
                    {"ContinuationToken": continuation_token}
                    if continuation_token
                    else {}
                ),
            )
            if data["KeyCount"] > 0:
                keys += [o["Key"] for o in data["Contents"]]
            have_next = data["IsTruncated"]
            if have_next:
                continuation_token = data["NextContinuationToken"]
        return keys

    def print_file(self, alexandria_file):
        if hasattr(alexandria_file.document, "instance_document"):
            instance = alexandria_file.document.instance_document.instance
            self.stdout.write(
                f" - file={alexandria_file.content.name} document={alexandria_file.document.title} instance={instance.pk} ({instance.case.meta.get('dossier-number', None)})"
            )
        else:
            self.stdout.write(
                f" - file={alexandria_file.content.name} document={alexandria_file.document.title} instance=(unknown)"
            )

    def handle(self, *args, **options):
        # Get list of bucket objects:
        s3_session = boto3.session.Session()
        self.s3_client = s3_session.client(
            service_name="s3",
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            endpoint_url=S3_ENDPOINT_URL,
        )
        bucket_file_keys = self.get_object_keys()

        # Get list of Alexandria files:
        alexandria_file_names = AlexandriaFile.objects.values_list("content", flat=True)

        # Get missing objects (Alexandria files w/o corresponding bucket object):
        missing_files = {
            alexandria_file
            for alexandria_file in AlexandriaFile.objects.all()
            if alexandria_file.content.name not in bucket_file_keys
        }

        # Get orphan objects (bucket objects w/o corresponding Alexandria file):
        orphan_objects = {
            bucket_file_key
            for bucket_file_key in bucket_file_keys
            if bucket_file_key not in alexandria_file_names
        }

        # WARNING: For the reports below, if you change the output format, please make
        # sure to adapt any consumers of this script (e.g. monitoring check scripts).

        # Report missing objects:
        self.stdout.write(f"missing: {len(missing_files)}")
        if missing_files:
            for missing_file in missing_files:
                self.print_file(missing_file)

        # Report orphan objects:
        self.stdout.write(f"orphans: {len(orphan_objects)}")
        if orphan_objects:
            for orphan_object in orphan_objects:
                self.stdout.write(f" - {orphan_object}")
