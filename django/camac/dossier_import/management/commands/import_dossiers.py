from django.core.management.base import BaseCommand

from camac.dossier_import.load_dossiers import perform_import


class Command(BaseCommand):
    help = "Import instances and cases from zip package"

    def add_arguments(self, parser):
        parser.add_arguments("path_to_file", nargs=1)

    def handle(self, *args, **options):
        with open(options["path_to_file"], "r") as f:
            perform_import(f)
