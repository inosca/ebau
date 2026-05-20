from django.conf import settings
from django.db import migrations
from django.db.utils import IntegrityError, ProgrammingError

INDEX_NAME = "unique_dossier_number"


def migrate(apps, schema_editor):
    if settings.APPLICATION_NAME == "kt_bern":
        # Kt. BE doesn't use the dossier-number meta property but instead uses
        # ebau-number which must not be unique - therefore, we skip the whole
        # migration.
        return

    with schema_editor.connection.cursor() as cursor:
        try:
            cursor.execute(
                f"""
                CREATE UNIQUE INDEX {INDEX_NAME} ON caluma_workflow_case ((meta->>'dossier-number'));
                """
            )
        except IntegrityError:
            print(
                f'\nWARNING: Unique index "{INDEX_NAME}" could not be created '
                "because of an integrity error. This means, that there are "
                "cases with duplicate dossier numbers. To fix this, run the "
                "`fix_duplicate_identifiers` management command. After the "
                "conflicts are fixed, you can create the index with the "
                "`create_unique_dossier_identififier` management command."
            )
            schema_editor.connection._rollback()
        except ProgrammingError:
            print(
                f'\nINFO: Unique index "{INDEX_NAME}" could not be created '
                "because it already exists. No further action necessary."
            )
            schema_editor.connection._rollback()


def revert(apps, schema_editor):
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"DROP INDEX IF EXISTS {INDEX_NAME};")


class Migration(migrations.Migration):
    dependencies = [
        ("caluma", "0002_delete_historicalinquiry_historicalinquiry"),
    ]

    operations = [
        migrations.RunPython(migrate, revert),
    ]
