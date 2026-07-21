import contextlib
import os

from celery import Celery
from celery.signals import worker_process_init

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "camac.settings")

app = Celery("camac")


@worker_process_init.connect
def _start_debugpy(**_):  # pragma: no cover
    from django.conf import settings

    if not os.environ.get("ENABLE_PTVSD_DEBUGGER") or not settings.DEBUG:
        return

    # Silence pydevd's "frozen modules" warning emitted on every worker process.
    os.environ.setdefault("PYDEVD_DISABLE_FILE_VALIDATION", "1")

    import debugpy

    port = int(os.environ.get("CELERY_DEBUGPY_PORT", 5679))

    with contextlib.suppress(OSError, RuntimeError):
        debugpy.listen(("0.0.0.0", port))
        print(f"Attached remote debugger for VSCode (celery) on port {port}")


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
