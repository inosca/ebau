import os
import re
import signal
from datetime import datetime

import psutil
from django import db
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create and restore snaphsots of the development database"
    SNAP_PREFIX = "dbsnap_"

    def add_arguments(self, parser):
        parser.add_argument(
            "--create",
            action="store_true",
            dest="create",
            default=None,
            help="Create a snapshot DB",
            required=False,
        )
        parser.add_argument(
            "--restore",
            action="store_true",
            dest="restore",
            default=None,
            help="Restore given DB snapshot",
            required=False,
        )
        parser.add_argument(
            "--latest",
            action="store_true",
            dest="latest",
            default=None,
            help="Select the latest snapshot (only automatic snapshots are considered)",
            required=False,
        )
        parser.add_argument(
            "--list",
            action="store_true",
            dest="list",
            help="List all snapshots",
            required=False,
        )
        parser.add_argument(
            "--cleanup",
            action="store_true",
            dest="cleanup",
            help=(
                "Delete snapshots. If --name is given, only that "
                "snapshot is deleted, otherwise all are"
            ),
            required=False,
        )

        parser.add_argument(
            "--name",
            required=False,
            default=None,
            help="Name of the snapshot to create or restore (or delete in --cleanup)",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.main_db = db.connections["default"]

    def handle(self, *args, **options):  # noqa: C901
        do_create = options.get("create")
        do_list = options.get("list")
        do_restore = options.get("restore")
        do_cleanup = options.get("cleanup")

        if not settings.DEBUG:
            print(
                "DEBUG is off. For safety reasons, this tool won't run outside of dev env!"
            )
            return

        snap_name = self._get_name(options)

        if not snap_name:
            return

        self.prefixed_snap_name = self.SNAP_PREFIX + snap_name
        self.db_name = settings.DATABASES["default"]["NAME"]

        settings.DATABASES["snapshot"] = {
            **settings.DATABASES["default"],
            "NAME": self.prefixed_snap_name,
        }
        self.snap_db = db.connections["snapshot"]

        if do_create and do_restore:
            self.stderr.write("Can't restore and create at the same time.\n")
            return

        if do_create:
            if snap_name in self._list():
                print(f"Snapshot {snap_name} already exists, cannot create it again")
                return
            self._make_copy(self.main_db, self.db_name, self.prefixed_snap_name)
            self._reconnect_existing_django_procs()
        elif do_restore:
            if not options.get("name") and not options.get("latest"):
                print("For restore, you MUST pass in a snapshot name")
                return
            if snap_name not in self._list():
                print(f"Snapshot {snap_name} does not exist. Check with --list")
                return
            self._drop_main()
            self._make_copy(self.snap_db, self.prefixed_snap_name, self.db_name)

            self._reconnect_existing_django_procs()
        elif do_list:
            self._print_list()

        elif do_cleanup:
            if options["name"]:
                self._cleanup([options["name"]])
            else:
                self._cleanup(self._list())

        else:
            self.print_help("manage.py", "snapdb")

    def _get_name(self, options):
        snap_name = options["name"] or self._make_name()
        if options["name"] and options["latest"]:
            print("Can't do --latest and --name at the same time")
            return
        if options["latest"]:
            snap_name = self._get_latest()
        return snap_name

    def _cleanup(self, to_delete):
        for dbname in to_delete:
            self._drop_snapshot(dbname)

    def _get_latest(self):
        all_snaps = self._list()
        timestamped = [
            snap for snap in all_snaps if re.match(r"\d{4}_\d{2}_\d{2}", snap)
        ]
        return sorted(timestamped)[-1]

    def _reconnect_existing_django_procs(self):
        # manage.py has a signal handler that reconnects
        # the DB on SIGUSR2
        for proc in psutil.process_iter():
            cmdline = proc.cmdline()
            if (
                "manage.py" in cmdline
                or "./manage.py" in cmdline
                and proc.pid != os.getpid()  # don't signal self
            ):
                proc.send_signal(signal.SIGUSR2)

        pass

    def _print_list(self):
        snaps = self._list()
        for snap in snaps:
            name = snap.replace(self.SNAP_PREFIX, "")
            print(f" * {name}")
        if not snaps:
            print("There are currently no snapshots")

    def _list(self):
        with self.main_db.cursor() as curs:
            curs.execute(
                f"""
                SELECT datname FROM pg_database
                WHERE datname LIKE '{self.SNAP_PREFIX}%'
                """
            )
            # we only do the prefix on SQL level, everything else deals
            # with un-prefixed snapshot names
            snaps = sorted(
                [snap.replace(self.SNAP_PREFIX, "") for snap, *_ in curs.fetchall()]
            )

        return snaps

    def _disconnect_others(self, conn):
        # Drop all existing connections to avoid interference
        with conn.cursor() as curs:
            curs.execute(
                """
                SELECT pg_terminate_backend(pg_stat_activity.pid)
                FROM pg_stat_activity
                WHERE pid <> pg_backend_pid();
                """
            )

    def _make_copy(self, conn, from_db, to_db):
        self._disconnect_others(conn)
        with conn.cursor() as curs:
            # Create the snapshot database
            curs.execute(
                f"""
                CREATE DATABASE {to_db} with template {from_db};
                """
            )

    def _drop_main(self):
        self._disconnect_others(self.snap_db)
        with self.snap_db.cursor() as curs:
            curs.execute(f"DROP DATABASE {self.db_name};")

    def _drop_snapshot(self, name):
        # No disconnect required, snap dbs shouldn't have any users
        with self.main_db.cursor() as curs:
            curs.execute(f"DROP DATABASE {self.SNAP_PREFIX}{name};")

    def _make_name(self):
        now = datetime.now()
        return (
            now.isoformat(timespec="minutes", sep="_")
            .replace(":", "_")
            .replace("-", "_")
        )
