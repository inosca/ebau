from django.conf import settings
from django.core.management.commands import migrate as django_migrate
from django.db.transaction import atomic, get_connection


class Command(django_migrate.Command):
    help = """Run the Django migrations as usual, but lock the
    migration table while doing it.

    This will avoid having partial migration issues if multiple containers
    startup at the same time and want to migrate the DB.
    """

    @atomic
    def handle(self, *args, **options):
        for db in settings.DATABASES:
            try:
                cursor = get_connection(db).cursor()
                cursor.execute("LOCK TABLE django_migrations")
            finally:
                if cursor and not cursor.closed:
                    cursor.close()

        # Migration tables are now locked, no other process can mess with them
        return super().handle(*args, **options)
