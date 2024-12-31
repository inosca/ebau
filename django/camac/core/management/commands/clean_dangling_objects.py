import boto3
import botocore
from alexandria.core.models import File
from django.conf import settings
from django.core.management.base import BaseCommand

from camac.communications.models import CommunicationsAttachment

MAPPINGS = [
    {
        "name": "ebau-media",
        "get_data": lambda: CommunicationsAttachment.objects.all().values_list(
            "file_attachment", flat=True
        ),
        "s3_access_key": settings.STORAGES["default"]["OPTIONS"]["access_key"],
        "s3_secret_access_key": settings.STORAGES["default"]["OPTIONS"]["secret_key"],
        "s3_endpoint_url": settings.STORAGES["default"]["OPTIONS"]["endpoint_url"],
        "s3_bucket": settings.STORAGES["default"]["OPTIONS"]["bucket_name"],
    },
    {
        "name": "alexandria-media",
        "get_data": lambda: File.objects.all().values_list("content", flat=True),
        "s3_access_key": settings.ALEXANDRIA_S3_ACCESS_KEY,
        "s3_secret_access_key": settings.ALEXANDRIA_S3_SECRET_KEY,
        "s3_endpoint_url": settings.ALEXANDRIA_S3_ENDPOINT_URL,
        "s3_bucket": settings.ALEXANDRIA_S3_BUCKET_NAME,
    },
]


class Command(BaseCommand):
    help = "Clean up unreferenced files and warn about unencrypted files in the storage bucket"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Delete data for real",
        )

    def get_object_keys(self, s3_client, mapping: dict):
        keys = []
        have_next = True
        continuation_token = None
        while have_next:
            data = s3_client.list_objects_v2(
                Bucket=mapping["s3_bucket"],
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

    def delete_file(self, s3_client, mapping: dict, fname: str, commit: bool):
        print(f"Deleting unreferenced file: {fname}")
        if commit:
            s3_client.delete_object(Bucket=mapping["s3_bucket"], Key=fname)
        mapping["stats"]["deleted"] += 1

    def check_encryption(self, s3_client, mapping: dict, fname: str):
        try:
            s3_client.get_object(Bucket=mapping["s3_bucket"], Key=fname)
            # If this didn't throw any exception, we were able to fetch it
            # without SSE-C key (i.e. not good):
            print(f"WARNING, unencrypted file: {fname}")
            mapping["stats"]["unencrypted"] += 1
        except botocore.exceptions.ClientError:
            # Exception means we could not fetch it without SSE-C key
            # (i.e. good):
            mapping["stats"]["encrypted"] += 1

    def handle(self, *args, **options):
        s3_session = boto3.session.Session()

        for m in MAPPINGS:
            print(f"\033[1m{m['name']}\033[0m")

            print("Fetching list of files from database")
            db_files = m["get_data"]()

            print("Connecting to storage")
            s3_client = s3_session.client(
                service_name="s3",
                aws_access_key_id=m["s3_access_key"],
                aws_secret_access_key=m["s3_secret_access_key"],
                endpoint_url=m["s3_endpoint_url"],
            )

            print("Fetching list of files in bucket")
            bucket_files = self.get_object_keys(s3_client, m)

            print(
                f"Cleaning up among {len(bucket_files)} bucket objects and {len(db_files)} DB entries"
            )
            m["stats"] = {
                "total": len(bucket_files),
                "encrypted": 0,
                "unencrypted": 0,
                "deleted": 0,
            }
            for f in bucket_files:
                if f in db_files:
                    # file found in db, check if it's encrypted
                    self.check_encryption(s3_client, m, f)
                else:
                    # file not found in db, can be deleted
                    self.delete_file(s3_client, m, f, options["commit"])

            print(f"\033[1m{m['name']} stats: {m['stats']}\033[0m")
