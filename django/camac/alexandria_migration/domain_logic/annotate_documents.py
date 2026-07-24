import hashlib
import logging
import os
import shutil
import tempfile
from concurrent.futures import Executor, Future, ProcessPoolExecutor
from dataclasses import dataclass, field
from mimetypes import guess_extension
from pathlib import Path
from tempfile import NamedTemporaryFile

import setproctitle
from alexandria.core.models import Document, File, make_uuid
from alexandria.core.tika import TikaClient
from alexandria.storages.backends.s3 import S3Storage
from django.conf import settings
from django.contrib.postgres.search import SearchVector
from django.core.files.base import ContentFile
from django.core.files.storage import storages
from django.db import connections, transaction
from django.db.models import Prefetch, Value
from django.utils import timezone
from preview_generator.manager import PreviewManager

from camac.alexandria_migration.domain_logic.base import BaseMigrator, disable_auto_now
from camac.alexandria_migration.models import DocumentMark, MigrationLog
from camac.alexandria_migration.utils import UploadState, timeout
from camac.instance.models import InstanceAlexandriaDocument


def _patch_thumbnail_logging():
    """Install logging filter for thumbnailer.

    We need this so we don't get the "missing a dependency" errors spammed on
    the terminal.
    """

    def _filter_missing_dependency(record):
        # return False to drop the record, True to let it through
        return "is missing a dependency" not in record.getMessage()

    # attach to preview_generator's logger itself (blocks before any handler sees it)
    # The logger name in preview_generator is "PreviewGenerator"
    logging.getLogger("PreviewGenerator").addFilter(_filter_missing_dependency)


_patch_thumbnail_logging()


class SynchronousExecutor(Executor):
    """Drop-in for ProcessPoolExecutor for sync operation.

    Used for testing / debugging (check --no-parallel commandline)
    """

    # TODO: We have ThreadPoolExecutor used in duplicate_documents, which
    # might benefit from this as well. Also, there's the GIS / OEREB clients
    # that may use this also

    def submit(self, fn, /, *args, **kwargs):
        future = Future()
        try:
            result = fn(*args, **kwargs)
            future.set_result(result)
        except Exception as exc:  # pragma: no cover
            future.set_exception(exc)
        return future

    def map(self, fn, *iterables, timeout=None, chunksize=1):  # pragma: no cover
        # Just for completeness of the API
        return list(map(fn, *iterables))

    def shutdown(self, wait=True, *, cancel_futures=False):
        pass


@dataclass
class AnnotateDocumentsMigrator(BaseMigrator):
    documents: list[Document] = field(default_factory=list)
    document_marks: list[DocumentMark] = field(default_factory=list)
    update_files: list[File] = field(default_factory=list)
    create_files: list[File] = field(default_factory=list)
    instance_documents: list[InstanceAlexandriaDocument] = field(default_factory=list)
    copy_paths: list[tuple[str, str]] = field(default_factory=list)
    no_parallel: bool = field(default=False)
    workers: int = field(default=0)
    failed: bool = field(default=False)

    _storage = None
    _preview_manager = None

    @classmethod
    def cleanup_orphans(cls):
        """Clean up orphaned uploads from previous aborted runs."""
        from alexandria.core.models import File as AlexandriaFile

        cls._storage = None
        cls._preview_manager = None

        # Also clear preview cache
        cache_path = os.path.join(tempfile.gettempdir(), "alexandria_preview_cache")
        if os.path.exists(cache_path):
            shutil.rmtree(cache_path, ignore_errors=True)

        log_files = UploadState.get_all_log_files()
        if not log_files:
            return

        print("Cleaning up any orphaned thumbnails from S3 ...", end="", flush=True)
        storage = cls.get_storage()
        total_cleaned = 0
        for log_path in log_files:
            with open(log_path) as f:
                paths = [line.strip() for line in f if line.strip()]

            for s3_path in paths:
                # Check if this path exists in File table
                if not AlexandriaFile.objects.filter(content=s3_path).exists():
                    # Check if it was maybe just created in this run?
                    # No, this is called at the very beginning of the command.
                    storage.delete(s3_path)
                    if total_cleaned % 20 == 0:
                        print(".", end="", flush=True)
                    total_cleaned += 1

            UploadState.delete_log_file(log_path)

        if total_cleaned > 0:
            print(f"\nCleaned up {total_cleaned} orphaned thumbnails")
        else:
            print("\nNothing to cleanup")

    @classmethod
    def get_storage(cls):
        if cls._storage is None:
            storage_backend = settings.ALEXANDRIA_FILE_STORAGE
            cls._storage = storages.create_storage({"BACKEND": storage_backend})
            if hasattr(cls._storage, "bucket"):
                # Initialize the S3 client once per process
                _ = cls._storage.bucket.meta.client

        return cls._storage

    @classmethod
    def get_preview_manager(cls):
        if cls._preview_manager is None:
            cache_path = os.path.join(tempfile.gettempdir(), "alexandria_preview_cache")
            cls._preview_manager = PreviewManager(cache_path, create_folder=True)
        return cls._preview_manager

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
                queryset=File.objects.filter(
                    variant=File.Variant.ORIGINAL
                ).prefetch_related("renderings"),
                to_attr="_originals",
            ),
            "instance_document",
        )

        # Default number of workers is number of CPU + 1.
        # If commandline passes number of workers, use that
        default_workers = (os.cpu_count() or 1) + 1
        workers = self.workers or default_workers
        executor = (
            SynchronousExecutor()
            if self.no_parallel
            else ProcessPoolExecutor(max_workers=workers)
        )
        setproctitle.setproctitle(
            f"Annotating Documents: {type(executor).__name__} with {workers} workers"
        )

        upload_state = UploadState(self.run)

        # Record the parent PID so forked workers can detect they are
        # in a child process and unset the inherited DB connection.
        AnnotateDocumentsMigrator._parent_pid = os.getpid()

        with executor as executor:
            total = len(documents)
            for i, document in enumerate(documents, start=1):
                future = executor.submit(
                    self.annotate_document,
                    document,
                    (i, total),
                    self.run,
                )
                # Process Pool executor can't update `self`, as it's in a
                # subprocess, so we do it via return values instead
                future.add_done_callback(self._record_task_result)

        if self.failed:  # pragma: no cover
            # escalate to the management command, which will set the migration
            # run to "failed" state
            raise (
                RuntimeError(
                    "Something bad happened during annotation procedure. "
                    "Check STDOUT and try again"
                )
            )

        # Now that parallel work is done, save everything to DB.
        with transaction.atomic(), disable_auto_now(Document, File):
            # When the logs, files and everything is saved, we don't need
            # the upload state anymore - these thumbnails are now "save"
            transaction.on_commit(upload_state.clear)

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

            setproctitle.setproctitle(
                "Annotating Documents: Creating Thumbnail DB entries"
            )
            File.objects.bulk_create(
                self.create_files,
                batch_size=settings.ALEXANDRIA_MIGRATION.db_batch_size,
            )
            setproctitle.setproctitle(
                "Annotating Documents: Updating vector, checksum, language"
            )
            File.objects.bulk_update(
                self.update_files,
                fields=["content_vector", "content_text", "checksum", "language"],
                batch_size=settings.ALEXANDRIA_MIGRATION.db_batch_size,
            )
            setproctitle.setproctitle("Annotating Documents: Storing logs")
            MigrationLog.objects.bulk_create(
                self.logs, batch_size=settings.ALEXANDRIA_MIGRATION.db_batch_size
            )

    def _record_task_result(self, future):
        # Can be called with future or direct result
        if isinstance(future, list):  # pragma: no cover
            result = future
        else:
            try:
                result = future.result()
            except Exception as exc:  # pragma: no cover
                print(f"Worker failed with {type(exc).__name__}: {exc}")
                self.failed = True
                return

        for file_res in result:
            if err := file_res.get("error"):  # pragma: todo cover
                # TODO: These are individual-file errors. Currently, the only
                # way to get these is if the file is not available in S3, or
                # comes out empty. This should not happen, but *might*. Not
                # sure yet whether this should cause a fatal error of the whole
                # migration run though
                print(err)
                self.failed = True
                return

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
        if not file:  # pragma: todo cover
            # TODO proper error logging / debugging in parallel mode
            print("No file for getting content, WAT")
            return None

        storage = cls.get_storage()
        assert isinstance(storage, S3Storage), (
            f"Misconfigured Storage backend? {storage} is not S3"
        )

        with storage.open(file.content.name, "rb") as fh:
            return fh.read()

    @classmethod
    def annotate_document(cls, document, progressinfo, run):
        """Annotate the given document.

        Return a list of dicts, each with their file-specific result data:
        - logs contains a list of log entries
        - file_updated: None or the updated file object
        - file_created: None or the created thumbnail
        """
        # Forked workers inherit the parent's DB socket. Reusing it from
        # multiple processes can corrupt the connection or cause the server
        # to terminate it prematurely.
        #
        # Instead of closing it (which might send a termination packet to
        # the server, breaking the parent's connection), we unset it so
        # Django "forgets" it in this process.
        is_child = os.getpid() != cls._parent_pid
        if is_child:  # pragma: no cover
            # Not covered in tests, as test uses a non-subprocess executor
            connections["default"].connection = None

        i, t = progressinfo
        doc_prefix = f"Annotating Documents: doc {i}/{t}"
        setproctitle.setproctitle(doc_prefix)

        # We only make thumbnails for the most recent files. Those
        # are the ones being used, the rest is not really needed by anyone
        if document._most_recent_file:
            most_recent = document._most_recent_file[0]
        else:  # pragma: todo cover
            most_recent = None
            # If the document has no "most recent file", it could be that it's already
            # filtered out because there is a thumbnail. Therefore, it's only a problem
            # if there is *no* thumbnail on this document.

            # But in any case, we don't process the file if there's no
            # most-recent original to be processed.
            if not document._most_recent_thumbnail:
                # There's a no thumbnail, so there's a file that has no originals
                # and no thumbnails - which should not happen in the migration
                # TODO deal with it in some more "practicable" way
                print(f"Document has no original file? {document}")

        # Pre-cache the document reference on each file so that
        # accessing file.document in the worker doesn't trigger a DB query.
        for file in document._originals:
            file.document = document

        res = [
            cls.annotate_file(
                file,
                instance_id=document.instance_document.instance_id,
                # if there's no most-recent file, but there's others, something's weird
                # TODO: We should check for each step whether it's already
                # done, and only do it (and pull the file from storage!)
                # if it's not done yet
                is_most_recent=most_recent and (file.pk == most_recent.pk),
                prefix=f"{doc_prefix} - file id {file.pk}",
                run=run,
            )
            for file in document._originals
        ]

        if is_child:  # pragma: no cover
            # Not covered in tests, as test uses a non-subprocess executor
            # If a worker in this module interacts with the DB, it's a bug.
            assert connections["default"].connection is None, (
                "Database query detected in forked worker! "
                "Workers must not interact with the database."
            )

        return res

    @classmethod
    def annotate_file(cls, file, instance_id, is_most_recent, prefix, run):
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
            setproctitle.setproctitle(f"{prefix}: Fetching contents")
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

        setproctitle.setproctitle(f"{prefix}: Checksumming")
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

        setproctitle.setproctitle(f"{prefix}: Content Vector")
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

        thumbnail = cls._make_thumbnail(file, instance_id, content, run, prefix)
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
    def _make_thumbnail(cls, file, instance_id, content, run, prefix):
        """Generate thumbnail for the given file.

        Return the thumbnail File if done, None if not.
        """
        if (
            file.variant == File.Variant.ORIGINAL
            # Use the prefetched renderings cache to avoid a DB query in
            # the forked worker process (DB connections are not fork-safe).
            and len(file.renderings.all()) < 1
            and settings.ALEXANDRIA_ENABLE_THUMBNAIL_GENERATION
        ):
            return cls._create_thumbnail(file, content, run, prefix)

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

        tika_timeout = settings.ALEXANDRIA_MIGRATION.tika_timeout
        try:
            with timeout(tika_timeout):
                parsed_content = TikaClient.get_content_from_buffer(content)
        except Exception:  # pragma: no cover
            # SIGALRM during requests.put() is caught by urllib3 and
            # re-raised as ReadTimeout/ConnectionError instead of
            # TimeoutError.  Treat any such failure as empty content.
            parsed_content = None

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

        try:
            with timeout(tika_timeout):
                language = TikaClient.get_language_from_content(parsed_content[:1000])
        except Exception:  # pragma: no cover
            language = settings.LANGUAGE_CODE

        if not language or language == "unknown":  # pragma: no cover
            language = settings.LANGUAGE_CODE

        config = settings.ALEXANDRIA_ISO_639_TO_PSQL_SEARCH_CONFIG.get(
            language, "simple"
        )
        text_content = parsed_content.strip()

        # Truncate content for indexing to avoid Postgres tsvector limits (1MB)
        # and excessively large SQL queries.
        indexed_content = text_content[
            : settings.ALEXANDRIA_MIGRATION.search_vector_max_chars
        ]

        content_vector = base_vector + SearchVector(
            Value(indexed_content),
            config=config,
            weight="C",
        )

        file.content_vector = content_vector
        file.language = language
        # Truncate stored text to a reasonable limit to avoid
        # massive DB rows that slow down everything.
        file.content_text = text_content[
            : settings.ALEXANDRIA_MIGRATION.content_text_max_chars
        ]
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
    def _create_thumbnail(cls, file, content, run, prefix):
        """Generate an Alexandria thumbnail file and return it.

        May return None if it wasn't possible
        """

        setproctitle.setproctitle(f"{prefix}: Thumbnailing")
        extension = guess_extension(file.mime_type)
        with NamedTemporaryFile(suffix=extension) as tmp:
            tmp.write(content)
            tmp.flush()

            manager = cls.get_preview_manager()
            preview_kwargs = {"file_ext": extension}
            if settings.ALEXANDRIA_THUMBNAIL_WIDTH:  # pragma: no cover
                preview_kwargs["width"] = settings.ALEXANDRIA_THUMBNAIL_WIDTH
            if settings.ALEXANDRIA_THUMBNAIL_HEIGHT:  # pragma: no cover
                preview_kwargs["height"] = settings.ALEXANDRIA_THUMBNAIL_HEIGHT
            try:
                path_to_preview_image = Path(
                    manager.get_jpeg_preview(tmp.name, **preview_kwargs)
                )
            # thumbnail generation can throw many different exceptions, catch all
            except Exception:  # noqa: B902
                return None

        with path_to_preview_image.open("rb") as thumb:
            thumb_content = thumb.read()

            storage = cls.get_storage()
            new_file_pk = make_uuid()
            file_name = f"{file.name}_preview.jpg"
            s3_filename = f"{new_file_pk}_{file_name}"

            # Immediate upload
            setproctitle.setproctitle(f"{prefix}: Uploading thumbnail")

            actual_s3_path = storage.save(s3_filename, ContentFile(thumb_content))
            UploadState(run).add(actual_s3_path)

            ret = File(
                pk=new_file_pk,
                name=file_name,
                document=file.document,
                variant=File.Variant.THUMBNAIL.value,
                created_at=timezone.now(),
                modified_at=timezone.now(),
                original=file,
                encryption_status=file.encryption_status,
                content=actual_s3_path,
                mime_type="image/jpeg",
                size=len(thumb_content),
            )

            # Clean up the local preview image
            if path_to_preview_image.exists():
                path_to_preview_image.unlink()

            setproctitle.setproctitle(f"{prefix}: Done")

            return ret
