import boto3
from alexandria.core.models import Document, File, auto_delete_file_on_delete
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import CharField, Q, Subquery
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast
from django.db.models.signals import post_delete

from camac.instance.models import Instance


class Command(BaseCommand):
    help = "Clean up alexandria models which reference a non existing Instance."

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

    @transaction.atomic
    def clean_alexandria_models(self, commit):
        post_delete.disconnect(auto_delete_file_on_delete, sender=File)
        sid = transaction.savepoint()
        try:
            instance_pks = Instance.objects.annotate(
                pk_str=Cast("pk", output_field=CharField())
            ).values_list("pk_str", flat=True)
            dangling_documents = Document.objects.annotate(
                camac_id_text=KeyTextTransform("camac-instance-id", "metainfo")
            ).filter(~Q(camac_id_text__in=Subquery(instance_pks)))

            if dangling_documents.count():
                print(
                    "Delete all dangling alxeandria models and the attached minio data."
                )
                # This is split up in case there are a lot of documents.
                while (count := dangling_documents.count()) and count > 0:
                    deleted = Document.objects.filter(
                        pk__in=dangling_documents[:100_000].values("pk")
                    ).delete()
                    print(f"Deleted alexandria models: {deleted}")
            else:
                print("No dangling alexandria models found.")

        finally:
            post_delete.connect(auto_delete_file_on_delete, sender=File)

        if commit:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)

    def handle(self, *args, **options):
        s3_session = boto3.session.Session()

        self.clean_alexandria_models(options["commit"])

        minio_config = {
            "name": "alexandria-media",
            "s3_access_key": settings.ALEXANDRIA_S3_ACCESS_KEY,
            "s3_secret_access_key": settings.ALEXANDRIA_S3_SECRET_KEY,
            "s3_endpoint_url": settings.ALEXANDRIA_S3_ENDPOINT_URL,
            "s3_bucket": settings.ALEXANDRIA_S3_BUCKET_NAME,
        }
        print(f"\033[1m{minio_config['name']}\033[0m")

        print("Fetching list of files from database")
        db_files = File.objects.all().values_list("content", flat=True)

        print("Connecting to storage")
        s3_client = s3_session.client(
            service_name="s3",
            aws_access_key_id=minio_config["s3_access_key"],
            aws_secret_access_key=minio_config["s3_secret_access_key"],
            endpoint_url=minio_config["s3_endpoint_url"],
        )

        print("Fetching list of files in bucket")
        bucket_files = self.get_object_keys(s3_client, minio_config)

        print(
            f"Cleaning up among {len(bucket_files)} bucket objects and {len(db_files)} DB entries"
        )
        minio_config["stats"] = {
            "total": len(bucket_files),
            "deleted": 0,
        }
        for f in bucket_files:
            if f not in db_files:
                # file not found in db, can be deleted
                self.delete_file(s3_client, minio_config, f, options["commit"])

        print(f"\033[1m{minio_config['name']} stats: {minio_config['stats']}\033[0m")
