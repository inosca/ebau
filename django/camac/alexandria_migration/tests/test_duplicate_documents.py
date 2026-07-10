import pytest
from django.core.exceptions import ImproperlyConfigured

from camac.alexandria_migration.domain_logic.duplicate_documents import (
    DuplicateDocumentsMigrator,
)


def test_copy_task(mocker):
    """Ensure file copying correctly works."""
    storage = mocker.Mock()
    storage.bucket.name = "test-bucket"

    source_key = "source-key"
    to_name = "target-key"

    DuplicateDocumentsMigrator._copy_task(storage, source_key, to_name)

    expected_copy_args = {
        "CopySource": {
            "Bucket": "test-bucket",
            "Key": "source-key",
        },
        "Bucket": "test-bucket",
        "Key": "target-key",
    }

    storage.bucket.meta.client.copy_object.assert_called_once_with(**expected_copy_args)


def test_process_aborts_on_encryption(settings):
    """Ensure migration aborts if encryption is enabled."""
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = True
    migrator = DuplicateDocumentsMigrator(instance_ids=[1], run=None)

    with pytest.raises(
        ImproperlyConfigured,
        match="does not support ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION=True",
    ):
        migrator.process()
