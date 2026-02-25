import csv
import os
from dataclasses import asdict, dataclass, fields
from logging import getLogger
from pathlib import Path
from typing import List, Optional, Type

import boto3
from codetiming import Timer
from django.conf import settings

log = getLogger(__name__)

NULL_STRING = " - "


@dataclass
class ReportEntry:
    pass


class ReportWriter:  # pragma: no cover
    def __init__(
        self,
        report_filename: str,
        columns: Optional[List[str]] = None,
        report_entry_class: Optional[Type[ReportEntry]] = None,
    ):
        self.report_filename = report_filename
        self._columns = None
        if columns:
            self._columns = columns
        if report_entry_class:
            self._columns = [f.name for f in fields(report_entry_class)]

        config = settings.DOSSIER_IMPORT["S3"]
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=config["url"],
            aws_access_key_id=config["access_key"],
            aws_secret_access_key=config["secret_key"],
            verify=False,
        )
        self.source_bucket = config["source_bucket"]

    def _upload_to_storage(self, filepath: Path):
        from camac.dossier_import.config.kt_ag_sap_migration.task_dispatcher import (
            is_disabled_docs_migration,
        )

        if is_disabled_docs_migration():
            return

        abs_path = filepath.resolve()
        message = f"Upload {abs_path} to {self.source_bucket}: {{:.4f}}seconds"
        with Timer(name="report_upload", text=message, logger=log.info):
            with open(abs_path, "rb") as f:
                self.s3_client.upload_fileobj(
                    f, self.source_bucket, str(abs_path).lstrip("/")
                )

    def _add_report_row(self, row):
        row = [str(r) if r is not None else "" for r in row]
        with open(self.report_filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)
        self._upload_to_storage(self.report_filepath)

    def add_report_entry(self, entry: ReportEntry):
        self._add_report_dict(asdict(entry))

    def write_raw(self, data: str):
        print(f"write_raw to {self.report_filepath}:")
        with open(self.report_filepath, "a", newline="", encoding="utf-8") as f:
            f.write(data)
        self._upload_to_storage(self.report_filepath)

    def _add_report_dict(self, d):
        with open(self.report_filepath, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, self._columns)
            writer.writerow(d)
        self._upload_to_storage(self.report_filepath)

    def _create_report(self):
        self.report_filepath.parent.mkdir(parents=True, exist_ok=True)

        if os.path.exists(self.report_filepath):
            os.remove(self.report_filepath)

        if self._columns:
            with open(self.report_filepath, "a", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, self._columns)
                writer.writeheader()

    def init_reports(self, segment_name: str, start_time: str, report_type: str):
        BASE_DIR = Path(settings.DOSSIER_IMPORT["MIGRATION_REPORTS_DIR"])
        self.init_report_at(BASE_DIR / start_time / segment_name / report_type)

    def init_report_at(self, report_dir_path: Path):
        self._report_dir = report_dir_path
        self.report_filepath: Path = self.get_report_file_path(self.report_filename)
        self._create_report()

    def get_report_file_path(self, filename):
        return self._report_dir / filename

    def create_diba_url(self, instance_id, view):
        if not instance_id:
            return NULL_STRING
        return f"{settings.INTERNAL_BASE_URL}/cases/{instance_id}/{view}"
