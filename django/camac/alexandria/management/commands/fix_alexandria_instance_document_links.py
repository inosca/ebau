from alexandria.core.models import Document
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import CharField, F, IntegerField, Value
from django.db.models.functions import Cast, Replace


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        wrong_type = Document.objects.annotate(
            instance_id=Cast(F("metainfo__camac-instance-id"), output_field=CharField())
        ).exclude(instance_id__startswith='"', instance_id__endswith='"')

        for document in wrong_type:
            document.metainfo["camac-instance-id"] = str(
                document.metainfo["camac-instance-id"]
            )
            document.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed type of instance ID in metainfo for document {document.pk}"
                )
            )

        missmatches = Document.objects.exclude(
            instance_document__instance_id=Cast(
                Replace(
                    Cast(F("metainfo__camac-instance-id"), output_field=CharField()),
                    Value('"'),
                    Value(""),
                ),
                output_field=IntegerField(),
            )
        )

        for document in missmatches:
            document.instance_document.instance_id = int(
                document.metainfo["camac-instance-id"]
            )
            document.instance_document.save()
            self.stdout.write(
                self.style.SUCCESS(
                    f"Fixed instance ID missmatch for document {document.pk}"
                )
            )
