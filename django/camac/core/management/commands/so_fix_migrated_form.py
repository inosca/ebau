from caluma.caluma_form.models import Document, Form
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = """ebauSO: Revert unnecessary versioning of migriertes-dossier."""

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    @transaction.atomic
    def handle(self, *args, **options):
        sid = transaction.savepoint()

        try:
            form = Form.objects.get(slug="migriertes-dossier")
            documents = Document.objects.filter(form__slug="migriertes-dossier-v2")
            for document in documents:
                try:
                    old_form = document.form
                    document.form = form
                    document.save()
                    print(
                        f"Changed: {document.pk} from {old_form.pk} to {document.form.pk}"
                    )
                except Exception as e:
                    print(f"Failed: {document.pk}, {document.form.pk}: {e}")

            form = Form.objects.get(slug="parzelle-tabelle")
            documents = Document.objects.filter(form__slug="parzelle-tabelle-v2")
            for document in documents:
                try:
                    old_form = document.form
                    document.form = form
                    document.save()
                    print(
                        f"Changed: {document.pk} from {old_form.pk} to {document.form.pk}"
                    )
                except Exception as e:
                    print(f"Failed: {document.pk}, {document.form.pk}: {e}")

            f = Form.objects.filter(slug="migriertes-dossier-v2")
            if f.count():
                f.first().delete()
                print("Deleted: migriertes-dossier-v2")
            f = Form.objects.filter(slug="parzelle-tabelle-v2")
            if f.count():
                f.first().delete()
                print("Deleted: parzelle-tabelle-v2")

            if options["commit"]:
                transaction.savepoint_commit(sid)
            else:
                transaction.savepoint_rollback(sid)
                print("Run with --commit to apply changes")
        except Exception as e:
            transaction.savepoint_rollback(sid)
            print(f"Reverting changes due to error: {e}")
