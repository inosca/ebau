from django.core.management.commands import flush as django_flush


class Command(django_flush.Command):
    help = """
    Run the Django flush as usual, but cascade the TRUNCATE.

    Tables owned by the Elixir app live in the same database and have foreign
    keys into Django tables (e.g. user_identities -> "USER"). PostgreSQL
    refuses to truncate a referenced table unless the referencing tables are
    truncated as well, which cascading takes care of.

    This option was previously available in the flush command directly but
    was removed in Django 3.1: https://docs.djangoproject.com/en/5.2/releases/3.1/#:~:text=allow_cascade%20argument%20of%20DatabaseOperations.sql_flush%28%29%20is%20now%20a
    """

    def handle(self, **options):
        options.setdefault("allow_cascade", True)

        return super().handle(**options)
