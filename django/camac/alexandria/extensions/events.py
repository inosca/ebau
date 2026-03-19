from alexandria.core.models import Document, Mark
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.utils.translation import gettext as _

from camac.core.models import HistoryActionConfig
from camac.core.utils import create_history_entry
from camac.instance.models import Instance, InstanceAlexandriaDocument


@receiver(post_save, sender=Document)
def create_instance_document_relation(sender, instance, created, **kwargs):
    instance_id = instance.metainfo.get("camac-instance-id")

    if created and instance_id:
        InstanceAlexandriaDocument.objects.create(
            instance_id=instance_id,
            document=instance,
        )


@receiver(m2m_changed, sender=Document.marks.through)
def log_document_mark_mutations(
    sender, instance: Document, action: str, pk_set, **kwargs
):
    if not settings.ALEXANDRIA.get("LOG_MARKS_IN_HISTORY"):
        return

    if action not in ("post_add", "post_remove"):
        return

    instance_id = instance.metainfo.get("camac-instance-id")
    if not instance_id:
        return

    camac_instance = Instance.objects.get(pk=instance_id)

    doc_label = instance.title or str(instance.pk)

    try:
        checksum = instance.get_latest_original().checksum
    except ObjectDoesNotExist:
        checksum = None

    doc_ref = f"{doc_label} {checksum or ''}"

    marks = Mark.objects.filter(pk__in=pk_set)

    for mark in marks:
        mark_name = mark.name.translate()

        values = {"doc": doc_ref, "mark": mark_name}

        if action == "post_add":
            text = _("Document %(doc)s was marked as %(mark)s.") % values
        else:
            text = _("Mark %(mark)s was removed from document %(doc)s.") % values

        create_history_entry(
            instance=camac_instance,
            user=None,
            text=text,
            history_type=HistoryActionConfig.HISTORY_TYPE_DOCUMENT_MARK,
        )
