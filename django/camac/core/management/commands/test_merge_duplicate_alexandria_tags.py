import pytest
from alexandria.core.factories import DocumentFactory, TagFactory
from alexandria.core.models import Tag
from django.core.management import call_command

pytestmark = pytest.mark.django_db


def test_merge_duplicate_alexandria_tags():
    TagFactory(
        name="AfU",
        created_by_group="1",
        modified_by_group="1",
    )
    duplicate_tag = TagFactory(
        name="AfU",
        created_by_group="1",
        modified_by_group="1",
    )
    other_group_tag = TagFactory(
        name="AfU",
        created_by_group="2",
        modified_by_group="2",
    )

    document_with_duplicate = DocumentFactory()
    document_with_both_tags = DocumentFactory()

    duplicate_group_tags = Tag.objects.filter(name="AfU", created_by_group="1")

    document_with_duplicate.tags.add(duplicate_tag)
    document_with_both_tags.tags.add(*duplicate_group_tags)

    call_command("merge_duplicate_alexandria_tags", commit=True)

    remaining_tag = Tag.objects.get(name="AfU", created_by_group="1")

    assert Tag.objects.filter(name="AfU", created_by_group="1").count() == 1
    assert Tag.objects.filter(pk=other_group_tag.pk).exists()

    assert document_with_duplicate.tags.filter(pk=remaining_tag.pk).exists()
    assert document_with_duplicate.tags.count() == 1

    assert document_with_both_tags.tags.filter(pk=remaining_tag.pk).exists()
    assert document_with_both_tags.tags.count() == 1


def test_merge_duplicate_alexandria_tags_dry_run():
    TagFactory(
        name="Dry Run Tag",
        created_by_group="1",
        modified_by_group="1",
    )
    duplicate_tag = TagFactory(
        name="Dry Run Tag",
        created_by_group="1",
        modified_by_group="1",
    )

    document = DocumentFactory()
    document.tags.add(duplicate_tag)

    call_command("merge_duplicate_alexandria_tags")

    assert Tag.objects.filter(name="Dry Run Tag", created_by_group="1").count() == 2
    assert Tag.objects.filter(pk=duplicate_tag.pk).exists()
    assert document.tags.filter(pk=duplicate_tag.pk).exists()


def test_merge_duplicate_alexandria_tags_without_duplicates():
    TagFactory(
        name="Unique Tag",
        created_by_group="1",
        modified_by_group="1",
    )

    call_command("merge_duplicate_alexandria_tags")

    assert Tag.objects.filter(name="Unique Tag", created_by_group="1").count() == 1
