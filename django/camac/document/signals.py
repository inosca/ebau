import logging

from django.db.models import signals
from django.dispatch import receiver
from sorl.thumbnail import delete

from .models import Attachment

logger = logging.getLogger(__name__)


@receiver(signals.pre_delete, sender=Attachment)
def auto_delete_attachment_file(sender, instance, **kwargs):
    if instance.path:
        try:
            delete(instance.path)
        except FileNotFoundError:  # pragma: no cover
            logger.exception(f"Couldn't delete file {instance.path.path}")
