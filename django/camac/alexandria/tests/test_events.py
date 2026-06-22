import pytest
from alexandria.core.factories import CategoryFactory
from alexandria.core.models import Document
from django.utils.translation import gettext as _

from camac.instance.models import HistoryActionConfig, HistoryEntry


@pytest.mark.django_db
def test_event_creation(instance):
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


@pytest.mark.django_db
def test_event_mark_no_instance_no_history(
    mocker,
    settings,
    alexandria_settings,
    alexandria_document_factory,
    alexandria_mark_factory,
):
    alexandria_settings["LOG_MARKS_IN_HISTORY"] = True
    create_history_entry = mocker.patch(
        "camac.alexandria.extensions.events.create_history_entry"
    )

    document = alexandria_document_factory()

    mark = alexandria_mark_factory()
    document.marks.add(mark)

    create_history_entry.assert_not_called()


@pytest.mark.parametrize(("has_file"), [False, True])
@pytest.mark.django_db
def test_event_mark_journal_history(
    instance,
    mocker,
    settings,
    alexandria_settings,
    application_settings,
    alexandria_document_factory,
    alexandria_mark_factory,
    alexandria_file_factory,
    has_file,
):
    alexandria_settings["LOG_MARKS_IN_HISTORY"] = True

    document = alexandria_document_factory(metainfo={"camac-instance-id": instance.pk})
    if has_file:
        alexandria_file_factory(document=document)
    else:
        document.files.all().delete()

    mark = alexandria_mark_factory()
    document.marks.add(mark)

    # if the document does not happen to have a file, the checksum is ignored.
    doc_title = document.title
    if has_file:
        doc_title += f" {document.get_latest_original().checksum}"

    gettext_values = {
        "doc": doc_title,
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
