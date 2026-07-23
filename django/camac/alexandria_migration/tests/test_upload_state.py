import random
from unittest.mock import MagicMock, patch

import pytest
from alexandria.core import models as alexandria_models
from django.core.files.base import ContentFile

from camac.alexandria_migration.domain_logic.annotate_documents import (
    AnnotateDocumentsMigrator,
)
from camac.alexandria_migration.utils import UploadState


@pytest.fixture
def mock_run():
    return MagicMock(pk=random.randint(1, 1000000))


@pytest.fixture(autouse=True)
def mock_temp_dir(tmp_path):
    with patch("tempfile.gettempdir", return_value=str(tmp_path)):
        yield tmp_path


def test_upload_state_lifecycle(mock_run):
    state = UploadState(mock_run)
    assert f"alexandria_migration_{mock_run.pk}_uploads.log" in str(state.path)

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
def test_cleanup_orphans_with_orphans(mock_run, alexandria_s3_mock):
    """Test cleanup when orphans actually exist."""
    state = UploadState(mock_run)
    orphaned_path = "orphaned/file.jpg"
    saved_path = "saved/file.jpg"

    state.add(orphaned_path)
    state.add(saved_path)

    storage = AnnotateDocumentsMigrator.get_storage()
    storage.save(orphaned_path, ContentFile(b"orphaned content"))
    storage.save(saved_path, ContentFile(b"saved content"))

    doc = alexandria_models.Document.objects.create(title="Test Doc")
    alexandria_models.File.objects.create(
        document=doc, name="saved.jpg", content=saved_path, size=13
    )

    assert storage.exists(orphaned_path)
    assert storage.exists(saved_path)

    AnnotateDocumentsMigrator.cleanup_orphans()

    assert not storage.exists(orphaned_path)
    assert storage.exists(saved_path)
    assert not state.path.exists()


@pytest.mark.django_db
def test_cleanup_orphans_no_orphans(mock_run, alexandria_s3_mock):
    """Test cleanup when no orphans exist (all files in log are in DB)."""
    state = UploadState(mock_run)
    saved_path = "saved/file.jpg"

    state.add(saved_path)

    storage = AnnotateDocumentsMigrator.get_storage()
    storage.save(saved_path, ContentFile(b"saved content"))

    doc = alexandria_models.Document.objects.create(title="Test Doc")
    alexandria_models.File.objects.create(
        document=doc, name="saved.jpg", content=saved_path, size=13
    )

    assert storage.exists(saved_path)

    AnnotateDocumentsMigrator.cleanup_orphans()

    # File should still be there because it's in the DB
    assert storage.exists(saved_path)
    # But the log file should be cleaned up
    assert not state.path.exists()


def test_cleanup_orphans_no_logs():
    """Test cleanup when no log files exist at all."""
    # Ensure no logs exist (mock_temp_dir fixture handles isolation)
    assert not UploadState.get_all_log_files()

    # Should not crash and should do nothing
    AnnotateDocumentsMigrator.cleanup_orphans()
