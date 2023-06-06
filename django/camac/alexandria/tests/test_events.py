from alexandria.core.models import Document
from django.db.models.signals import post_save

from camac.alexandria.extensions.events import create_instance_document_relation


def test_event_creation(db, instance, alexandria_category):
    post_save.connect(create_instance_document_relation, sender=Document)

    document = Document.objects.create(
        title="Test", category=alexandria_category, metainfo={"case_id": instance.pk}
    )
    assert document.instance_document.instance.pk == instance.pk

    document.metainfo["case_id"] = 2
    document.save()
    assert document.instance_document.instance.pk == instance.pk

    post_save.disconnect(create_instance_document_relation, sender=Document)
