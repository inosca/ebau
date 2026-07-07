import pytest
from alexandria.storages.backends.s3 import SsecGlobalS3Storage

from camac.alexandria_migration.domain_logic.duplicate_documents import (
    DuplicateDocumentsMigrator,
)


@pytest.mark.parametrize("encryption_enabled", [True, False])
def test_copy_task(
    # fixtures
    mocker,
    settings,
    # parametrization
    encryption_enabled,
):
    """Ensure file copying correctly deals with SSEC."""
    settings.ALEXANDRIA_ENABLE_AT_REST_ENCRYPTION = encryption_enabled

    if encryption_enabled:
        settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET = "test-secret"
        settings.ALEXANDRIA_SSEC_ALGORITHM = "AES256"
        storage = mocker.Mock(spec=SsecGlobalS3Storage)
    else:
        storage = mocker.Mock()

    storage.bucket.name = "test-bucket"

    file_to_copy = mocker.Mock()
    file_to_copy.storage = storage
    file_to_copy.name = "source-key"

    to_name = "target-key"

    DuplicateDocumentsMigrator._copy_task(file_to_copy, to_name)

    expected_copy_args = {
        "CopySource": {
            "Bucket": "test-bucket",
            "Key": "source-key",
        },
        "Bucket": "test-bucket",
        "Key": "target-key",
    }

    if encryption_enabled:
        expected_copy_args.update(
            {
                "CopySourceSSECustomerKey": "test-secret",
                "CopySourceSSECustomerAlgorithm": settings.ALEXANDRIA_SSEC_ALGORITHM,
                "SSECustomerKey": "test-secret",
                "SSECustomerAlgorithm": settings.ALEXANDRIA_SSEC_ALGORITHM,
            }
        )

    storage.bucket.meta.client.copy_object.assert_called_once_with(**expected_copy_args)
