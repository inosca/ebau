import os
import re
import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand

from camac.settings.env import ROOT_DIR

DEFAULT_OUTPUT = ROOT_DIR("../elixir-ebau/priv/repo/ebau_schema.sql")

VERSION_COMMENT_RE = re.compile(r"^-- Dumped .*\n", re.MULTILINE)


class Command(BaseCommand):
    help = "Dump the legacy database schema to the Elixir project's ebau_schema.sql"

    def add_arguments(self, parser):
        parser.add_argument(
            "--output",
            dest="output",
            type=str,
            default=DEFAULT_OUTPUT,
            help="Output path for the schema dump (default: elixir-ebau/priv/repo/ebau_schema.sql)",
        )

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]

        pg_dump_args = [
            "pg_dump",
            "--schema-only",
            "--no-owner",
            "--no-acl",
        ]

        if db.get("HOST"):
            pg_dump_args += ["-h", db["HOST"]]
        if db.get("PORT"):
            pg_dump_args += ["-p", str(db["PORT"])]
        if db.get("USER"):
            pg_dump_args += ["-U", db["USER"]]

        pg_dump_args.append(db["NAME"])

        env = os.environ.copy()
        if db.get("PASSWORD"):
            env["PGPASSWORD"] = db["PASSWORD"]

        result = subprocess.run(
            pg_dump_args,
            capture_output=True,
            text=True,
            env=env,
            check=True,
        )

        content = VERSION_COMMENT_RE.sub("", result.stdout)

        output_path = options["output"]
        with open(output_path, "w") as f:
            f.write(content)

        self.stdout.write(f"Legacy schema written to {output_path}")
