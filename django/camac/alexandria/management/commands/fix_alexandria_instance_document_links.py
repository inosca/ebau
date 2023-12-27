from alexandria.core.models import Document
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        instance_ids = list(Instance.objects.values_list("pk", flat=True))

        # Get all documents that have an instance id as integer in the metainfo
        affected_documents = Document.objects.filter(
            **{"metainfo__camac-instance-id__in": instance_ids}
        )

        for document in affected_documents:
            instance_id = document.metainfo["camac-instance-id"]

            assert (
                type(instance_id) == int
            ), f'"camac-instance-id" of document "{document.pk}" is not an integer'

            document.metainfo["camac-instance-id"] = str(instance_id)
            document.save()

            assert (
                instance_id != document.instance_document.instance_id
            ), f'Instance relationship of document "{document.pk}" is correct'

            document.instance_document.instance_id = instance_id
            document.instance_document.save()
