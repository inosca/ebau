import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

BASE_DIR = "/tmp"
EXCLUDE_DIR = "/tmp/camac"


class Command(BaseCommand):
    help = """Disclaimer: This is a temporary fix to manage the growth of the
    temporary files generated through long-running child processes created
    by sorl-thumbnail during thumbnail generation. As soon as a sustainble
    fix is implemented, this command should be removed.

    Removes tempfiles from /tmp and all its subfolders (except for camac)
    in the django container which are at least TEMPFILE_RETENTION_TIME
    seconds old. The subfolder /tmp/camac is ignored and is handled separately
    through the managament command cleanup_tempfiles."""

    def handle(self, *args, **options):
        base_path = Path(BASE_DIR)
        exclude_path = Path(EXCLUDE_DIR)
        threshold = time.time() - settings.TEMPFILE_RETENTION_TIME

        for path in base_path.glob("**/*"):
            if exclude_path in [path] + [parent for parent in path.parents]:
                continue

            # we assume that modification time is same as creation time
            if path.is_file() and path.stat().st_mtime < threshold:
                path.unlink()
