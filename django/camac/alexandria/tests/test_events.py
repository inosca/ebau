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


def test_event_mark_no_instance_no_history(
    db, mocker, settings, alexandria_document_factory, alexandria_mark_factory
):
    settings.ALEXANDRIA["LOG_MARKS_IN_HISTORY"] = True
    create_history_entry = mocker.patch(
        "camac.alexandria.extensions.events.create_history_entry"
    )

    document = alexandria_document_factory()

    mark = alexandria_mark_factory()
    document.marks.add(mark)

    create_history_entry.assert_not_called()


def test_event_mark_journal_history(
    db,
    instance,
    mocker,
    settings,
    alexandria_document_factory,
    alexandria_mark_factory,
    alexandria_file_factory,
):
    settings.ALEXANDRIA["LOG_MARKS_IN_HISTORY"] = True
    create_history_entry = mocker.patch(
        "camac.alexandria.extensions.events.create_history_entry"
    )

    document = alexandria_document_factory(metainfo={"camac-instance-id": instance.pk})
    alexandria_file_factory(document=document)

    mark = alexandria_mark_factory()
    document.marks.add(mark)

    assert create_history_entry.call_count == 1
    text = create_history_entry.call_args.kwargs["text"]

    assert (
        f"Dokument {document.title} {document.get_latest_original().checksum} wurde als {mark.name} markiert."
        == text
    )

    document.marks.remove(mark)

    assert create_history_entry.call_count == 2

    text = create_history_entry.call_args_list[1].kwargs["text"]

    assert (
        f"Markierung {mark.name} wurde vom Dokument {document.title} {document.get_latest_original().checksum} entfernt."
        == text
    )
