import logging
from time import sleep
from typing import Callable, List, Set

from django.conf import settings
from redis import Redis

from camac.dossier_import.config.kt_ag_sap_migration.documents.docs_exporter import (
    DocsExporter,
)
from camac.dossier_import.config.kt_ag_sap_migration.documents.ebau_document_client import (
    create_ebau_document_client,
)
from camac.dossier_import.config.kt_ag_sap_migration.tasks import (
    import_s3_docs_task,
    wait_for_docs_from_sap_to_s3_task,
)

FINISHED_DOC_EXPORTS_SET = "finished_doc_exports"
FINISHED_DOC_IMPORTS_SET = "finished_doc_imports"

log = logging.getLogger(__name__)


def is_disabled_docs_migration():  # pragma: no cover
    if not settings.DOSSIER_IMPORT["DOCS_MIGRATION_ENABLED"]:
        log.info(
            "Skipping document migration as it is disabled by DOSSIER_IMPORT.DOCS_MIGRATION_ENABLED"
        )
        return True

    return False


if not is_disabled_docs_migration():  # pragma: no cover
    redis = Redis.from_url(settings.CELERY_BROKER_URL, decode_responses=True)


def _add_to_redis_set(setname: str, value: str):  # pragma: no cover
    redis.sadd(setname, value)


def _has_redis_set_value(setname, value):  # pragma: no cover
    return redis.sismember(setname, value)


def signal_doc_export_done(municipality: str):  # pragma: no cover
    if is_disabled_docs_migration():
        return
    _add_to_redis_set(FINISHED_DOC_EXPORTS_SET, municipality)


def signal_doc_import_done(municipality: str):  # pragma: no cover
    if is_disabled_docs_migration():
        return
    _add_to_redis_set(FINISHED_DOC_IMPORTS_SET, municipality)


def _wait_for_all_values_in_set(setname, values: List[str]):  # pragma: no cover
    """Block until all values are available in the set."""
    remaining: Set[str] = set(values)

    while remaining:
        existing = redis.smembers(setname)
        old_len = len(remaining)
        remaining.difference_update(existing)
        if remaining:
            if len(remaining) != old_len:
                log.info(
                    f"'{remaining}' still missing in '{setname}'. Continue waiting for 60 seconds."
                )
            sleep(60)

    return


def _wait_for_value_in_set(setname, value: str):  # pragma: no cover
    """Block until the value is available in the set."""
    while not _has_redis_set_value(setname, value):
        log.info(
            f"'{value}' still missing in '{setname}'. Continue waiting for 60 seconds."
        )
        sleep(60)


def wait_for_docs_imports_to_finish(municipalities: List[str]):  # pragma: no cover
    if is_disabled_docs_migration():
        return
    _wait_for_all_values_in_set(FINISHED_DOC_IMPORTS_SET, municipalities)


def cleanup_redis_migration_keys():  # pragma: no cover
    if is_disabled_docs_migration():
        return

    count = redis.delete(FINISHED_DOC_EXPORTS_SET, FINISHED_DOC_IMPORTS_SET)

    if count:
        log.info(f"Deleted {count} still existing redis migration keys")


def _wait_for_running_replications(municipality: str):  # pragma: no cover
    while create_ebau_document_client().is_any_replication_running():
        log.info(
            f"{municipality} export is waiting for another SAP document export to finish"
        )
        sleep(60)


def start_export_docs_from_sap_to_s3_and_wait_task(
    municipality: str,
    municipality_id: int,
    dossier_ids: List[str],
    segment_name: str,
    start_time: str,
) -> Callable:  # pragma: no cover
    if is_disabled_docs_migration():
        return lambda: None

    _wait_for_running_replications(municipality)

    log.info(
        f"starting export_docs_from_sap_to_s3_task for {municipality}, {municipality_id} and dossier_ids: {dossier_ids}"
    )
    try:
        docs_exporter = DocsExporter(
            municipality, municipality_id, dossier_ids, segment_name, start_time
        )
        docs_exporter.do_export()
    except Exception as e:
        log.error(
            f"Error starting SAP document export for {municipality}: {e}", exc_info=True
        )
        return lambda: None

    return lambda: _wait_for_value_in_set(FINISHED_DOC_EXPORTS_SET, municipality)


def start_wait_for_docs_from_sap_to_s3_task(
    municipality: str,
    replication_id: str,
    dossier_ids: List[str],
    segment_name: str,
    start_time: str,
):  # pragma: no cover
    if is_disabled_docs_migration():
        return

    # give the started replication some time to write the first status to the database
    sleep(10)

    wait_for_docs_from_sap_to_s3_task.delay(
        municipality, replication_id, dossier_ids, segment_name, start_time
    )


def start_import_task(
    municipality: str, dossier_ids: List[str], segment_name: str, start_time: str
):  # pragma: no cover
    if is_disabled_docs_migration():
        return

    import_s3_docs_task.delay(municipality, dossier_ids, segment_name, start_time)
