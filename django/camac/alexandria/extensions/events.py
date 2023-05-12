from django.db.models.signals import post_save
from django.dispatch import receiver

from alexandria.core.models import Document
from instance.models import InstanceAlexandriaDocument

@receiver(post_save, sender=Document)
def create_instance_document_relation(sender, document, created, **kwargs):
    if created:
        InstanceAlexandriaDocument.objects.create(
            instance_id=document.category.meta["case_id"],
            document=document,
        )
