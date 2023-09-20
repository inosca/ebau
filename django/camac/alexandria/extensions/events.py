from alexandria.core.models import Document
from django.db.models.signals import post_save
from django.dispatch import receiver

from camac.instance.models import InstanceAlexandriaDocument


@receiver(post_save, sender=Document)
def create_instance_document_relation(sender, instance, created, **kwargs):
    instance_id = instance.metainfo.get("camac-instance-id")

    if created and instance_id:
        InstanceAlexandriaDocument.objects.create(
            instance_id=instance_id,
            document=instance,
        )
