import csv
import json

from caluma.caluma_form import api as form_api
from caluma.caluma_form.models import Answer, Question
from caluma.caluma_user.models import BaseUser
from django.core.management.base import BaseCommand
from django.db import transaction

from camac.instance.models import Instance

GIS_MAP_QUESTION_SLUG = "gis-map"


def parse_coordinate(value):
    """Parse a coordinate from the CSV.

    Values use "." as thousands separator (e.g. "2.661.456" -> 2661456).
    Returns None for empty values.
    """

    cleaned = (value or "").strip()
    if not cleaned:
        return None
    return int(cleaned.replace(".", ""))


class Command(BaseCommand):
    help = """Correct GIS coordinates of kt_ag instances based on a CSV file.

    The CSV must contain at least the columns GES_ID, X geändert
    and Y geändert. Without --commit the command performs a dry run
    and only logs the changes it would make.
    """

    def add_arguments(self, parser):
        parser.add_argument(
            "csv_file",
            type=str,
            help="Path to the CSV file with corrected coordinates",
        )
        parser.add_argument(
            "--commit",
            default=False,
            action="store_true",
            help="Persist the changes (default is a dry run)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        commit = options["commit"]
        csv_path = options["csv_file"]

        question = Question.objects.get(slug=GIS_MAP_QUESTION_SLUG)
        user = BaseUser()

        stats = {"updated": 0, "skipped": 0, "errors": 0}

        with open(csv_path, newline="", encoding="utf-8") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                self._process_row(row, question, user, commit, stats)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. updated={stats['updated']} "
                f"skipped={stats['skipped']} errors={stats['errors']}"
            )
        )

        if not commit:
            self.stdout.write(
                self.style.WARNING(
                    "Dry run – no changes were persisted. Re-run with --commit "
                    "to apply the changes."
                )
            )
            transaction.set_rollback(True)

    def _process_row(self, row, question, user, commit, stats):
        raw_id = (row.get("GES_ID") or "").strip()
        if not raw_id:
            return

        try:
            instance_id = int(raw_id)
        except ValueError:
            self.stderr.write(f"Invalid GES_ID {raw_id!r}, skipping")
            stats["errors"] += 1
            return

        try:
            x = parse_coordinate(row.get("X geändert"))
            y = parse_coordinate(row.get("Y geändert"))
        except ValueError:
            self.stderr.write(
                f"Instance {instance_id}: invalid coordinates "
                f"({row.get('X geändert')!r}, {row.get('Y geändert')!r}), skipping"
            )
            stats["errors"] += 1
            return

        if x is None or y is None:
            self.stdout.write(
                f"Instance {instance_id}: no corrected coordinates, skipping"
            )
            stats["skipped"] += 1
            return

        try:
            instance = Instance.objects.get(pk=instance_id)
        except Instance.DoesNotExist:
            self.stderr.write(f"Instance {instance_id}: not found, skipping")
            stats["errors"] += 1
            return

        document = instance.case.document
        answer = Answer.objects.filter(
            document=document, question_id=GIS_MAP_QUESTION_SLUG
        ).first()

        if not answer or not answer.value:
            self.stdout.write(
                f"Instance {instance_id}: no existing gis-map answer, skipping"
            )
            stats["skipped"] += 1
            return

        try:
            data = json.loads(answer.value)
        except (TypeError, ValueError):
            self.stderr.write(
                f"Instance {instance_id}: gis-map answer is not valid JSON, skipping"
            )
            stats["errors"] += 1
            return

        markers = data.get("markers") or []
        if not markers:
            self.stdout.write(
                f"Instance {instance_id}: gis-map answer has no markers, skipping"
            )
            stats["skipped"] += 1
            return

        if len(markers) > 1:
            self.stdout.write(
                self.style.WARNING(
                    f"Instance {instance_id}: gis-map answer has {len(markers)} "
                    "markers, updating only the first"
                )
            )

        old_x = markers[0].get("x")
        old_y = markers[0].get("y")
        markers[0]["x"] = x
        markers[0]["y"] = y
        data["markers"] = markers

        action = "Updating" if commit else "Would update"
        self.stdout.write(
            f"{action} instance {instance_id}: ({old_x}, {old_y}) -> ({x}, {y})"
        )

        if commit:
            form_api.save_answer(
                document=document,
                question=question,
                value=json.dumps(data),
                user=user,
            )

        stats["updated"] += 1
