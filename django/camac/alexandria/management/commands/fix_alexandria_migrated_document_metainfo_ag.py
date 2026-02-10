from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from tqdm import tqdm

from camac.instance.models import Instance


class Command(BaseCommand):
    """
    Fix missing caluma-document-id in metainfo for migrated AG dossiers documents.

    This is needed to show them in the portal.
    """

    help = "Fix missing caluma-document-id in Alexandria document metainfo for migrated AG dossiers"

    # Migration form slugs for kt_ag
    MIGRATION_FORM_SLUGS = [
        "reklame-migration",
        "vorentscheid-migration",
        "baugesuch-migration",
        "uvp-migration",
        "pgv-migration",
        "anfrage-migration",
    ]

    # Categories to update
    MIGRATION_CATEGORIES = [
        "beilagen-zum-gesuch-grundstuecksangaben",
        "beilagen-zum-gesuch-gutachten-nachweise-begruendungen",
        "beilagen-zum-gesuch-brandschutz",
        "beilagen-zum-gesuch-weitere-gesuchsunterlagen",
        "beilagen-zum-gesuch-eingabequittung",
    ]

    def add_arguments(self, parser):
        parser.add_argument(
            "--commit",
            dest="commit",
            action="store_true",
            default=False,
            help="Actually commit the changes to the database (default is dry-run)",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        commit = options["commit"]
        sid = transaction.savepoint()

        self.stdout.write(
            self.style.WARNING(
                "Fixing missing caluma-document-id in Alexandria metainfo for migrated AG dossiers..."
            )
        )

        if not commit:
            self.stdout.write(
                self.style.WARNING(
                    "Running in DRY-RUN mode. Use --commit to apply changes."
                )
            )

        # Build query for all migration form slugs
        form_query = Q()
        for slug in self.MIGRATION_FORM_SLUGS:
            form_query |= Q(case__document__form__slug=slug)

        # base queryset for migrated instances
        migrated_instances_queryset = (
            Instance.objects.filter(form_query)
            .exclude(case__isnull=True)
            .exclude(case__document__isnull=True)
        )

        total_instances = migrated_instances_queryset.count()
        self.stdout.write(
            self.style.SUCCESS(f"Found {total_instances} migrated instances to process")
        )

        if total_instances == 0:
            self.stdout.write(self.style.SUCCESS("No instances to process."))
            return

        updated_documents = 0
        processed_instances = 0

        batch_size = 100

        # progress bar for processing instances
        with tqdm(total=total_instances, desc="Processing instances") as pbar:
            offset = 0

            while offset < total_instances:
                instance_batch = list(
                    migrated_instances_queryset.select_related(
                        "case",
                        "case__document",
                        "case__document__form",
                    ).prefetch_related(
                        "alexandria_instance_documents__document__category"
                    )[offset : offset + batch_size]
                )

                if not instance_batch:
                    break

                for instance in instance_batch:
                    result = self._process_instance([instance], commit)
                    updated_documents += result["updated"]
                    processed_instances += result["processed"]
                    pbar.update(1)

                offset += batch_size

        # Summary
        self.stdout.write(self.style.SUCCESS("\n" + "=" * 60))
        self.stdout.write(
            self.style.SUCCESS(f"Processed {processed_instances} instances")
        )
        self.stdout.write(self.style.SUCCESS(f"Updated documents: {updated_documents}"))
        self.stdout.write(self.style.SUCCESS("=" * 60))

        if commit:
            transaction.savepoint_commit(sid)
            self.stdout.write(
                self.style.SUCCESS("\nChanges have been committed to the database.")
            )
        else:
            transaction.savepoint_rollback(sid)
            self.stdout.write(
                self.style.WARNING(
                    "\nDRY-RUN: No changes were made. Use --commit to apply changes."
                )
            )

    def _process_instance(self, instances, commit):
        """Process a batch of instances and return statistics."""
        updated = 0
        processed = 0

        # Process each instance
        for instance in instances:
            processed += 1
            caluma_document_id = str(instance.case.document.pk)

            for instance_doc in instance.alexandria_instance_documents.all():
                document = instance_doc.document

                if (
                    document.category.slug not in self.MIGRATION_CATEGORIES
                    or "caluma-document-id" in document.metainfo
                ):
                    continue

                # Add the missing caluma-document-id
                document.metainfo["caluma-document-id"] = caluma_document_id
                document.save()
                updated += 1

                if commit and updated % 50 == 0:
                    self.stdout.write(
                        self.style.SUCCESS(f"Progress: {updated} documents updated...")
                    )

        return {"updated": updated, "processed": processed}
