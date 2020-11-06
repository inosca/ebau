from pathlib import Path

from django.core.management.base import BaseCommand

from camac.data_migration.rsta_import import Importer


class Command(BaseCommand):
    help = """Import RSTA instances from prefecta application.

    Accepts a directory or JSON-files directly."""

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            metavar="PATH",
            type=Path,
            help="Path to directory or JSON file",
        )

    def handle(self, *args, **options):
        path = options["path"]

        importer = Importer(path)
        importer.run()
