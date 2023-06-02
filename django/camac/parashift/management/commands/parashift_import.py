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
        parser.add_argument(
            "bfs_nr",
            type=str,
            help="BFS number of the municipality to import (or KOOR_BG if importing as KOOR BG)",
        )

    def handle(self, *args, **options):
        from_id = options.get("from_id")
        to_id = options.get("to_id")
        bfs_nr = options.get("bfs_nr")
        client = ParashiftImporter(bfs_nr)

        try:
            client.run(from_id, to_id)
        except (ParashiftDataError, ParashiftValidationError) as e:
            self.stderr.write(f"Couldn't import dossiers: {e.args[0]}")
