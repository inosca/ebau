import pytest


def test_event_creation(db, instance, document_factory):
    document = document_factory(meta={instance})

    assert document.instances.count() == 1
    assert document.instances.first().instance.pk == instance.pk

    document.description = "new description"
    document.save()

    assert document.instances.count() == 1
