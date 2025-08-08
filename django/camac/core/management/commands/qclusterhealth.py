import json
from datetime import datetime, timedelta

import django_q.monitor
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

STATE_STORAGE_FILE = "/tmp/qclusterhealth_state.json"


class Command(BaseCommand):
    """
    Health check to report Q-cluster liveness.

    You can use this for a Kubernetes health check, by configuring the following
    liveness probe:

    ```yaml
      livenessProbe:
        exec:
          command: ["python", "manage.py", "qclusterhealth"]
    ```

    You can add a `--max-scheduled-age` parameter to define which task age
    is considered problematic (Defaults to 300 seconds, which is 5 minutes).

    Additionally, you can also pass a `--max-queue-size` parameter, to define
    at which point the queue size is considered unhealthy. Because this is very
    deployment/traffic-dependent, it's disabled by default.

    The `--check-trend` parameter can be used to track the change of the
    situation over time. If enabled, a "bad" situation (too long queue, too
    old entries) is not immediately reported as bad (exit code), but instead
    it is observed over two runs, and only if it gets worse, will the health be
    reported as "bad".

    For example: If you call it with the default arguments, and the oldest task
    is older than 5 minutes, it would immediately report "unhealthy", and the
    pod could get restarted. This of course puts a delay into processing, and if
    the next run is "bad" as well, we have an implicit restart loop.

    If we use the `--check-trend` parameter instead, it will only report
    "unhealthy" if the oldest scheduled task did not change during two check
    runs, or if the queue length got *longer*
    """

    help = "Q-Cluster health check."

    def add_arguments(self, parser):
        parser.add_argument(
            "-a",
            "--max-scheduled-age",
            type=int,
            default=5 * 60,
            help="Max age of a scheduled task, in seconds. Defaults to 5 mins",
            required=False,
        )

        parser.add_argument(
            "-q",
            "--max-queue-size",
            type=int,
            default=0,
            help="Max number of tasks in the task queue. Defaults to 0 (don't check)",
            required=False,
        )

        parser.add_argument(
            "-t",
            "--check-trend",
            action="store_true",
            help=(
                "Track trend of the situation instead of instantaneous state "
                "(only report if limit gets exceeded towards worse)"
            ),
            required=False,
        )

    def _read_state(self):
        """Read current system state and store it.

        Updates the properties `self._current_queue_size` (a size, integer)
        and `self._current_oldest_task` (a datetime or None)
        """
        broker = django_q.monitor.get_broker()
        self._current_queue_size = broker.queue_size()

        now = timezone.now()
        oldest_task = now
        has_tasks = False
        for task in broker.get_connection():
            has_tasks = True
            oldest_task = min(oldest_task, task.task.get("started"))

        self._current_oldest_task = oldest_task if has_tasks else None

    def _is_queue_size_healthy(self):
        if self.max_qsize:
            if self._current_queue_size > self.max_qsize:
                self.stdout.write(
                    f"Queue size exceeded: {self._current_queue_size} is "
                    f"over the limit of  {self.max_qsize}"
                )
                return False
        return True

    def _is_task_age_healthy(self):
        if not self.max_age:  # pragma: no cover
            # Not covered - explicitly disabling task age check is not worth
            # it's own test case
            return True

        if (
            self._current_oldest_task is not None
            and self._current_oldest_task < self.max_allowed_task_birth
        ):
            self.stdout.write(
                f"At least one tasks is pending for over {self.max_age} seconds"
            )
            return False
        return True

    def _store_state(self):
        fh = open(STATE_STORAGE_FILE, "w")
        json.dump(
            {
                "queue_size": self._current_queue_size,
                "oldest_task": (
                    self._current_oldest_task.isoformat()
                    if self._current_oldest_task
                    else None
                ),
                "task_age_healthy": self._is_task_age_healthy(),
                "queue_size_healthy": self._is_queue_size_healthy(),
                "measured_at": timezone.now().isoformat(),
            },
            fh,
        )
        fh.close()

    def _load_previous_state(self):
        self._previous_queue_size = None
        self._previous_oldest_task = None

        # previous state is assumed "good" by default
        self._previous_task_age_was_healthy = True
        self._previous_queue_size_was_healthy = True
        try:
            fh = open(STATE_STORAGE_FILE, "r")
            data = json.load(fh)
            fh.close()
        except Exception:
            # reading / parse error is just what happens on first run and is
            # acceptable
            return

        self._previous_queue_size = data["queue_size"]
        self._previous_task_age_was_healthy = data["task_age_healthy"]
        self._previous_queue_size_was_healthy = data["queue_size_healthy"]

        if oldest := data["oldest_task"]:
            self._previous_oldest_task = datetime.fromisoformat(oldest)

    def _check_current_state(self):
        # For each failed check, increase the fail counter
        failed = sum(
            [
                int(not self._is_queue_size_healthy()),
                int(not self._is_task_age_healthy()),
            ]
        )

        if failed:
            raise CommandError(
                "At least one check failed. Q-Cluster seems unhealthy",
                returncode=failed,
            )

    def _check_trend(self):
        has_improved = True

        task_age_was_bad = not self._previous_task_age_was_healthy
        if task_age_was_bad and not self._is_task_age_healthy():
            has_improved = False

        queue_length_was_bad = not self._previous_queue_size_was_healthy
        if queue_length_was_bad and not self._is_queue_size_healthy():
            has_improved = False

        if not has_improved:
            raise CommandError(
                "At least one check failed, and situation "
                "didn't improve since last time",
                returncode=5,
            )

    def handle(self, *args, **options):
        self.max_age = options.get("max_scheduled_age")
        self.max_qsize = options.get("max_queue_size")
        self.check_trend = options.get("check_trend", False)

        now = timezone.now()
        self.max_allowed_task_birth = now - timedelta(seconds=self.max_age)

        # previous state is loaded, THEN current system state is extracted.
        # The current state is then saved for future runs.
        self._load_previous_state()
        self._read_state()
        self._store_state()

        if self.check_trend:
            self._check_trend()
        else:
            self._check_current_state()
