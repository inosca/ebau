from unittest.mock import MagicMock

import pytest
from alexandria.core import models as alexandria_models
from django.core.files.base import ContentFile

from camac.alexandria_migration.domain_logic.annotate_documents import (
    AnnotateDocumentsMigrator,
)
from camac.alexandria_migration.utils import UploadState


@pytest.fixture
def mock_run():
    return MagicMock(pk=12345)


def test_upload_state_lifecycle(mock_run):
    state = UploadState(mock_run)
    assert "alexandria_migration_12345_uploads.log" in str(state.path)

    # Test add
    state.add("path/to/s3/file1.jpg")
    state.add("path/to/s3/file2.jpg")

    assert state.path.exists()

    # Test get_all
    paths = state.get_all()
    assert paths == ["path/to/s3/file1.jpg", "path/to/s3/file2.jpg"]

    # Test clear
    state.clear()
    assert not state.path.exists()


def test_upload_state_concurrency(mock_run):
    state = UploadState(mock_run)
    # Simulate multiple adds (flock is handled internally)
    for i in range(10):
        state.add(f"path/to/file_{i}.jpg")

    paths = state.get_all()
    assert len(paths) == 10
    state.clear()


@pytest.mark.django_db
def test_cleanup_orphans(mock_run, alexandria_s3_mock):
    # 1. Create a log file with some paths
    state = UploadState(mock_run)
    orphaned_path = "orphaned/file.jpg"
    saved_path = "saved/file.jpg"

    state.add(orphaned_path)
    state.add(saved_path)

    # 2. Upload both files to S3 mock
    storage = AnnotateDocumentsMigrator.get_storage()
    storage.save(orphaned_path, ContentFile(b"orphaned content"))
    storage.save(saved_path, ContentFile(b"saved content"))

    # 3. Create a DB entry for one of them
    doc = alexandria_models.Document.objects.create(title="Test Doc")
    alexandria_models.File.objects.create(
        document=doc, name="saved.jpg", content=saved_path, size=13
    )

    assert storage.exists(orphaned_path)
    assert storage.exists(saved_path)

    # 4. Run cleanup
    AnnotateDocumentsMigrator.cleanup_orphans()

    # 5. Verify orphaned is gone, saved is still there, and log is gone
    assert not storage.exists(orphaned_path)
    assert storage.exists(saved_path)
    assert not state.path.exists()
