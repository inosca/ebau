from alexandria.core.factories import CategoryFactory
from alexandria.core.models import Document


def test_event_creation(db, instance):
    alexandria_category = CategoryFactory()

    document = Document.objects.create(
        title="Test",
        category=alexandria_category,
        metainfo={"camac-instance-id": instance.pk},
    )
    assert document.instance_document.instance.pk == instance.pk

    document.metainfo["camac-instance-id"] = 2
    document.save()
    assert document.instance_document.instance.pk == instance.pk
