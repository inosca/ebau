import fcntl
import signal
import tempfile
from contextlib import contextmanager
from datetime import timedelta
from functools import lru_cache
from pathlib import Path

from alexandria.core.models import Category, Mark
from django.conf import settings

from camac.document.models import AttachmentSection


@lru_cache
def get_available_categories() -> dict[str, Category]:
    """Get all available alexandria categories as a dict using the slug as key."""

    return {category.pk: category for category in Category.objects.all()}


@lru_cache
def get_available_marks() -> dict[str, Mark]:
    return {mark.pk: mark for mark in Mark.objects.all()}


@lru_cache
def get_fallback_category() -> Category:
    return get_available_categories()[settings.ALEXANDRIA_MIGRATION.fallback_category]


@lru_cache
def get_target_category(
    attachment_section: AttachmentSection,
    bucket: str | None,
) -> Category:
    """Get the correct alexandria category given an attachment section and bucket name."""

    available_categories = get_available_categories()

    category = settings.ALEXANDRIA_MIGRATION.category_mapping.get(attachment_section.pk)
    suffix = settings.ALEXANDRIA_MIGRATION.category_suffix_mapping.get(bucket)

    if not category:
        raise ValueError(
            "Could not find category for attachment section "
            f"{attachment_section.pk} with bucket {bucket}. Please check the "
            "category mapping in the module configuration."
        )

    full_slug = category

    if suffix is not None:
        full_slug += suffix

    if full_slug not in available_categories:
        full_slug = category

    return available_categories[full_slug]


def get_marks_from_context(context: dict[str, bool]) -> list[Mark]:
    """Get the correct marks from a given context dictionary containing legacy marks."""

    available_marks = get_available_marks()

    return [
        available_marks[mark_slug]
        for context_key, mark_slug in settings.ALEXANDRIA_MIGRATION.context_mark_mapping.items()
        if context.get(context_key) is True
    ]


def humanize_timedelta(delta: timedelta) -> str:
    """Format timedelta in a human-readable way.

    E.g.: "1h 16m 30s"
    """

    total_seconds = int(delta.total_seconds())

    hours, remainder = divmod(total_seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    parts = []
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds or not parts:
        parts.append(f"{seconds}s")

    return " ".join(parts)


class UploadState:
    """Store S3 upload state in a temporary log file for later cleanup if needed.

    We upload thumbnails to S3 before writing the corresponding data to the DB.
    If the migration aborts, we need a way to cleanup these thumbnails to avoid
    collecting garbage in S3, and therefore we write the uploaded files to this
    log.

    When committing the changes to DB, we cleanup the upload log again.
    """

    def __init__(self, run):
        self.path = (
            Path(tempfile.gettempdir()) / f"alexandria_migration_{run.pk}_uploads.log"
        )

    def add(self, s3_path: str):
        """Append an S3 path to the log file in a process-safe way."""
        with open(self.path, "a") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            f.write(f"{s3_path}\n")
            fcntl.flock(f, fcntl.LOCK_UN)

    def get_all(self) -> list[str]:
        """Return a list of all S3 paths in the log file."""
        if not self.path.exists():
            return []  # pragma: no cover
        with open(self.path) as f:
            return [line.strip() for line in f if line.strip()]

    def clear(self):
        """Delete the log file."""
        self.delete_log_file(self.path)

    @classmethod
    def delete_log_file(cls, path: Path):
        """Delete a log file."""
        if path.exists():
            path.unlink()

    @classmethod
    def get_all_log_files(cls) -> list[Path]:
        """Find all migration upload log files in the temp directory."""
        tmp_dir = Path(tempfile.gettempdir())
        return list(tmp_dir.glob("alexandria_migration_*_uploads.log"))


@contextmanager
def timeout(seconds):
    """Context manager for timing out a block of code using SIGALRM."""

    assert seconds, "Cannot have a timeout with 0 seconds"

    def signal_handler(signum, frame):
        raise TimeoutError("Timed out!")

    old_handler = signal.signal(signal.SIGALRM, signal_handler)
    signal.alarm(int(seconds))
    try:
        yield
    finally:
        signal.alarm(0)
        signal.signal(signal.SIGALRM, old_handler)
