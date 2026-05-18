import hashlib
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass, field
from mimetypes import guess_extension
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from alexandria.core.models import Document, File
from alexandria.core.tika import TikaClient
from alexandria.storages.backends.s3 import S3Storage
from django import db
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.files.base import ContentFile
from django.db import transaction
from django.db.models import Prefetch, Value
from django.utils import timezone
from preview_generator.manager import PreviewManager

from camac.alexandria_migration.domain_logic.base import BaseMigrator, disable_auto_now
from camac.alexandria_migration.models import DocumentMark, MigrationLog
from camac.instance.models import InstanceAlexandriaDocument


@dataclass
class AnnotateDocumentsMigrator(BaseMigrator):
    documents: list[Document] = field(default_factory=list)
    document_marks: list[DocumentMark] = field(default_factory=list)
    update_files: list[File] = field(default_factory=list)
    create_files: list[File] = field(default_factory=list)
    instance_documents: list[InstanceAlexandriaDocument] = field(default_factory=list)
    copy_paths: list[tuple[str, str]] = field(default_factory=list)
    no_parallel: Optional[bool] = field(default=False)

    def process(self) -> None:
        documents = Document.objects.filter(
            instance_document__instance_id__in=self.instance_ids
        ).prefetch_related(
            Prefetch(
                "files",
                queryset=File.objects.filter(variant=File.Variant.ORIGINAL)
                .filter(renderings__isnull=True)
                .order_by("-created_at")[:1],
                to_attr="_most_recent_file",
            ),
            Prefetch(
                "files",
                queryset=File.objects.filter(variant=File.Variant.THUMBNAIL).order_by(
                    "-created_at"
                )[:1],
                to_attr="_most_recent_thumbnail",
            ),
            Prefetch(
                "files",
                queryset=File.objects.filter(variant=File.Variant.ORIGINAL),
                to_attr="_originals",
            ),
            "instance_document",
        )

        with transaction.atomic(), disable_auto_now(Document, File):
            # We use a process pool executor here. Also not passing max_workers
            # as we're CPU-bound here and it doesn't make sense to use more than
            # we have

            if self.no_parallel:
                for document in documents:
                    self._record_task_result(
                        AnnotateDocumentsMigrator.annotate_document(document)
                    )

            else:
                # Parallel mode - this should be default
                # TODO: refactor so it's not two full loops - if possible. Not
                # important enough to spend too much time on
                with ProcessPoolExecutor() as executor:
                    for document in documents:
                        future = executor.submit(
                            AnnotateDocumentsMigrator.annotate_document,
                            document,
                        )
                        # Process Pool executor can't update `self`, as it's in a
                        # subprocess, so we do it via return values instead
                        future.add_done_callback(self._record_task_result)

            self.logs.extend(
                [
                    MigrationLog(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_ANNOTATED,
                        run=self.run,
                        instance_id=instance_id,
                    )
                    for instance_id in self.instance_ids
                ]
            )

            File.objects.bulk_create(self.create_files)
            File.objects.bulk_update(
                self.update_files,
                fields=["content_vector", "content_text", "checksum", "language"],
            )
            MigrationLog.objects.bulk_create(self.logs)

    def _record_task_result(self, future):
        # Can be called with future or direct result
        result = future if isinstance(future, list) else future.result()

        for file_res in result:
            if err := file_res.get("error"):
                # TODO fix and ensure the result is loged properly. But for now,
                # stdout is fine
                print(err)
                continue

            for log in file_res["logs"]:
                # the run is not recorded to avoid passing it along
                # across multiple functions
                log.run = self.run
                self.logs.append(log)
            if upd := file_res["file_updated"]:
                self.update_files.append(upd)
            if cre := file_res["file_created"]:
                self.create_files.append(cre)

    @classmethod
    def _get_file_content(cls, file):
        if not file:
            # wat
            # TODO proper error logging / debugging in parallel mode
            print("NO file for getting content, WAT")
        assert isinstance(file.content.storage, S3Storage), (
            f"Misconfigured Storage backend? {file.content.storage} is not S3"
        )
        with file.content.open("rb") as fh:
            return fh.read()

    @classmethod
    def annotate_document(cls, document):
        """Annotate the given document.

        Return a list of dicts, each with their file-specific result data:
        - logs contains a list of log entries
        - file_updated: None or the updated file object
        - file_created: None or the created thumbnail
        """

        # We only make thumbnails for the most recent files. Those
        # are the ones being used, the rest is not really needed by anyone
        if document._most_recent_file:
            most_recent = document._most_recent_file[0]
        else:
            most_recent = None
            # If the document has no "most recent file", it could be that it's already
            # filtered out because there is a thumbnail. Therefore, it's only a problem
            # if there is *no* thumbnail on this document.
            #
            # But in any case, we don't process the file if there's no
            # most-recent original to be processed.
            if not document._most_recent_thumbnail:
                # There's a no thumbnail, so there's a file that has no originals
                # and no thumbnails - which should not happen in the migration
                # TODO deal with it in some more "practicable" way
                print(f"Document has no original file? {document}")

        res = [
            cls.annotate_file(
                file,
                instance_id=document.instance_document.instance_id,
                # if there's no most-recent file, but there's others, something's weird
                # TODO: We should check for each step whether it's already
                # done, and only do it (and pull the file from storage!)
                # if it's not done yet
                is_most_recent=most_recent and (file.pk == most_recent.pk),
            )
            for file in document._originals
        ]

        return res

    @classmethod
    def annotate_file(cls, file, instance_id, is_most_recent):
        """Annotate the given file.

        This includes setting the checksum, fulltext index, and, for
        the most recent file, also generates a thumbnail.

        Return a dict with result data:
        - logs contains a list of log entries
        - file_updated: None or the updated file object
        - file_created: None or the created thumbnail,
        - 'error': a message (if this is given, the other keys won't be returned)
        """
        # The implementation of the functions is copied form Alexandria itself,
        # but modified such that we only need to fetch each file's content once,
        # and only have to update each file's DB entry once as well.

        try:
            content = cls._get_file_content(file)
        except FileNotFoundError as exc:
            print(f"Err: Migrated original file not found in S3: {exc}")
            # TODO Deal with this - S3 doesn't have our migrated file,
            # this sounds bad
            #
            # return here, as FTS and thumbnail will definitely also not work here
            return {"error": str(exc)}

        if not content:
            return {
                "error": f"could not get content for file {file.pk} (name:{file.name})"
            }

        results = {
            "logs": [],
            "file_updated": None,
            "file_created": None,
        }

        did_checksum = cls._set_checksum(file, content)
        if did_checksum:
            results["logs"].append(
                MigrationLog(
                    run=None,
                    instance_id=instance_id,
                    target_document=file.document,
                    target_file=file,
                    type=MigrationLog.Type.ANNOTATED_CHECKSUM,
                )
            )

        did_content_vector = cls._set_content_vector(file, content)
        if did_content_vector:
            results["logs"].append(
                MigrationLog(
                    run=None,
                    instance_id=instance_id,
                    target_document=file.document,
                    target_file=file,
                    type=MigrationLog.Type.ANNOTATED_FULLTEXT_SEARCH,
                )
            )

        thumbnail = cls._make_thumbnail(file, instance_id, content)
        if thumbnail:
            results["logs"].append(
                MigrationLog(
                    run=None,
                    instance_id=instance_id,
                    target_document=file.document,
                    # TODO should target_file be the (original) file or the
                    # (new) thumbnail? or even both, extending the log model?
                    target_file=file,
                    type=MigrationLog.Type.ANNOTATED_THUMBNAIL,
                )
            )

        if did_content_vector or did_checksum or thumbnail:
            results["file_updated"] = file
        if thumbnail:
            results["file_created"] = thumbnail
        return results

    @classmethod
    def _make_thumbnail(cls, file, instance_id, content):
        """Generate thumbnail for the given file.

        Return the thumbnail File if done, None if not.
        """
        if (
            file.variant == File.Variant.ORIGINAL
            # TODO ensure this does not trigger a query
            and file.renderings.count() < 1
            and settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION
        ):
            return cls._create_thumbnail(file, content)
        return None

    @classmethod
    def _set_content_vector(cls, file, content):
        """Calculate content vector for fulltext search.

        Return True if calculation was done, False otherwise.
        """
        if (
            not settings.ALEXANDRIA_ENABLE_CONTENT_SEARCH
            or file.variant != File.Variant.ORIGINAL
            or file.content_vector
        ):
            # already done or not enabled - don't do anything
            return False

        parsed_content = TikaClient.get_content_from_buffer(content)
        # Note: Tika will complain for a couple of document types that it doesn't
        # understand. That's OK (For example, Zip archives are not supported)

        file_name = str(Path(file.name).stem)
        file_name_vector = SearchVector(Value(file_name), weight="D")
        document_name_vector = SearchVector(Value(file.document.title), weight="A")
        document_desc_vector = SearchVector(
            Value(file.document.description or ""), weight="B"
        )

        base_vector = file_name_vector + document_name_vector + document_desc_vector

        if not parsed_content:
            # Update only content_vector and content_text to avoid race conditions
            file.content_vector = base_vector
            return True

        language = TikaClient.get_language_from_content(parsed_content[:1000])

        config = settings.ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG.get(
            language, "simple"
        )
        text_content = parsed_content.strip()
        content_vector = base_vector + SearchVector(
            Value(text_content),
            config=config,
            weight="C",
        )

        file.content_vector = content_vector
        file.language = language
        file.content_text = text_content
        return True

    @classmethod
    def _set_checksum(cls, file, content):
        """Calculate checksum for the given file.

        Return True if done, False if not.
        """

        # We respect the settings as defined in Alexandria.
        if settings.ALEXANDRIA_ENABLE_CHECKSUM and not file.checksum:
            file.checksum = f"sha256:{hashlib.sha256(content).hexdigest()}"
            return True
        return False

    @classmethod
    def _create_thumbnail(cls, file, content):
        """Generate an Alexandria thumbnail file and return it.

        May return None if it wasn't possible
        """

        with NamedTemporaryFile() as tmp:
            temp_file = Path(tmp.name)
            manager = PreviewManager(str(temp_file.parent))
            with temp_file.open("wb") as f:
                f.write(content)

            extension = guess_extension(file.mime_type)
            preview_kwargs = {"file_ext": extension}
            if settings.ALEXANDRIA_THUMBNAIL_WIDTH:  # pragma: no cover
                preview_kwargs["width"] = settings.ALEXANDRIA_THUMBNAIL_WIDTH
            if settings.ALEXANDRIA_THUMBNAIL_HEIGHT:  # pragma: no cover
                preview_kwargs["height"] = settings.ALEXANDRIA_THUMBNAIL_HEIGHT
            try:
                path_to_preview_image = Path(
                    manager.get_jpeg_preview(str(temp_file), **preview_kwargs)
                )
            # thumbnail generation can throw many different exceptions, catch all
            except Exception:  # noqa: B902
                return None

        with path_to_preview_image.open("rb") as thumb:
            thumb_content = thumb.read()
            ret = File(
                name=f"{file.name}_preview.jpg",
                document=file.document,
                variant=File.Variant.THUMBNAIL.value,
                created_at=timezone.now(),
                modified_at=timezone.now(),
                original=file,
                encryption_status=file.encryption_status,
                content=ContentFile(thumb_content, name=f"{file.name}_preview.jpg"),
                mime_type="image/jpeg",
                size=len(thumb_content),
            )
            return ret
