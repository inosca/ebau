def test_event_creation(db, instance, document_factory):
    document = document_factory(meta={"case_id": instance.pk})

    assert document.instance_document.instance.pk == instance.pk
