import itertools

from alexandria.core.models import Document
from django.core.management.base import BaseCommand
from django.db import connection
from django.db.models import Exists, OuterRef
from django.utils.timezone import now
from tqdm import tqdm

from camac.alexandria_migration.domain_logic import (
    AnnotateDocumentsMigrator,
    CommunicationLinksMigrator,
    CreateDocumentsMigrator,
    DuplicateDocumentsMigrator,
)
from camac.alexandria_migration.models import MigrationLog, MigrationRun
from camac.alexandria_migration.utils import humanize_timedelta
from camac.communications.models import CommunicationsAttachment
from camac.instance.models import Instance


class Command(BaseCommand):
    help = "Migrate legacy documents module to alexandria"

    def add_arguments(self, parser):
        parser.add_argument("--from", dest="from", type=int, default=None)
        parser.add_argument("--to", dest="to", type=int, default=None)
        parser.add_argument("--batch-size", dest="batch_size", type=int, default=100)
        parser.add_argument("--limit", dest="limit", type=int, default=None)
        parser.add_argument(
            "--no-parallel",
            dest="no_parallel",
            action="store_true",
            default=False,
        )
        parser.add_argument(
            "--workers",
            dest="workers",
            type=int,
            default=0,
            help="Number of workers. Defaults to number of CPUs+1",
        )

        subparsers = parser.add_subparsers(title="sub-commands", required=True)

        reset = subparsers.add_parser(
            "reset",
            help="Reset all existing alexandria data",
        )
        reset.set_defaults(method=self.reset)

        create_documents = subparsers.add_parser(
            "create_documents",
            help="Create alexandria documents and files from attachments (First stage)",
        )
        create_documents.set_defaults(method=self.create_documents)
        duplicate_documents = subparsers.add_parser(
            "duplicate_documents",
            help="Duplicate alexandria documents of attachments in "
            "multiple sections (Second stage)",
        )
        duplicate_documents.set_defaults(method=self.duplicate_documents)
        fix_communication_links = subparsers.add_parser(
            "fix_communication_links",
            help="Fix links from communications module attachments (Last stage)",
        )
        fix_communication_links.set_defaults(method=self.fix_communication_links)

        annotate = subparsers.add_parser(
            "annotate",
            help="Annotate migrated documents: Create thumbnails, checksums, index for FTS",
        )
        annotate.set_defaults(method=self.annotate_documents)

    def handle(self, method, *args, **options):
        command = method.__name__

        if command == "reset":
            return method(*args, **options)

        try:
            self.run = MigrationRun.objects.create(command=command)

            method(*args, **options)

            self.run.status = MigrationRun.Status.DONE
        except Exception as e:
            self.run.status = MigrationRun.Status.FAILED
            raise e
        except KeyboardInterrupt:
            self.run.status = MigrationRun.Status.CANCELED
        finally:
            if self.run._should_delete:
                # This happens if there are no instances selected
                self.run.delete()
                return  # noqa: B012

            self.run.ended_at = now()
            self.run.save()

            self.stdout.write(self.run.summary())

    def filter_instances(self, instances, options):
        instances = instances.order_by("pk")

        if _from := options.get("from"):
            instances = instances.filter(pk__gte=_from)

        if to := options.get("to"):
            instances = instances.filter(pk__lte=to)

        if limit := options.get("limit"):
            instances = instances[:limit]

        return instances.values_list("pk", flat=True)

    def reset(self, *args, **options):
        """Reset all alexandria data including migration runs and logs."""

        self.stdout.write(self.style.WARNING("Resetting old alexandria data..."))

        start = now()

        with connection.cursor() as cursor:
            cursor.execute("""
                BEGIN;
                UPDATE
                    communications_communicationsattachment
                SET
                    alexandria_file_id = NULL
                WHERE
                    document_attachment_id IS NOT NULL;
                DELETE FROM alexandria_migration_migrationlog;
                DELETE FROM alexandria_migration_migrationrun;
                DELETE FROM instance_instancealexandriadocument;
                DELETE FROM alexandria_core_file;
                DELETE FROM alexandria_core_document_marks;
                DELETE FROM alexandria_core_document;
                COMMIT;
            """)

        self.stdout.write(
            self.style.SUCCESS(
                f"Alexandria data successfully resetted in {humanize_timedelta(now() - start)}"
            )
        )

    def create_documents(self, *args, **options):
        instances = self.filter_instances(
            Instance.objects.exclude(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED,
                        instance_id=OuterRef("pk"),
                    )
                )
            ),
            options,
        )

        if not len(instances):
            self.stdout.write(
                self.style.ERROR(
                    "There are no eligible instances to create alexandria documents. Please adjust your filters."
                )
            )
            self.run._should_delete = True
            return

        batch_size = options.get("batch_size")

        self.stdout.write(
            self.style.SUCCESS(
                f"Starting migration of {len(instances)} instances chunked into {batch_size} instance batches..."
            )
        )

        with tqdm(total=len(instances)) as bar:
            for batch in itertools.batched(instances, batch_size):
                CreateDocumentsMigrator(batch, self.run).process()

                bar.update(len(batch))

        self.stdout.write(
            self.style.SUCCESS(
                f"Migration of {len(instances)} instances was successful"
            )
        )

    def duplicate_documents(self, *args, **options):
        instances = self.filter_instances(
            Instance.objects.filter(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED,
                        instance_id=OuterRef("pk"),
                    )
                )
                & Exists(
                    Document.objects.filter(
                        metainfo__has_key="duplicate-to",
                        instance_document__instance_id=OuterRef("pk"),
                    )
                )
            ).exclude(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_DUPLICATED,
                        instance_id=OuterRef("pk"),
                    )
                )
            ),
            options,
        )

        if not len(instances):
            self.stdout.write(
                self.style.ERROR(
                    "There are no eligible instances for duplicating alexandria documents. "
                    "Please adjust your filters or run the prerequisite commands."
                )
            )
            self.run._should_delete = True
            return

        batch_size = options.get("batch_size")

        self.stdout.write(
            self.style.SUCCESS(
                f"Starting duplication of documents on {len(instances)} instances chunked into {batch_size} instance batches..."
            )
        )

        with tqdm(total=len(instances)) as bar:
            for batch in itertools.batched(instances, batch_size):
                DuplicateDocumentsMigrator(batch, self.run).process()

                bar.update(len(batch))

        self.stdout.write(
            self.style.SUCCESS(
                f"Duplication of documents on {len(instances)} instances was successful"
            )
        )

    def fix_communication_links(self, *args, **options):
        instances = self.filter_instances(
            Instance.objects.filter(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED,
                        instance_id=OuterRef("pk"),
                    )
                )
                & Exists(
                    CommunicationsAttachment.objects.filter(
                        document_attachment__isnull=False,
                        message__topic__instance_id=OuterRef("pk"),
                    )
                )
            ).exclude(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_COMMUNICATION_LINKS_FIXED,
                        instance_id=OuterRef("pk"),
                    )
                )
            ),
            options,
        )

        if not len(instances):
            self.stdout.write(
                self.style.ERROR(
                    "There are no eligible instances for fixing communication links. "
                    "Please adjust your filters or run the prerequisite commands. "
                    "(Note for small instance ranges, it could well be that there are no "
                    "comms attachments to re-link)"
                )
            )
            self.run._should_delete = True
            return

        batch_size = options.get("batch_size")

        self.stdout.write(
            self.style.SUCCESS(
                f"Fixing communication module links on {len(instances)} instances "
                f"chunked into {batch_size} instance batches..."
            )
        )

        with tqdm(total=len(instances)) as bar:
            for batch in itertools.batched(instances, batch_size):
                CommunicationLinksMigrator(batch, self.run).process()

                bar.update(len(batch))

        self.stdout.write(
            self.style.SUCCESS(
                f"Fixing of communications module links on {len(instances)} instances was successful"
            )
        )

    def annotate_documents(self, *args, **options):
        instances = self.filter_instances(
            # Eligible instances: Are created from the migration, are duplicated,
            # and not yet annotated. Note we do not care about the communication
            # link status here - that may happen at the same time, before, or after,
            # it doesn't matter.
            Instance.objects.filter(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_CREATED,
                        instance_id=OuterRef("pk"),
                    )
                )
                & Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_DUPLICATED,
                        instance_id=OuterRef("pk"),
                    )
                )
            ).exclude(
                Exists(
                    MigrationLog.objects.filter(
                        type=MigrationLog.Type.INSTANCE_DOCUMENTS_ANNOTATED,
                        instance_id=OuterRef("pk"),
                    )
                )
            ),
            options,
        )

        if not len(instances):
            self.stdout.write(
                self.style.ERROR(
                    "There are no eligible instances for annotating. Please adjust your filters or run the prequisite commands."
                )
            )
            self.run._should_delete = True
            return

        batch_size = options.get("batch_size")

        self.stdout.write(
            self.style.SUCCESS(
                f"Annotating thumbnails, FTS indexes, checksums on {len(instances)} instances chunked into {batch_size} instance batches..."
            )
        )

        with tqdm(total=len(instances)) as bar:
            for batch in itertools.batched(instances, batch_size):
                AnnotateDocumentsMigrator(
                    batch,
                    self.run,
                    workers=options["workers"],
                    no_parallel=options["no_parallel"],
                ).process()
                bar.update(len(batch))

        self.stdout.write(
            self.style.SUCCESS(
                f"Annotation of {len(instances)} instances was successful"
            )
        )
