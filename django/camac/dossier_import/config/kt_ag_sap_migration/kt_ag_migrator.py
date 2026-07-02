import os
import shutil
import zipfile
from logging import INFO, WARNING, getLogger
from typing import TYPE_CHECKING, Callable, List, Optional

from alexandria.core.models import Category
from codetiming import Timer
from django.conf import settings
from django.db import close_old_connections, connection, transaction

from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_import_report_writer import (
    DossierImportReportWriter,
)
from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_loader import (
    KtAargauDossierLoader,
)
from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
    cleanup_redis_migration_keys,
    start_export_docs_from_sap_to_s3_and_wait_task,
    start_import_task,
    wait_for_docs_imports_to_finish,
)
from camac.dossier_import.domain_logic import perform_import
from camac.dossier_import.dossier_classes import Dossier
from camac.dossier_import.messages import DossierSummary
from camac.dossier_import.models import DossierImport
from camac.user.models import Group, User, UserGroup

if TYPE_CHECKING:
    from camac.dossier_import.config.kt_ag_sap_migration.dossier_import.dossier_classes import (
        KtAargauDossier,
    )

IMPORT_SETTINGS = settings.DOSSIER_IMPORT
SAP_SETTINGS = IMPORT_SETTINGS["SAP_ACCESS"]

log = getLogger(__name__)


class KtAargauMigrator:
    def __init__(
        self,
        source_path: Optional[str],
        start_time: Optional[str],
        dossier: Optional[str],
        skip_existing: bool,
        rm_file: bool,
        quiet: bool = False,
        skip_dossier_import: bool = False,
        skip_document_import: bool = False,
        skip_document_export: bool = False,
        only_municipalities: Optional[List[str]] = None,
        only_dossiers: Optional[List[str]] = None,
    ):
        self.source_path = source_path
        self.start_time = start_time
        self.dossier = dossier
        self.skip_existing = skip_existing
        self.rm_file = rm_file
        self.quiet = quiet
        self.skip_dossier_import = skip_dossier_import
        self.skip_document_import = skip_document_import
        self.skip_document_export = skip_document_export
        self.only_municipalities = only_municipalities
        self.only_dossiers = only_dossiers

    @classmethod
    def prepare_user_and_group(cls):
        user_name = IMPORT_SETTINGS["USER"]
        group_name = IMPORT_SETTINGS["GROUP"]

        group = Group.objects.get(trans__language="de", trans__name=group_name)

        if not User.objects.filter(username=user_name).exists():
            cls._create_user(user_name=user_name, group=group)

        user = User.objects.get(username=user_name)
        return user, group

    @classmethod
    @transaction.atomic
    def _create_user(cls, user_name, group):
        user = User.objects.create(
            username=user_name,
            name=user_name,
            surname="User",
            email=f"{user_name}@diba.ag.ch",
        )
        UserGroup.objects.create(user=user, group=group, default_group=1)
        return user

    def migrate(self):
        self._disable_distribution_notification()
        try:
            self._ensure_db_connection()
            self._prepare_categories()
            self.user, self.group = self.prepare_user_and_group()

            if self.dossier:  # pragma: no cover
                log.info(f"Importing from '{self.dossier}'")
                self.dossier_import_reporter = DossierImportReportWriter(
                    "result.csv", "result-details.json"
                )
                self.dossier_import_reporter.init_reports(
                    "single_file", self.start_time, "dossier_import"
                )
                self._import_dossier(self.dossier)
            else:
                segment_name = "unknown"
                if self.source_path:
                    self._unzip_source_if_needed()
                    SAP_SETTINGS["json_target_dir"] = self.source_path
                    segment_name = os.path.basename(self.source_path)

                log.info(f"Importing all from {SAP_SETTINGS['json_target_dir']}")

                loader = KtAargauDossierLoader()

                cleanup_redis_migration_keys()

                all_municipalities = []
                for (
                    municipality,
                    municipality_id_str,
                    _,
                ) in loader.list_dossier_count_per_municipality():
                    if (
                        self.only_municipalities
                        and municipality not in self.only_municipalities
                    ):  # pragma: no cover
                        log.info(
                            f"Skipping {municipality} because it is not in the list of municipalities to import."
                        )
                        continue

                    all_municipalities.append(municipality)

                    dossier_ids = loader.get_dossier_ids(municipality)

                    municipality_id = int(municipality_id_str)
                    if self.only_dossiers:  # pragma: no cover
                        dossier_ids = list(set(dossier_ids) & set(self.only_dossiers))
                        log.info(
                            "Reduced list of dossiers to intersection with only_dossiers."
                        )

                    if dossier_ids:
                        self._migrate_municipality(
                            segment_name,
                            municipality,
                            municipality_id,
                            dossier_ids,
                            len(dossier_ids),
                        )
                    else:  # pragma: no cover
                        log.warning(
                            f"No dossiers found for {municipality}/{municipality_id}. Skipping ..."
                        )
                        all_municipalities.remove(municipality)

                self._close_db_connection_before_idle_time()
                if not self.skip_document_import:
                    wait_for_docs_imports_to_finish(all_municipalities)
                    log.info("Done: waiting for all document imports to finish.")
                else:  # pragma: no cover
                    log.info("Not waiting for skipped document imports.")
        finally:
            self._restore_categories()
            self._restore_restore_distribution_notification()
            cleanup_redis_migration_keys()

    def _migrate_municipality(
        self, segment_name, municipality, municipality_id, dossier_ids, count
    ):
        log.info(f"Importing {municipality}/{municipality_id} with {dossier_ids}")
        self.dossier_import_reporter = DossierImportReportWriter(
            f"{municipality}.csv", f"{municipality}-details.json"
        )
        self.dossier_import_reporter.init_reports(
            segment_name, self.start_time, "dossier_import"
        )

        if not self.skip_document_export:
            wait_for_async_check_SAP_export: Callable = (
                start_export_docs_from_sap_to_s3_and_wait_task(
                    municipality,
                    municipality_id,
                    dossier_ids,
                    segment_name,
                    self.start_time,
                )
            )
        else:  # pragma: no cover
            log.info("Skipping any document export.")

        if not self.skip_dossier_import:
            self._import_dossier(municipality, municipality, count, dossier_ids)
        self._close_db_connection_before_idle_time()

        if not self.skip_document_export:
            # wait for SAP export to finish because only a single export job must run at a time, if needed
            wait_for_async_check_SAP_export()
            log.info(
                f"Done: waiting for SAP export of {municipality}/{municipality_id}"
            )
        else:  # pragma: no cover
            log.info("Not waiting for skipped document export.")

        if not self.skip_document_import:
            start_import_task(municipality, dossier_ids, segment_name, self.start_time)
        else:  # pragma: no cover
            log.info("Skipping any document import.")

    MIGRATION_MIME_TYPES = {
        "application/vnd.ms-outlook",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/octet-stream",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "application/msword",
        "application/zip",
        "application/vnd.ms-office",
        "application/x-ole-storage",
        "text/plain",
        "text/html",
        "image/heic",
        "text/rtf",
        "image/webp",
    }

    @transaction.atomic
    def _prepare_categories(self):
        self._org_mimetypes = {}
        for slug in [
            "alle-beteiligten",
            "beteiligte-behörden",
            "alle-kanton",
            "intern",
            "beilagen-zum-gesuch",
        ]:
            category = Category.objects.filter(slug=slug).first()
            if category:
                self._org_mimetypes[slug] = category.allowed_mime_types
                category.allowed_mime_types = list(
                    set(category.allowed_mime_types) | self.MIGRATION_MIME_TYPES
                )
                category.save()

    def _restore_categories(self):
        self._ensure_db_connection()
        for slug, org_mime_types in self._org_mimetypes.items():
            category = Category.objects.filter(slug=slug).first()
            category.allowed_mime_types = org_mime_types
            category.save()

    def _disable_distribution_notification(self):
        if self.quiet:  # pragma: no cover
            self.original_notification_settings = settings.DISTRIBUTION["NOTIFICATIONS"]
            settings.DISTRIBUTION["NOTIFICATIONS"] = {}

    def _restore_restore_distribution_notification(self):
        if self.quiet:  # pragma: no cover
            settings.DISTRIBUTION["NOTIFICATIONS"] = self.original_notification_settings

    def _ensure_db_connection(self):
        close_old_connections()
        connection.ensure_connection()

    def _close_db_connection_before_idle_time(self):
        connection.close()

    def _import_dossier(
        self,
        source_path,
        municipality="unknown",
        total_count="unknown",
        only_dossiers=None,
    ):
        log.info(f"Migrating '{municipality}' with {total_count} dossiers ...")
        self._ensure_db_connection()
        self.current_total_count = total_count
        self.currently_imported_count = 1

        try:
            dossier_import = DossierImport.objects.create(
                user_id=self.user.pk,
                group_id=self.group.pk,
                dossier_loader_type="Kanton Aargau SAP",
                source_file=source_path,
            )
            dossier_import.messages["target_count"] = total_count
            dossier_import.messages["municipality"] = municipality
            dossier_import.save()

            KtAargauDossierLoader.set_dossier_filter(self.only_dossiers)
            perform_import(dossier_import, self.skip_existing, self._dossier_imported)
            KtAargauDossierLoader.set_dossier_filter(None)
            self.dossier_import_reporter.report_municipality_result(dossier_import)

        except Exception as e:  # pragma: no cover
            log.exception(f"Error importing '{municipality}': {e}")

    def _unzip_source_if_needed(self):
        if self.source_path.lower().endswith(".zip"):
            zip_path = self.source_path
            base_dir = os.path.splitext(zip_path)[0]

            if os.path.exists(base_dir):  # pragma: no cover
                shutil.rmtree(base_dir)
            os.makedirs(base_dir)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(base_dir)

            expected_file = os.path.join(base_dir, "municipalities_counts.json")
            if not os.path.isfile(expected_file):  # pragma: no cover
                message = f"Cannot find 'municipalities_counts.json' toplevel in extracted {base_dir}. Aborting."
                log.error(message)
                raise ValueError(message)

            self.source_path = base_dir

    def _dossier_imported(self, dossier: Dossier, message: DossierSummary):
        dossier: KtAargauDossier
        self.dossier_import_reporter.add_report_row_for(
            dossier, message, self.currently_imported_count, self.current_total_count
        )

        log.log(
            self._level_from_message_status(message),
            f"{dossier.city}: imported {self.currently_imported_count} / {self.current_total_count} dossiers:\n"
            + f"\t{str(message)}\n"
            + f"\t{str({name: durations[-1] for name, durations in Timer.timers._timings.items()})}",
        )

        self.currently_imported_count += 1

        if message.status == "success" and self.rm_file and dossier.dossier_file_path:
            os.remove(dossier.dossier_file_path)  # pragma: no cover

    def _level_from_message_status(self, message):  # pragma: no cover
        if message.status == "success":
            level = INFO
        else:
            level = WARNING
        return level
