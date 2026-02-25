import uuid
from typing import List, Optional

from django.conf import settings

from camac.dossier_import.conftest import JSON_INPUT_DIR
from camac.dossier_import.tests.data.kt_ag.s3_test_files import MinioBackupRestore


class DevEbauDocumentClient:  # pragma: no cover
    def __init__(self):
        self._requests = {}

        self.minio_backup_restore = MinioBackupRestore(
            settings.DOSSIER_IMPORT["S3"]["url"],
            settings.DOSSIER_IMPORT["S3"]["access_key"],
            settings.DOSSIER_IMPORT["S3"]["secret_key"],
        )

    def initialize_infrastructure(self, clear_db: bool = False):
        if not self.minio_backup_restore.does_bucket_exist("migration-media"):
            self.minio_backup_restore.create_bucket("migration-media")
            self.minio_backup_restore.restore_bucket(
                "migration-media", "migration-media-staging.zip"
            )

    def replicate_data(
        self,
        purge: Optional[bool] = False,
        commune_id: Optional[List[int]] = None,
        request_id: Optional[List[str]] = None,
        status_commune: Optional[List[dict]] = None,
        status_canton: Optional[List[dict]] = None,
        submission_date_from: Optional[str] = None,
        submission_date_to: Optional[str] = None,
    ) -> str:
        self.initialize_infrastructure()
        s = str(uuid.uuid4())

        from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
            redis,
        )

        if redis:
            redis.sadd(s, *request_id)

        return s

    def get_replication_status(self, replication_id: str):
        from datetime import datetime

        from camac.dossier_import.config.kt_ag_sap_migration.documents.ebau_document_client import (
            ReplicationStatus,
        )

        ts = int(datetime.now().timestamp())
        completed = ts % 2 == 0
        print(f"fake replication status from {ts}: {completed}")
        return ReplicationStatus.COMPLETED if completed else ReplicationStatus.RUNNING

    def is_any_replication_running(self) -> bool:
        return False

    def download_replication_csv_log(self, replication_id: str) -> str:
        from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
            redis,
        )

        if not redis:
            return "created by mock implementation"

        id = next(iter(redis.smembers(replication_id)), None)
        if not id:
            return "created by mock implementation"

        for subdir in JSON_INPUT_DIR.iterdir():
            if subdir.is_dir() and (subdir / f"{id}.json").exists():
                csv_path = subdir / "export.csv"
                try:
                    with open(csv_path, "r") as f:
                        return f.read()
                except Exception as e:
                    print(str(e))

        return "created by mock implementation"
