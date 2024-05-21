from django.core.management.base import BaseCommand
from django.db import transaction

from camac.user.models import User, UserGroup


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--dry", dest="dry", action="store_true", default=False)
        parser.add_argument(
            "--verbose", dest="verbose", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        self.verbose = options.get("verbose", False)

        self.set_default_group()

        if options["dry"]:
            transaction.savepoint_rollback(sid)
        else:
            transaction.savepoint_commit(sid)

    def set_default_group(self):
        """Set the a default group for all users that don't have any."""
        users = User.objects.filter(groups__isnull=False).distinct()
        for u in users:
            if UserGroup.objects.filter(user=u, default_group=1).count() == 0:
                first = UserGroup.objects.filter(user=u).first()
                first.default_group = 1
                first.save()
                if self.verbose:
                    print(f"set default group of {u.email} to {first.group.get_name()}")
