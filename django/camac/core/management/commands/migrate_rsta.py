from pathlib import Path

from django.core.management.base import BaseCommand

from camac.data_migration.rsta_import import Importer


class Command(BaseCommand):
    help = """Import RSTA instances from prefecta application.

    Accepts a directory or JSON-files directly.
    Documents have to be in a subfolder (name = gNr) of the JSON-files.
    """

    # Example: ./manage.py migrate_rsta /data
    # * /data
    # | * foo.json (gNr = 123)
    # | ...
    # | * /123
    #   | - my_document.doc
    #   | ...

    def add_arguments(self, parser):
        parser.add_argument(
            "path",
            metavar="PATH",
            type=Path,
            help="Path to directory or JSON file",
        )

        parser.add_argument(
            "--state-file",
            type=Path,
            default=None,
            help="Path to state file of previous runs, default: migration_rsta_state.pickle",
        )

        parser.add_argument(
            "--document-path",
            type=Path,
            default=None,
            help="Path to document folders, default: Same as PATH",
        )

        parser.add_argument(
            "--no-reimport",
            default=True,
            dest="reimport",
            action="store_false",
            help="Disable reimport of existing (failed) instances.",
        )

        parser.add_argument(
            "--debug",
            action="store_true",
            default=False,
            help="Throw exception and stop if error occures",
        )

        parser.add_argument(
            "--zustaendig-only",
            action="store_true",
            default=False,
            help="Import only zustaendig as tags, requires existing instances with geschaefts_nr.",
        )

        parser.add_argument(
            "--documents-only",
            action="store_true",
            default=False,
            help="Import only documents, requires existing instances with geschaefts_nr.",
        )

    def handle(self, *args, **options):
        path = options["path"].resolve()

        kwargs = {
            k: v.resolve()
            for k, v in options.items()
            if k in ["state_file", "document_path"] and v
        }

        if options["zustaendig_only"]:
            kwargs.setdefault(
                "state_file", Path.cwd() / "migrate_rsta_zustaendig.pickle"
            )
            importer = Importer(path, **kwargs)
            print('Importing only "zustaendig: user" tags')
            importer.set_zustaendig(options["reimport"], options["debug"])
            return

        if options["documents_only"]:
            kwargs.setdefault(
                "state_file", Path.cwd() / "migrate_rsta_documents.pickle"
            )
            importer = Importer(path, **kwargs)
            print("Importing only missing documents")
            importer.reimport_documents(options["reimport"], options["debug"])
            return

        importer = Importer(path, **kwargs)
        importer.run(options["reimport"], options["debug"])
