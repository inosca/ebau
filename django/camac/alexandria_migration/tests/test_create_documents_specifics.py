import pytest
from alexandria.core.models import Category, Mark

from camac.alexandria_migration.domain_logic.create_documents import (
    CreateDocumentsMigrator,
)
from camac.alexandria_migration.models import MigrationRun
from camac.document.models import Attachment, AttachmentSection


@pytest.fixture
def migrator(db):
    run = MigrationRun.objects.create(command=MigrationRun.Command.CREATE_DOCUMENTS)
    return CreateDocumentsMigrator(run=run, instance_ids=[])


@pytest.mark.django_db
def test_attachment_to_document_fallback_category(migrator, mocker, settings):
    """Test that fallback category is used when no sections are present."""
    settings.ALEXANDRIA_MIGRATION.fallback_category = "fallback-slug"
    fallback_cat = Category.objects.create(pk="fallback-slug", name="Fallback")

    # Use an actual attachment object
    attachment = Attachment(
        user_id=1,
        service_id=None,
        context={},
        name="test.pdf",
        instance_id=123,
        uuid="00000000-0000-0000-0000-000000000001",
        date="2023-01-01T00:00:00Z",
        path="path/to/file",
        mime_type="application/pdf",
        size=100,
        attachment_id=1,
        question=None,
    )
    attachment._sections = []
    attachment._versions = []

    migrator.attachment_to_document(attachment)

    assert len(migrator.documents) == 1
    assert migrator.documents[0].category == fallback_cat
    assert migrator.documents[0].title == "test.pdf"
    assert migrator.documents[0].metainfo == {"camac-instance-id": 123}


@pytest.mark.django_db
def test_attachment_to_document_with_section(migrator, mocker, settings):
    """
    Test that target category from mapping is used when a section is present.

    Also check that document marks are correctly extracted.
    """
    settings.ALEXANDRIA_MIGRATION.category_mapping = {42: "target-slug"}
    settings.ALEXANDRIA_MIGRATION.context_mark_mapping = {"isDecision": "decision-slug"}
    target_cat = Category.objects.create(pk="target-slug", name="Target")
    decision_mark = Mark.objects.create(pk="decision-slug", name="Decision")

    section = AttachmentSection(pk=42, name="Section")
    attachment = Attachment(
        user_id=1,
        service_id=None,
        context={"displayName": "Custom Title", "isDecision": True},
        name="test.pdf",
        instance_id=123,
        uuid="00000000-0000-0000-0000-000000000002",
        date="2023-01-01T00:00:00Z",
        path="path/to/file",
        mime_type="application/pdf",
        size=100,
        attachment_id=2,
        question=None,
    )
    attachment._sections = [section]
    attachment._versions = []

    migrator.attachment_to_document(attachment)

    assert len(migrator.documents) == 1
    assert migrator.documents[0].category == target_cat
    assert migrator.documents[0].title == "Custom Title"
    assert len(migrator.document_marks) == 1
    assert migrator.document_marks[0].mark == decision_mark


@pytest.mark.django_db
def test_attachment_to_document_with_multiple_sections(migrator, mocker, settings):
    """Test that first section determines category and others go to metainfo."""
    settings.ALEXANDRIA_MIGRATION.category_mapping = {
        42: "target-slug",
        43: "other-slug",
    }
    target_cat = Category.objects.create(pk="target-slug", name="Target")
    Category.objects.create(pk="other-slug", name="Other")

    section1 = AttachmentSection(pk=42, name="Section 1")
    section2 = AttachmentSection(pk=43, name="Section 2")

    attachment = Attachment(
        user_id=1,
        service_id=None,
        context={},
        name="test.pdf",
        instance_id=123,
        uuid="00000000-0000-0000-0000-000000000003",
        date="2023-01-01T00:00:00Z",
        path="path/to/file",
        mime_type="application/pdf",
        size=100,
        attachment_id=3,
        question=None,
    )
    attachment._sections = [section1, section2]
    attachment._versions = []

    migrator.attachment_to_document(attachment)

    assert len(migrator.documents) == 1
    assert migrator.documents[0].category == target_cat
    assert migrator.documents[0].metainfo["duplicate-to"] == ["other-slug"]
