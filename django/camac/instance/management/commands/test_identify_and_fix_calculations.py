import datetime
import json
import logging
import signal
import sqlite3
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from types import SimpleNamespace

import openpyxl
import pytest
from django.core.management import CommandError
from django.db import transaction
from django.db.models import Q

from camac.instance.management.commands import identify_and_fix_calculations
from camac.instance.management.commands.identify_and_fix_calculations import (
    Command,
    RecalcInfo,
    RunState,
    RunStateStore,
    StatsEntry,
    TaskResult,
)

CONFIGURATION = {
    "do_validate": False,
    "do_recalc": True,
    "do_fix_calc": True,
    "do_commit": True,
    "analyze_only": (),
    "search_only": None,
    "recalc_handoff_in": None,
}


def _stats_entry(instance_id, event="detected"):
    return StatsEntry(
        "Test municipality",
        f"{instance_id} (in progress)",
        [
            RecalcInfo(
                name="calculated-field",
                hidden=False,
                before=1,
                after=2,
                event=event,
            )
        ],
    )


def _checkpoint_and_raise(state_configuration, result, message):
    with transaction.atomic():
        Command._checkpoint_on_commit(state_configuration, result)
        raise RuntimeError(message)


def test_run_state_is_created_resumed_and_reset():
    store = RunStateStore(CONFIGURATION)

    state = store.start()
    assert store.path.exists()
    assert store.path.name == "state.sqlite3"
    assert state.configuration == CONFIGURATION

    store.record_completed("recalculation", 1, [_stats_entry(1)])
    store.record_completed("recalculation", 1, [_stats_entry(1, event="fixed")])
    store.record_completed("validation", 2, [])
    resumed = store.start()
    assert resumed.completed_ids == {"recalculation": {1}, "validation": {2}}
    assert resumed.results[("recalculation", 1)] == [_stats_entry(1)]
    assert resumed.results[("validation", 2)] == []

    incompatible_store = RunStateStore({**CONFIGURATION, "do_fix_calc": False})
    with pytest.raises(CommandError, match="different command options"):
        incompatible_store.start()

    reset = incompatible_store.start(reset=True)
    assert reset.configuration == incompatible_store.configuration
    assert reset.completed_ids == {}


def test_checkpoint_results_are_stored_as_individual_sqlite_rows():
    store = RunStateStore(CONFIGURATION)
    store.start()
    store.record_completed("validation", 1, [])
    store.record_completed("recalculation", 1, [_stats_entry(1)])

    with sqlite3.connect(store.path) as connection:
        rows = connection.execute(
            "SELECT phase, instance_id FROM completed_instances ORDER BY phase"
        ).fetchall()

    assert rows == [("recalculation", 1), ("validation", 1)]


def test_malformed_sqlite_checkpoint_can_be_reset():
    store = RunStateStore(CONFIGURATION)
    store.directory.mkdir(parents=True)
    store.path.write_text("not an SQLite database")

    with pytest.raises(CommandError, match="Use --reset-state"):
        store.start()

    assert store.start(reset=True).configuration == CONFIGURATION


def test_many_sqlite_checkpoints_restore_all_completed_instances():
    store = RunStateStore(CONFIGURATION)
    store.start()

    for instance_id in range(1_000):
        store.record_completed("validation", instance_id, [])

    resumed = store.start()
    assert resumed.completed_ids == {"validation": set(range(1_000))}
    assert len(resumed.results) == 1_000


def test_run_configuration_ignores_verbosity_and_dev_mode():
    options = {**CONFIGURATION, "dev_mode": False, "verbosity": 0}

    assert Command._run_configuration(options) == CONFIGURATION
    assert (
        Command._run_configuration({**options, "dev_mode": True, "verbosity": 3})
        == CONFIGURATION
    )


def test_run_configuration_includes_handoff_input_but_not_output(tmp_path):
    handoff_input = tmp_path / "handoff.json"

    assert Command._run_configuration(
        {**CONFIGURATION, "recalc_handoff_in": handoff_input}
    ) == {**CONFIGURATION, "recalc_handoff_in": str(handoff_input)}
    assert (
        Command._run_configuration(
            {**CONFIGURATION, "recalc_handoff_out": tmp_path / "output.json"}
        )
        == CONFIGURATION
    )


def test_parallel_argument_accepts_an_optional_worker_count():
    parser = Command.__new__(Command).create_parser(
        "manage.py", "identify_and_fix_calculations"
    )

    assert parser.parse_args([]).parallel is False
    assert parser.parse_args(["--parallel"]).parallel is None
    assert parser.parse_args(["--parallel", "2"]).parallel == 2
    assert (
        parser.parse_args(["--recalc-handoff-out", "out.json"]).recalc_handoff_out.name
        == "out.json"
    )
    assert (
        parser.parse_args(["--recalc-handoff-in", "in.json"]).recalc_handoff_in.name
        == "in.json"
    )


def test_load_recalculation_handoff_normalizes_duplicate_ids(tmp_path):
    path = tmp_path / "handoff.json"
    path.write_text(
        json.dumps(
            {
                "instance_ids": [4, 2, 4],
                "last_instance_created_at": "2025-01-15T10:30:00+00:00",
            }
        )
    )

    instance_ids, cutoff = Command._load_recalculation_handoff(path)

    assert instance_ids == {2, 4}
    assert cutoff == datetime.datetime(2025, 1, 15, 10, 30, tzinfo=datetime.UTC)


@pytest.mark.parametrize(
    ("content", "message"),
    [
        ("[]", "must be a JSON object"),
        (json.dumps({"instance_ids": []}), "must be a JSON object"),
        (
            json.dumps(
                {
                    "instance_ids": ["1"],
                    "last_instance_created_at": "2025-01-15T10:30:00+00:00",
                }
            ),
            "instance_ids must contain only integers",
        ),
        (
            json.dumps(
                {
                    "instance_ids": [],
                    "last_instance_created_at": "not a timestamp",
                }
            ),
            "must be an ISO-8601 timestamp",
        ),
        (
            json.dumps(
                {
                    "instance_ids": [],
                    "last_instance_created_at": "2025-01-15T10:30:00",
                }
            ),
            "must include a timezone",
        ),
    ],
)
def test_load_recalculation_handoff_rejects_invalid_content(tmp_path, content, message):
    path = tmp_path / "handoff.json"
    path.write_text(content)

    with pytest.raises(CommandError, match=message):
        Command._load_recalculation_handoff(path)


def test_load_recalculation_handoff_rejects_missing_or_invalid_json(tmp_path):
    with pytest.raises(CommandError, match="Could not read recalculation handoff"):
        Command._load_recalculation_handoff(tmp_path / "missing.json")

    path = tmp_path / "invalid.json"
    path.write_text("not JSON")
    with pytest.raises(CommandError, match="Could not read recalculation handoff"):
        Command._load_recalculation_handoff(path)


def test_recalculation_handoff_unions_exported_ids_with_changed_calculations(
    monkeypatch,
):
    cutoff = datetime.datetime(2025, 1, 15, 10, 30, tzinfo=datetime.UTC)

    class QuerySet:
        def __init__(self, count, values=None):
            self.count_value = count
            self.values_value = values
            self.filter_calls = []

        def filter(self, *args, **kwargs):
            self.filter_calls.append((args, kwargs))
            return self

        def count(self):
            return self.count_value

        def values(self, *fields):
            assert fields == ("pk",)
            return self.values_value

    class Manager:
        def __init__(self, querysets):
            self.querysets = iter(querysets)
            self.filter_calls = []

        def filter(self, *args, **kwargs):
            self.filter_calls.append((args, kwargs))
            return next(self.querysets)

    answer_query = QuerySet(count=0)
    changed_instances = QuerySet(count=2, values="changed-instance-ids")
    exported_instances = QuerySet(count=1)
    combined_instances = QuerySet(count=3)
    instance_manager = Manager([exported_instances, combined_instances])
    answer_manager = Manager([answer_query])
    monkeypatch.setattr(
        identify_and_fix_calculations,
        "Instance",
        SimpleNamespace(objects=instance_manager),
    )
    monkeypatch.setattr(
        identify_and_fix_calculations, "Answer", SimpleNamespace(objects=answer_manager)
    )
    monkeypatch.setattr(identify_and_fix_calculations, "OuterRef", lambda field: field)
    monkeypatch.setattr(
        identify_and_fix_calculations, "Exists", lambda queryset: queryset
    )
    command = Command.__new__(Command)
    command.recalc_handoff = ({2, 5}, cutoff)
    command._base_qs = lambda: changed_instances

    assert command._recalculation_qs() is combined_instances

    assert answer_manager.filter_calls == [
        ((), {"document__family__case__pk": "case"}),
    ]
    assert answer_query.filter_calls == [
        ((Q(created_at__gt=cutoff) | Q(modified_at__gt=cutoff),), {}),
    ]
    assert instance_manager.filter_calls == [
        ((), {"pk__in": {2, 5}}),
        (
            (Q(pk__in={2, 5}) | Q(pk__in="changed-instance-ids"),),
            {},
        ),
    ]


def test_recalculation_handoff_export_contains_known_incorrect_ids_and_cutoff(
    monkeypatch, tmp_path
):
    latest_creation_date = datetime.datetime(2025, 1, 15, 10, 30, tzinfo=datetime.UTC)
    values = SimpleNamespace(first=lambda: latest_creation_date)
    instances = SimpleNamespace(
        order_by=lambda *args: SimpleNamespace(
            values_list=lambda *args, **kwargs: values
        )
    )
    monkeypatch.setattr(
        identify_and_fix_calculations, "Instance", SimpleNamespace(objects=instances)
    )
    command = Command.__new__(Command)
    command.run_state = RunState(
        configuration=CONFIGURATION,
        started_at=datetime.datetime.now(),
        results={
            ("recalculation", 3): [_stats_entry(3, event="fixed")],
            ("recalculation", 1): [_stats_entry(1, event="detected")],
            ("recalculation", 2): [_stats_entry(2, event="clean")],
            ("validation", 4): [_stats_entry(4, event="detected")],
        },
    )
    output_path = tmp_path / "handoff.json"

    command._write_recalculation_handoff(output_path)

    assert json.loads(output_path.read_text()) == {
        "instance_ids": [1, 3],
        "last_instance_created_at": "2025-01-15T10:30:00+00:00",
    }


def test_handoff_export_reloads_completed_results(monkeypatch, tmp_path):
    initial_state = RunState(
        configuration=CONFIGURATION,
        started_at=datetime.datetime.now(),
    )
    completed_state = RunState(
        configuration=CONFIGURATION,
        started_at=initial_state.started_at,
        results={("recalculation", 1): [_stats_entry(1)]},
    )

    class StateStoreStub:
        instance = None

        def __init__(self, configuration):
            type(self).instance = self
            self.configuration = configuration
            self.start_calls = []

        def start(self, reset=False):
            self.start_calls.append(reset)
            return initial_state if len(self.start_calls) == 1 else completed_state

    class ExecutorStub:
        def shutdown(self, *args, **kwargs):
            pass

    command = Command.__new__(Command)
    command.configure_logging = lambda verbosity: None
    command._restore_stats = lambda: None
    command.log_stats = lambda: None
    written_states = []
    command._write_recalculation_handoff = lambda path: written_states.append(
        command.run_state
    )
    monkeypatch.setattr(identify_and_fix_calculations, "RunStateStore", StateStoreStub)
    monkeypatch.setattr(
        identify_and_fix_calculations, "SynchronousExecutor", ExecutorStub
    )

    command.handle(
        verbosity=0,
        parallel=False,
        do_validate=False,
        do_recalc=False,
        do_fix_calc=False,
        do_commit=False,
        excel_out=None,
        recalc_handoff_in=None,
        recalc_handoff_out=tmp_path / "handoff.json",
        dev_mode=False,
        analyze_only=None,
        search_only=None,
        reset_state=False,
    )

    assert StateStoreStub.instance.start_calls == [False, False]
    assert written_states == [completed_state]


@pytest.mark.parametrize("parallel", [None, 2])
def test_parallel_worker_count_is_passed_to_executor(monkeypatch, parallel):
    class RecordingExecutor:
        instance = None

        def __init__(self, max_workers=None):
            type(self).instance = self
            self.max_workers = max_workers

        def shutdown(self, *args, **kwargs):
            pass

    class StateStoreStub:
        def __init__(self, configuration):
            self.configuration = configuration

        def start(self, reset=False):
            return RunState(
                configuration=self.configuration,
                started_at=datetime.datetime.now(),
            )

    command = Command.__new__(Command)
    command.configure_logging = lambda verbosity: None
    command._restore_stats = lambda: None
    command.log_stats = lambda: None
    monkeypatch.setattr(
        identify_and_fix_calculations, "ProcessPoolExecutor", RecordingExecutor
    )
    monkeypatch.setattr(identify_and_fix_calculations, "RunStateStore", StateStoreStub)

    command.handle(
        verbosity=0,
        parallel=parallel,
        do_validate=False,
        do_recalc=False,
        do_fix_calc=False,
        do_commit=False,
        excel_out=None,
        recalc_handoff_in=None,
        recalc_handoff_out=None,
        dev_mode=False,
        analyze_only=None,
        search_only=None,
        reset_state=False,
    )

    assert RecordingExecutor.instance.max_workers == parallel


@pytest.mark.django_db(transaction=True)
def test_checkpoint_is_written_only_after_document_commit():
    store = RunStateStore(CONFIGURATION)
    store.start()
    assert store.start().completed_ids == {}
    result = TaskResult("recalculation", 1, [_stats_entry(1)])

    with pytest.raises(RuntimeError, match="rollback"):
        _checkpoint_and_raise(CONFIGURATION, result, "rollback")

    assert store.start().completed_ids == {}

    with transaction.atomic():
        Command._checkpoint_on_commit(CONFIGURATION, result)

    assert store.start().completed_ids == {"recalculation": {1}}


@pytest.mark.django_db(transaction=True)
def test_checkpoint_keeps_previously_committed_documents_after_failure():
    store = RunStateStore(CONFIGURATION)
    store.start()

    with transaction.atomic():
        Command._checkpoint_on_commit(
            CONFIGURATION, TaskResult("recalculation", 1, [_stats_entry(1)])
        )

    with pytest.raises(RuntimeError, match="second document"):
        _checkpoint_and_raise(
            CONFIGURATION,
            TaskResult("recalculation", 2, [_stats_entry(2)]),
            "second document failed",
        )

    state = store.start()
    assert state.completed_ids == {"recalculation": {1}}
    assert ("recalculation", 2) not in state.results


@pytest.mark.django_db(transaction=True)
@pytest.mark.parametrize(
    ("task", "task_kwargs", "phase", "operation"),
    [
        (Command.check_validation, {}, "validation", "validation"),
        (
            Command.check_miscalculation,
            {"analyze_only": None, "fix_calculation": False, "do_commit": False},
            "recalculation",
            "recalculation",
        ),
    ],
)
def test_failed_tasks_are_logged_without_being_checkpointed(
    monkeypatch, caplog, task, task_kwargs, phase, operation
):
    def fail_clean_env(cls):
        raise RuntimeError("expected failure")

    RunStateStore(CONFIGURATION).start(reset=True)
    monkeypatch.setattr(Command, "_clean_env", classmethod(fail_clean_env))

    result = task("[Test 1/1]", 1, state_configuration=CONFIGURATION, **task_kwargs)

    command = Command.__new__(Command)
    command.stats = defaultdict(lambda: defaultdict(list))
    with caplog.at_level(logging.ERROR):
        command._log_result(SimpleNamespace(result=lambda: result))

    assert result.phase == phase
    assert any(
        f"Error during {operation} (expected failure)" in message
        for message in caplog.messages
    )
    assert RunStateStore(CONFIGURATION).start().completed_ids == {}


def test_concurrent_checkpoint_merges_preserve_all_outcomes():
    RunStateStore(CONFIGURATION).start()

    def record(instance_id):
        RunStateStore(CONFIGURATION).record_completed(
            "recalculation", instance_id, [_stats_entry(instance_id)]
        )

    with ThreadPoolExecutor(max_workers=4) as executor:
        list(executor.map(record, range(1, 9)))

    state = RunStateStore(CONFIGURATION).start()
    assert state.completed_ids == {"recalculation": set(range(1, 9))}
    assert set(state.results) == {
        ("recalculation", instance_id) for instance_id in range(1, 9)
    }


@pytest.mark.parametrize("stop_signal", [signal.SIGINT, signal.SIGTERM])
def test_stop_signals_cancel_pending_work_without_waiting(
    monkeypatch, stop_signal, tmp_path
):
    class InterruptingExecutor:
        instance = None

        def __init__(self):
            type(self).instance = self
            self.shutdown_calls = []

        def submit(self, *args, **kwargs):
            signal.raise_signal(stop_signal)

        def shutdown(self, *args, **kwargs):
            self.shutdown_calls.append((args, kwargs))

    class StateStoreStub:
        def __init__(self, configuration):
            self.configuration = configuration

        def start(self, reset=False):
            return RunState(
                configuration=self.configuration,
                started_at=datetime.datetime.now(),
            )

    command = Command.__new__(Command)
    command.configure_logging = lambda verbosity: None
    command._restore_stats = lambda: None
    command.iter_instances_for_validation = lambda: (1, [SimpleNamespace(pk=1)])
    command.log_stats = lambda: pytest.fail("stats should not be logged on interrupt")
    command._write_recalculation_handoff = lambda path: pytest.fail(
        "handoff should not be exported on interrupt"
    )
    previous_handler = signal.getsignal(stop_signal)

    monkeypatch.setattr(
        identify_and_fix_calculations, "SynchronousExecutor", InterruptingExecutor
    )
    monkeypatch.setattr(identify_and_fix_calculations, "RunStateStore", StateStoreStub)

    command.handle(
        verbosity=0,
        parallel=False,
        do_validate=True,
        do_recalc=False,
        do_fix_calc=False,
        do_commit=False,
        excel_out=None,
        recalc_handoff_in=None,
        recalc_handoff_out=tmp_path / "handoff.json",
        dev_mode=False,
        analyze_only=None,
        search_only=None,
        reset_state=False,
    )

    assert signal.getsignal(stop_signal) is previous_handler
    assert InterruptingExecutor.instance.shutdown_calls == [
        ((), {"wait": False, "cancel_futures": True})
    ]


class QuerySetStub:
    def __init__(self, instance_ids):
        self.instance_ids = list(instance_ids)

    def exclude(self, **kwargs):
        excluded_ids = kwargs.get("pk__in")
        if excluded_ids is None:
            return self
        return QuerySetStub(
            instance_id
            for instance_id in self.instance_ids
            if instance_id not in excluded_ids
        )

    def filter(self, **kwargs):
        included_ids = kwargs["pk__in"]
        return QuerySetStub(
            instance_id
            for instance_id in self.instance_ids
            if instance_id in included_ids
        )

    def order_by(self, *args):
        return self

    def count(self):
        return len(self.instance_ids)

    def iterator(self, chunk_size):
        return iter(self.instance_ids)

    def __getitem__(self, item):
        return QuerySetStub(self.instance_ids[item])


def test_iterators_exclude_instances_completed_by_their_phase(caplog):
    command = Command.__new__(Command)
    command.dev_mode = False
    command.run_state = RunState(
        configuration=CONFIGURATION,
        started_at=datetime.datetime.now(),
        completed_ids={"validation": {1}, "recalculation": {2}},
    )
    command._base_qs = lambda: QuerySetStub([1, 2, 3])

    assert QuerySetStub([1, 2, 3])[1:].instance_ids == [2, 3]
    assert QuerySetStub([1, 2, 3]).exclude() is not None

    with caplog.at_level(logging.INFO):
        validation_total, validation_instances = command.iter_instances_for_validation()
        recalculation_total, recalculation_instances = (
            command.iter_instances_for_miscalculation()
        )

    assert validation_total == 2
    assert list(validation_instances) == [2, 3]
    assert recalculation_total == 2
    assert list(recalculation_instances) == [1, 3]
    assert "Skipping 1 instances already checked for validation" in caplog.messages
    assert "Skipping 1 instances already checked or fixed" in caplog.messages


def test_restored_results_populate_existing_excel_sheets(tmp_path):
    command = Command.__new__(Command)
    command.stats = defaultdict(lambda: defaultdict(list))
    command.run_state = RunState(
        configuration=CONFIGURATION,
        started_at=datetime.datetime.now(),
        results={
            ("recalculation", 1): [
                _stats_entry(1),
                _stats_entry(1, event="fixed"),
            ]
        },
    )
    command.analyze_only = None
    command.excel_out = tmp_path / "recalculation.xlsx"

    command._restore_stats()
    command.log_to_excel(
        command.run_state.started_at, committed_to_db=True, did_fixes=True
    )

    workbook = openpyxl.load_workbook(command.excel_out)
    assert workbook.sheetnames == ["Info", "Analysis", "Fixes", "Statistics"]
    assert workbook["Analysis"].max_row == 2
    assert workbook["Fixes"].max_row == 2
    assert workbook["Statistics"].max_row == 2
