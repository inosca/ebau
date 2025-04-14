import boto3
import botocore
from alexandria.core.models import File as AlexandriaFile
from django.conf import settings
from django.core.management.base import BaseCommand

S3_ACCESS_KEY_ID = settings.ALEXANDRIA_S3_ACCESS_KEY
S3_SECRET_ACCESS_KEY = settings.ALEXANDRIA_S3_SECRET_KEY
S3_ENDPOINT_URL = settings.ALEXANDRIA_S3_ENDPOINT_URL
S3_BUCKET = settings.ALEXANDRIA_S3_BUCKET_NAME
S3_SSE_CUSTOMER_KEY = settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET


class Command(BaseCommand):
    help = "Detect and attempt to restore missing Alexandria files in storage"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Restore files for real",
        )

    def get_object_keys(self, s3_client) -> list[str]:
        keys = []
        have_next = True
        continuation_token = None
        while have_next:
            data = s3_client.list_objects_v2(
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

    def restore_file(self, alexandria_file, sources: list, s3_client, commit: bool):
        restored = False
        for source in sources:
            print(
                f" › Restoring: {source.content.name} -› {alexandria_file.content.name}"
            )
            try:
                if commit:
                    s3_client.copy_object(
                        Bucket=S3_BUCKET,
                        Key=alexandria_file.content.name,
                        SSECustomerAlgorithm="AES256",
                        SSECustomerKey=S3_SSE_CUSTOMER_KEY,
                        CopySource={"Bucket": S3_BUCKET, "Key": source.content.name},
                        CopySourceSSECustomerAlgorithm="AES256",
                        CopySourceSSECustomerKey=S3_SSE_CUSTOMER_KEY,
                    )
                    restored = True
                break
            except botocore.exceptions.ClientError:
                print("   ERROR: Could not restore, likely source is also missing")
        return restored

    def print_file(self, alexandria_file, indentation: int = 0) -> bool:
        padding = " " * indentation
        if hasattr(alexandria_file.document, "instance_document"):
            instance = alexandria_file.document.instance_document.instance
            print(
                f"{padding}instance={instance.pk} ({instance.case.meta.get('dossier-number', None)}) file={alexandria_file.content.name}"
            )
        else:
            print(f"{padding}instance=(unknown) file={alexandria_file.content.name}")

    def print_summary(self, files: list):
        # Build {instances-›documents-›files} tree:
        instances = {}
        for file in files:
            if hasattr(file.document, "instance_document"):
                instance = file.document.instance_document.instance
            else:
                instance = None
            instance_index = str(instance.pk) if instance else "unknown"
            if instance_index not in instances:
                instances[instance_index] = {"instance": instance, "documents": {}}
            instance_entry = instances[instance_index]

            document_index = str(file.document.pk)
            if document_index not in instance_entry["documents"]:
                instance_entry["documents"][document_index] = {
                    "document": file.document,
                    "files": [],
                }
            document_entry = instance_entry["documents"][document_index]
            document_entry["files"].append(file)

        # Print tree:
        for instance_index in instances:
            instance_entry = instances[instance_index]
            instance = instance_entry["instance"]
            if instance:
                dossier = instance.case.meta.get("dossier-number", "unknown")
                title = f"{dossier} <https://admin.ebau.gr.ch/cases/{instance.pk}/documents>"
            else:
                dossier = "unknown"
                title = f"{dossier}"
            print(f"\n{title}")
            for document_index in instance_entry["documents"]:
                document_entry = instance_entry["documents"][document_index]
                document = document_entry["document"]
                print(f" · {document.title}")
                for file in document_entry["files"]:
                    print(f"    · {file.content.name}")

    def handle(self, *args, **options):
        s3_session = boto3.session.Session()

        print("Connecting to storage")
        s3_client = s3_session.client(
            service_name="s3",
            aws_access_key_id=S3_ACCESS_KEY_ID,
            aws_secret_access_key=S3_SECRET_ACCESS_KEY,
            endpoint_url=S3_ENDPOINT_URL,
        )

        print("Fetching list of files in bucket")
        bucket_files = self.get_object_keys(s3_client)

        print("Checking all Alexandria files against bucket")
        total = AlexandriaFile.objects.count()
        count = 0
        unrestored_files = []
        for alexandria_file in AlexandriaFile.objects.all():
            count += 1
            print(f"{count}/{total}", end="\r")
            if alexandria_file.content.name not in bucket_files:
                self.print_file(alexandria_file)
                equals = (
                    AlexandriaFile.objects.none()
                    if not alexandria_file.checksum
                    else AlexandriaFile.objects.filter(
                        checksum=alexandria_file.checksum
                    ).exclude(pk=alexandria_file.pk)
                )
                nequals = equals.count()
                print(
                    f" › other files with same SHA256 ({alexandria_file.checksum}): {nequals}"
                )
                for equal in equals[:3]:
                    self.print_file(equal, 3)
                if not self.restore_file(
                    alexandria_file, equals, s3_client, options["commit"]
                ):
                    unrestored_files.append(alexandria_file)

        self.print_summary(unrestored_files)
