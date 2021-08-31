from django.core.management.base import BaseCommand

from camac.parashift.parashift import (
    ParashiftDataError,
    ParashiftImporter,
    ParashiftValidationError,
)


class Command(BaseCommand):
    """Import dossiers from parashift."""

    help = "Import dossiers from parashift."

    def add_arguments(self, parser):
        parser.add_argument("from_id", type=int, help="Parashift ID starting with")
        parser.add_argument("to_id", type=int, help="Parashift ID ending with")

    def handle(self, *args, **options):
        from_id = options.get("from_id")
        to_id = options.get("to_id")
        client = ParashiftImporter()
        try:
            client.run(from_id, to_id)
        except (ParashiftDataError, ParashiftValidationError) as e:
            self.stderr.write(f"Couldn't import dossiers: {e.args[0]}")
