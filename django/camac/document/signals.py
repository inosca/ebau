import logging
from pathlib import Path

from django.db.models import signals
from django.dispatch import receiver

from .models import Attachment

logger = logging.getLogger(__name__)


@receiver(signals.pre_delete, sender=Attachment)
def auto_delete_attachment_file(sender, instance, **kwargs):
    if instance.path:
        path = Path(instance.path.path)
        try:
            path.unlink()
        except FileNotFoundError:  # pragma: no cover
            logger.exception(f"Couldn't delete file {path}")
