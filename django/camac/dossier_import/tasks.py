import logging
from typing import List

from celery import shared_task
from django.conf import settings

log = logging.getLogger(__name__)

MAX_RETRIES = 8 * 60  # retry for max. 8 hours if retry_interval is 1 minute

if settings.APPLICATION_NAME == "kt_ag":  # pragma: no cover
    from camac.dossier_import.config.kt_ag.documents.docs_exporter import (
        DocsExportResultCheck,
    )
    from camac.dossier_import.config.kt_ag.documents.docs_importer import (
        DocsImporter,
    )

    @shared_task(bind=True)
    def wait_for_docs_from_sap_to_s3_task(
        self,
        municipality: str,
        replication_id: str,
        dossier_ids: List[str],
        segment_name: str,
        start_time: str,
    ):
        log.info(
            f"wait_for_docs_from_sap_to_s3_task for {municipality} and dossier_ids: {dossier_ids}"
        )
        if not DocsExportResultCheck(
            municipality, replication_id, dossier_ids, segment_name, start_time
        ).finished_with_result_export():
            self.retry(
                countdown=settings.DOSSIER_IMPORT["EBAU_DOCUMENT_CLIENT"][
                    "check_replication_interval_seconds"
                ],
                max_retries=MAX_RETRIES,
            )
            return

    @shared_task(
        soft_time_limit=60 * 60 * 6
    )  # 6 hours timeout to complete with all dossiers from one municipality
    def import_s3_docs_task(
        municipality: str, dossier_ids: List[str], segment_name: str, start_time: str
    ):
        log.info(
            f"starting import_s3_docs_task for {municipality} and dossier_ids: {dossier_ids}"
        )
        DocsImporter(municipality, dossier_ids, segment_name, start_time).do_import()
