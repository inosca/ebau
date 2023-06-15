from django.core.management.base import BaseCommand
from django.db import transaction
from tqdm import tqdm

from camac.user.models import User, UserGroup, UserGroupLog


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", "-d", dest="dry", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        user_groups = UserGroup.objects.filter(created_by__isnull=True)

        sid = transaction.savepoint()

        for user_group in tqdm(user_groups):
            log = (
                UserGroupLog.objects.filter(
                    action="i",
                    field1="USER_ID",
                    id1=user_group.user_id,
                    field2="GROUP_ID",
                    id2=user_group.group_id,
                )
                .order_by("-modification_date")
                .only("modification_date", "user_id")
                .first()
            )

            if not log:
                continue

            try:
                user = User.objects.get(pk=log.user_id)
                user_group.created_by = user
            except User.DoesNotExist:
                # This should only happen on the test system as we removed
                # almost all data once but did not truncate the user group log.
                tqdm.write(
                    self.style.WARNING(f"No user with the ID {log.user_id} found")
                )

            user_group.created_at = log.modification_date
            user_group.save()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)
