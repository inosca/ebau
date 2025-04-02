import datetime

from django.core.management.base import BaseCommand
from django.db import transaction

from camac.core.models import Sanction as LegacySanction
from camac.sanctions.models import Sanction


class Command(BaseCommand):
    help = "Migrate old PHP-based sanctions in Uri to new sanctions"

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Create data for real",
        )

    @transaction.atomic()
    def handle(self, *args, **options):
        tid = transaction.savepoint()

        sanctions = [
            sanction
            for legacy_sanction in LegacySanction.objects.all()
            if (sanction := self.create_sanction(legacy_sanction))
        ]
        self.stdout.write(f"Saving {len(sanctions)} sanctions to database")
        if len(sanctions):
            Sanction.objects.bulk_create(sanctions)

        if options["commit"]:
            transaction.savepoint_commit(tid)
        else:
            transaction.savepoint_rollback(tid)

    def create_sanction(self, legacy_sanction):
        migration_date = datetime.datetime.now(tz=datetime.timezone.utc)

        new_sanction = Sanction.objects.filter(
            meta__legacy_sanction__sanction_id=legacy_sanction.sanction_id,
        ).first()
        if new_sanction:
            self.stdout.write(
                f"Skipping legacy sanction {legacy_sanction.sanction_id} (sanction {new_sanction.id}, migration date {migration_date.isoformat()})"
            )
            return None

        self.stdout.write(
            f"Preparing migration of legacy sanction {legacy_sanction.sanction_id}"
        )
        start_date_str = legacy_sanction.start_date.strftime("%d.%m.%Y")
        return Sanction(
            instance=legacy_sanction.instance,
            name=f"Verfügung/Stellungnahme vom {start_date_str}",
            description=legacy_sanction.text,
            created_by_service=legacy_sanction.service,
            created_by_user=legacy_sanction.user,
            assigned_service=(
                legacy_sanction.control_instance
                if legacy_sanction.control_instance
                else legacy_sanction.service
            ),
            control_notes=legacy_sanction.notice,
            **(
                {
                    "controlled_at": legacy_sanction.end_date
                    if legacy_sanction.end_date
                    else migration_date,
                    "controlled_by_user": legacy_sanction.finished_by_user,
                }
                if legacy_sanction.is_finished
                else {}
            ),
            control_step="variabel",
            meta={
                "migration-date": migration_date.isoformat(),
                "legacy_sanction": {
                    "sanction_id": legacy_sanction.sanction_id,
                    "start_date": isoformat(legacy_sanction.start_date),
                    "deadline_date": isoformat(legacy_sanction.deadline_date),
                    "end_date": isoformat(legacy_sanction.end_date),
                },
            },
        )


def isoformat(dt):
    return dt.isoformat() if dt else ""
