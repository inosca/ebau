from concurrent.futures import ThreadPoolExecutor
from copy import deepcopy
from dataclasses import dataclass, field

from alexandria.core.models import Document, File, make_uuid
from alexandria.storages.backends.s3 import SsecGlobalS3Storage
from django.conf import settings
from django.db import transaction
from django.db.models import Prefetch

from camac.alexandria_migration.domain_logic.base import BaseMigrator, disable_auto_now
from camac.alexandria_migration.models import DocumentMark, MigrationLog
from camac.alexandria_migration.utils import get_available_categories
from camac.instance.models import InstanceAlexandriaDocument


@dataclass
class DuplicateDocumentsMigrator(BaseMigrator):
    documents: list[Document] = field(default_factory=list)
    document_marks: list[DocumentMark] = field(default_factory=list)
    files: list[File] = field(default_factory=list)
    instance_documents: list[InstanceAlexandriaDocument] = field(default_factory=list)
    copy_paths: list[tuple[str, str]] = field(default_factory=list)

    def process(self) -> None:
        documents = Document.objects.filter(
            instance_document__instance_id__in=self.instance_ids,
            metainfo__has_key="duplicate-to",
        ).prefetch_related(
            Prefetch("files", to_attr="_files"),
            Prefetch("marks", to_attr="_marks"),
        )

        for document in documents:
            self.copy_document(document)

        self.logs.extend(
            [
                MigrationLog(
                    type=MigrationLog.Type.INSTANCE_DOCUMENTS_DUPLICATED,
                    run=self.run,
                    instance_id=instance_id,
                )
                for instance_id in self.instance_ids
            ]
        )

        with transaction.atomic(), disable_auto_now(Document, File):
            with ThreadPoolExecutor(max_workers=32) as executor:
                for file, new_path in self.copy_paths:
                    executor.submit(self._copy_task, file, new_path)

            Document.objects.bulk_create(self.documents)
            DocumentMark.objects.bulk_create(self.document_marks)
            File.objects.bulk_create(self.files)
            InstanceAlexandriaDocument.objects.bulk_create(self.instance_documents)
            MigrationLog.objects.bulk_create(self.logs)

    def copy_document(self, document: Document):
        assert len(document._files) == 1, (
            "Editable (versioned) document found in multiple categories. This should not happen"
        )

        instance_id = document.metainfo["camac-instance-id"]

        for category in document.metainfo["duplicate-to"]:
            new_document = deepcopy(document)
            new_document.pk = make_uuid()
            new_document.category = get_available_categories()[category]
            new_document.metainfo.pop("duplicate-to", None)
            new_document.metainfo["duplicated-from"] = str(document.pk)

            self.copy_files_of_document(document, new_document)

            self.documents.append(new_document)
            self.document_marks.extend(
                [
                    DocumentMark(document=new_document, mark=mark)
                    for mark in document._marks
                ]
            )
            self.instance_documents.append(
                InstanceAlexandriaDocument(
                    instance_id=instance_id,
                    document_id=new_document.pk,
                )
            )

            self.logs.append(
                MigrationLog(
                    type=MigrationLog.Type.DOCUMENT_DUPLICATED,
                    run=self.run,
                    instance_id=instance_id,
                    source_document=document,
                    target_document=new_document,
                )
            )

    @staticmethod
    def _copy_task(file_to_copy, to_name):
        """Copy file to new path."""

        storage = file_to_copy.storage
        copy_args = {
            "CopySource": {
                "Bucket": storage.bucket.name,
                "Key": file_to_copy.name,
            },
            "Bucket": storage.bucket.name,
            "Key": to_name,
        }
        if isinstance(storage, SsecGlobalS3Storage):
            copy_args["CopySourceSSECustomerKey"] = (
                settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET
            )
            copy_args["CopySourceSSECustomerAlgorithm"] = (
                settings.ALEXANDRIA_SSEC_ALGORITHM
            )
            copy_args["SSECustomerKey"] = settings.ALEXANDRIA_S3_STORAGE_SSEC_SECRET
            copy_args["SSECustomerAlgorithm"] = settings.ALEXANDRIA_SSEC_ALGORITHM

        storage.bucket.meta.client.copy_object(**copy_args)

    def copy_files_of_document(self, document, new_document):
        for old_file in document._files:
            old_filename = old_file.content
            new_file_pk = make_uuid()
            new_filename = f"{new_file_pk}_{old_file.name}"

            new_file = deepcopy(old_file)
            new_file.pk = new_file_pk
            new_file.document = new_document
            new_file.content = new_filename

            self.files.append(new_file)
            self.copy_paths.append((old_filename, new_filename))
