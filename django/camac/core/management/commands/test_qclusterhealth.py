import json
import time

import pytest
from django.core.management import call_command
from django.core.management.base import CommandError
from django_q.tasks import async_task

import camac.core.management.commands.qclusterhealth

pytest.fixture(scope="function", autouse=True)


@pytest.fixture(scope="function", autouse=True)
def mock_state_file(mocker, tmp_path):
    # Patch the state storage file to a temp dir, so we don't leak
    # state between tests
    mocker.patch(
        "camac.core.management.commands.qclusterhealth.STATE_STORAGE_FILE",
        str(tmp_path / "state.json"),
    )


def _read_state_file():
    with open(
        camac.core.management.commands.qclusterhealth.STATE_STORAGE_FILE, "r"
    ) as fh:
        return json.load(fh)


def test_queue_length(db):
    # schedule two tasks
    async_task(time.sleep, 5)
    async_task(time.sleep, 5)

    with pytest.raises(CommandError) as excinfo:
        call_command("qclusterhealth", "--max-queue-size", "1")
    assert excinfo.match("At least one check failed. Q-Cluster seems unhealthy")

    # Use state file (that's always written)
    # to check if it did it's work
    assert _read_state_file()["queue_size"] == 2


def test_scheduled_task_age(db, freezer):
    # schedule two tasks
    freezer.move_to("2025-08-11T00:00:00Z")
    async_task(time.sleep, 5)
    async_task(time.sleep, 5)

    freezer.move_to("2025-08-11T0:06:00Z")
    with pytest.raises(CommandError) as excinfo:
        # max age by default is 5min, which we've exceeded by one minute
        call_command("qclusterhealth")

    assert excinfo.match("At least one check failed. Q-Cluster seems unhealthy")
    assert _read_state_file()["oldest_task"] == "2025-08-11T00:00:00+00:00"


def test_okay_state(db, freezer):
    # schedule two tasks
    freezer.move_to("2025-08-11T00:00:00Z")
    async_task(time.sleep, 5)
    async_task(time.sleep, 5)

    freezer.move_to("2025-08-11T00:30:00Z")
    # max age: 3600 seconds = 1h, well within our limit
    call_command(
        "qclusterhealth", "--max-queue-size", "3", "--max-scheduled-age", "3600"
    )
    # Implicitly checking that the command did not throw an exception by just
    # continuing here :-)

    # Use state file (that's always written)
    # to check if it did it's work
    state = _read_state_file()
    assert state["queue_size"] == 2
    assert state["oldest_task"] == "2025-08-11T00:00:00+00:00"


def test_trend_fresh(db, freezer):
    # schedule two tasks
    freezer.move_to("2025-08-11T00:00:00Z")
    async_task(time.sleep, 5)
    async_task(time.sleep, 5)

    # First call: everything good, no trend checking occurs
    call_command(
        "qclusterhealth",
        "--max-queue-size",
        "2",
        "--check-trend",
    )

    freezer.move_to("2025-08-11T00:30:00Z")
    async_task(time.sleep, 5)

    # Second trend-checking run should not cause any trouble -
    # this is the first "problem detection". It's bad though
    # for two reasons - we have 3 tasks (exceeding 2) and
    # the oldest tasks is more than 5 minutes old
    call_command(
        "qclusterhealth",
        "--max-queue-size",
        "2",
        "--check-trend",
    )

    # just 5 seconds later: test again, but now we have a trend
    # as it's been "bad" for two times
    freezer.move_to("2025-08-11T00:30:05Z")
    with pytest.raises(CommandError) as excinfo:
        call_command(
            "qclusterhealth",
            "--max-queue-size",
            "2",
            "--check-trend",
        )
    assert excinfo.match(
        "At least one check failed, and situation didn't improve since last time"
    )
