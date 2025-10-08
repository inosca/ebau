import pytest
from alexandria.core import models as alexandria_models

from camac.ech0211 import models


@pytest.mark.django_db
def test_ech0211_document_model_basics(attachment_factory, attachment_section_factory):
    cat0, cat1, cat2 = attachment_section_factory.create_batch(3)

    doc0, doc1, doc2 = attachment_factory.create_batch(3)

    doc0.attachment_sections.set([cat0])
    doc1.attachment_sections.set([cat1, cat2])
    doc2.attachment_sections.set([cat0, cat1, cat2])

    expected_keys = sorted(
        [
            f"{cat0.pk}-{doc0.pk}",
            f"{cat1.pk}-{doc1.pk}",
            f"{cat2.pk}-{doc1.pk}",
            f"{cat0.pk}-{doc2.pk}",
            f"{cat1.pk}-{doc2.pk}",
            f"{cat2.pk}-{doc2.pk}",
        ]
    )

    res = models.ECH0211Document.objects.all()

    assert sorted(res.values_list("pk", flat=True)) == expected_keys

    for doc in res:
        assert doc.category in [cat0, cat1, cat2]


def test_most_recent_file_prefetched(
    db, alexandria_file_factory, django_assert_num_queries
):
    original = alexandria_models.File.Variant.ORIGINAL

    file0 = alexandria_file_factory(variant=original)
    doc0 = file0.document

    file1 = alexandria_file_factory(variant=original, document=doc0)

    with django_assert_num_queries(2):
        # two queries, one should be the prefetch_related()
        doc = models.ECH0211AlexandriaDocument.objects.get(pk=doc0.pk)
        with django_assert_num_queries(0):
            # This is prefetched, so no additional query allowed.
            # We check that it's the right file, AND that there
            # are no additional queries for property lookup
            assert doc.most_recent_file == file1

    with django_assert_num_queries(2):
        # two queries, everything prefetched
        for doc in models.ECH0211AlexandriaDocument.objects.all():
            assert doc.most_recent_file in [file0, file1]


def test_most_recent_file_uncached(
    db, alexandria_file_factory, django_assert_num_queries
):
    doc = models.ECH0211AlexandriaDocument.objects.create(title="hello")
    file0 = alexandria_file_factory(
        variant=alexandria_models.File.Variant.ORIGINAL,
        # can't use document=doc here, as it's "the wrong type"
        document=alexandria_models.Document.objects.get(pk=doc.pk),
    )
    with django_assert_num_queries(1):
        assert file0 == doc.most_recent_file


def test_most_recent_file_empty(db, django_assert_num_queries, caplog):
    document = models.ECH0211AlexandriaDocument.objects.create()
    document_via_queryset = models.ECH0211AlexandriaDocument.objects.get(pk=document.pk)

    expected_msg = f"{document.pk} has no original files attached"

    with django_assert_num_queries(1):
        assert document.most_recent_file is None
        assert expected_msg in caplog.messages[0]

    caplog.clear()

    with django_assert_num_queries(0):
        assert document_via_queryset.most_recent_file is None
        assert expected_msg in caplog.messages[0]
