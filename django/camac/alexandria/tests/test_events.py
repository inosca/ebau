from alexandria.core.factories import CategoryFactory
from alexandria.core.models import Document
from django.utils.translation import gettext as _

from camac.instance.models import HistoryActionConfig, HistoryEntry


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
    application_settings,
    alexandria_document_factory,
    alexandria_mark_factory,
    alexandria_file_factory,
):
    settings.ALEXANDRIA["LOG_MARKS_IN_HISTORY"] = True

    document = alexandria_document_factory(metainfo={"camac-instance-id": instance.pk})
    alexandria_file_factory(document=document)

    mark = alexandria_mark_factory()
    document.marks.add(mark)
    gettext_values = {
        "doc": f"{document.title} {document.get_latest_original().checksum}",
        "mark": mark.name,
    }

    history_entries = HistoryEntry.objects.all()

    assert history_entries.count() == 1
    history_entry = history_entries.first()
    text = history_entry.title

    assert _("Document %(doc)s was marked as %(mark)s.") % gettext_values == text
    assert history_entry.history_type == HistoryActionConfig.HISTORY_TYPE_DOCUMENT_MARK

    document.marks.remove(mark)

    assert history_entries.count() == 2
    history_entry = history_entries.order_by("created_at").all()[1]
    text = history_entry.title

    assert (
        _("Mark %(mark)s was removed from document %(doc)s.") % gettext_values == text
    )
    assert history_entry.history_type == HistoryActionConfig.HISTORY_TYPE_DOCUMENT_MARK
