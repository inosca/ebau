import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = """Removes tempfiles (zips, pdfs, etc) from TEMPFILE_DOWNLOAD_PATH
    and all its subfolders which are at least TEMPFILE_RETENTION_TIME seconds
    old."""

    def handle(self, *args, **options):
        base_dir = settings.TEMPFILE_DOWNLOAD_PATH
        threshold = time.time() - settings.TEMPFILE_RETENTION_TIME

        for path in Path(base_dir).glob("**/*"):
            # we assume that modification time is same as creation time
            if path.is_file() and path.stat().st_mtime < threshold:
                path.unlink()
