from alexandria.core.models import Document
from django.db.models.signals import post_save
from django.dispatch import receiver

from camac.instance.models import InstanceAlexandriaDocument


@receiver(post_save, sender=Document)
def create_instance_document_relation(sender, instance, created, **kwargs):
    if created:
        InstanceAlexandriaDocument.objects.create(
            instance_id=instance.metainfo["case_id"],
            document=instance,
        )
