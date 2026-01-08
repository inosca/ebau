from caluma.caluma_form.models import Document
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db.models import Exists, OuterRef
from tqdm import tqdm

from camac.document.models import Attachment

MIGRATION_META_TIMESTAMP_KEY = "nfd-migrated-at"
MIGRATION_META_CLAIM_ID_KEY = "nfd-migrated-from-claimId"
SOURCE_FORM_ID = "nfd-tabelle"
FILL_DEMAND_FORM_ID = "fill-additional-demand"


class Command(BaseCommand):
    """
    How to use.

    pre-migration:

       python manage.py additional_demands_analyze_be --mode pre

    post migration with file check:

       python manage.py additional_demands_analyze_be --mode post --check-files

    post migration without file check:

       python manage.py additional_demands_analyze_be --mode post
    """

    help = "Verifies the integrity of the NFD migration. (Pre and Post checks)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--mode",
            type=str,
            choices=["pre", "post"],
            required=True,
            help="Specify 'pre' for source attachments file checks or 'post' for migration verification.",
        )
        parser.add_argument(
            "--check-files",
            action="store_true",
            help="If set in post mode, it will also verify file existence in storage.",
        )

    def handle(self, *args, **options):
        mode = options["mode"]
        should_check_files = options["check_files"]

        self.stdout.write(
            self.style.WARNING(
                f"\nSTARTING {mode.upper()}-MIGRATION INTEGRITY CHECKS...\n"
            )
        )

        errors = []
        successful = []

        if mode == "pre":
            checks = [
                ("Check source attachments files", self.check_source_attachments_files)
            ]
        else:
            checks = [
                ("Check migration integrity", self.check_migration_integrity),
                ("Check active init tasks", self.check_active_init_tasks),
                (
                    "Check migrated attachments reference",
                    self.check_migrated_attachments_reference,
                ),
            ]

            if should_check_files:
                self.stdout.write(
                    self.style.WARNING(" => File storage check will also be performed")
                )
                checks.append(
                    (
                        "Check migrated attachments files",
                        self.check_migrated_attachments_files,
                    )
                )

        for check_name, check_func in checks:
            if error := check_func():
                errors.append((check_name, error))
            else:
                successful.append(check_name)

        self.stdout.write("\n" + "====================================")
        if not errors:
            self.stdout.write(
                self.style.SUCCESS(f"  {mode.upper()}-MIGRATION VERIFICATION PASSED")
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"  VERIFICATION FAILED ({len(errors)} of {len(checks)} CHECK(S) FAILED)"
                )
            )

        for check_name in successful:
            self.stdout.write(f"  - {check_name}: OK")

        for check_name, error in errors:
            self.stdout.write(f"  - {check_name}: {error}")

    def check_migration_integrity(self):  # noqa: C901
        """
        Check migration integrity.

        Check method that is comparing eligible document ids to
        document ids referenced in the meta (MIGRATION_META_CLAIM_ID_KEY="nfd-migrated-from-claimId")
        of the migrated child cases and send-additional-demand work items respectively.
        """
        self.stdout.write(
            " => Checking Migration Integrity (Child Cases & 'Send' Work Items)..."
        )

        errors_found = []

        nfd_work_item = WorkItem.objects.filter(case_id=OuterRef("pk"), task_id="nfd")

        eligible_cases_qs = Case.objects.filter(
            Exists(nfd_work_item), instance__isnull=False
        ).exclude(workflow_id="migrated")

        source_data = Document.objects.filter(
            form_id=SOURCE_FORM_ID,
            family__work_item__task_id="nfd",
            family__work_item__case__in=eligible_cases_qs,
            answers__question_id="nfd-tabelle-behoerde",
            answers__value__isnull=False,
        ).values_list("pk", "family__work_item__case__instance__pk")

        eligible_source_map = {
            str(document_pk): str(instance_pk)
            for document_pk, instance_pk in source_data
        }
        eligible_source_document_ids = set(eligible_source_map.keys())

        child_case_data = Case.objects.filter(
            workflow_id=settings.ADDITIONAL_DEMAND["WORKFLOW"],
            **{"meta__has_key": MIGRATION_META_TIMESTAMP_KEY},
        ).values_list(f"meta__{MIGRATION_META_CLAIM_ID_KEY}", "instance__pk")

        migrated_child_map = {
            str(document_pk): str(instance_pk)
            for document_pk, instance_pk in child_case_data
            if document_pk
        }
        migrated_child_document_ids = set(migrated_child_map.keys())

        parent_work_item_document_ids = set(
            WorkItem.objects.filter(
                task_id=settings.ADDITIONAL_DEMAND["TASK"],
                child_case__isnull=False,
                **{"meta__has_key": MIGRATION_META_TIMESTAMP_KEY},
            ).values_list(f"meta__{MIGRATION_META_CLAIM_ID_KEY}", flat=True)
        )
        parent_work_item_document_ids = {
            str(doc_pk) for doc_pk in parent_work_item_document_ids if doc_pk
        }

        send_work_item_document_ids = set(
            WorkItem.objects.filter(
                task_id=settings.ADDITIONAL_DEMAND["SEND_TASK"],
                **{"meta__has_key": MIGRATION_META_TIMESTAMP_KEY},
            ).values_list(f"meta__{MIGRATION_META_CLAIM_ID_KEY}", flat=True)
        )

        send_work_item_document_ids = {
            str(doc_pk) for doc_pk in send_work_item_document_ids if doc_pk
        }

        eligible_source_count = len(eligible_source_document_ids)
        migrated_child_count = len(migrated_child_document_ids)

        self.stdout.write(f"   - Eligible Source Documents: {eligible_source_count}")
        self.stdout.write(f"   - Actual Migrated Documents: {migrated_child_count}")

        missing_migration_document_ids = (
            eligible_source_document_ids - migrated_child_document_ids
        )
        unexpected_migration_document_ids = (
            migrated_child_document_ids - eligible_source_document_ids
        )

        if (
            eligible_source_count != migrated_child_count
            or missing_migration_document_ids
            or unexpected_migration_document_ids
        ):
            error_msg = f"Count Mismatch: Expected {eligible_source_count}, Found {migrated_child_count}"
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))
            errors_found.append(error_msg)

            if missing_migration_document_ids:
                self.style.WARNING(
                    "    Claim Document IDs (Eligible but not migrated):"
                )
                for document_id in sorted(list(missing_migration_document_ids)):
                    instance_id = eligible_source_map.get(document_id)
                    self.stdout.write(
                        f"      - Claim Document ID: {document_id} (Instance ID : {instance_id})"
                    )

            if unexpected_migration_document_ids:
                self.style.WARNING("    Claim Document IDs (Migrated but unexpected):")
                for document_id in sorted(list(unexpected_migration_document_ids)):
                    instance_id = migrated_child_map.get(document_id)
                    self.stdout.write(
                        f"      - Claim Document ID: {document_id} (Instance ID : {instance_id})"
                    )

        else:
            self.stdout.write(
                self.style.SUCCESS("   All eligible claim documents have been migrated")
            )

        missing_send_items_document_ids = (
            migrated_child_document_ids - send_work_item_document_ids
        )

        send_work_item_count = len(send_work_item_document_ids)
        self.stdout.write(f"   - Actual Migrated Documents: {migrated_child_count}")
        self.stdout.write(f"   - 'Send' Work Items Found: {send_work_item_count}")

        if send_work_item_count != migrated_child_count:
            error_msg = f"Count Mismatch: Expected {migrated_child_count}, Found {send_work_item_count}"
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))
            errors_found.append(error_msg)

        if missing_send_items_document_ids:
            work_item_error_msg = f"Missing Work Items: {len(missing_send_items_document_ids)} migrated documents are missing the 'Send' Work Item."
            self.stdout.write(self.style.ERROR(f"   {work_item_error_msg}"))
            errors_found.append(work_item_error_msg)

            self.stdout.write(
                self.style.WARNING(
                    "    Migrated Claim Document IDs missing 'Send' Work Item:"
                )
            )
            for document_id in sorted(list(missing_send_items_document_ids)):
                instance_id = migrated_child_map.get(document_id)
                self.stdout.write(
                    f"      - Claim Document ID: {document_id} (Instance ID: {instance_id})"
                )

        elif len(send_work_item_document_ids) > 0:
            self.stdout.write(
                self.style.SUCCESS("   All migrated documents have a 'Send' Work Item.")
            )

        missing_parent_items_document_ids = (
            migrated_child_document_ids - parent_work_item_document_ids
        )

        parent_work_item_count = len(parent_work_item_document_ids)
        self.stdout.write(f"   - Actual Migrated Documents: {migrated_child_count}")
        self.stdout.write(f"   - 'Parent' Work Items Found: {parent_work_item_count}")

        if parent_work_item_count != migrated_child_count:
            error_msg = f"Count Mismatch: Expected {migrated_child_count}, Found {parent_work_item_count}"
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))
            errors_found.append(error_msg)

        if missing_parent_items_document_ids:
            work_item_error_msg = f"Missing Work Items: {len(missing_parent_items_document_ids)} migrated documents are missing the 'Parent' Work Item."
            self.stdout.write(self.style.ERROR(f"   {work_item_error_msg}"))
            errors_found.append(work_item_error_msg)

            self.stdout.write(
                self.style.WARNING(
                    "    Migrated Document IDs missing 'Parent' Work Item:"
                )
            )
            for document_id in sorted(list(missing_parent_items_document_ids)):
                instance_id = migrated_child_map.get(document_id)
                self.stdout.write(
                    f"      - Claim Document ID: {document_id} (Instance ID: {instance_id})"
                )

        elif len(parent_work_item_document_ids) > 0:
            self.stdout.write(
                self.style.SUCCESS(
                    "   All migrated documents have a 'Parent' Work Item."
                )
            )

        if errors_found:
            return "; ".join(errors_found)

        return None

    def check_active_init_tasks(self):
        self.stdout.write("\n => Checking Ready 'Init' Work Items...")
        errors_found = []
        target_states = [
            "subm",
            "circulation_init",
            "circulation",
            "coordination",
        ]

        relevant_cases_qs = (
            Case.objects.filter(
                instance__instance_state__name__in=target_states,
            )
            .exclude(workflow_id="migrated")
            .exclude(
                document__answers__question_id="is-paper",
                document__answers__value="is-paper-yes",
            )
        )

        active_cases_count = relevant_cases_qs.count()

        if active_cases_count == 0:
            self.stdout.write(f"   - No cases found in states {target_states}.")
            return None

        cases_with_valid_work_items = set(
            WorkItem.objects.filter(
                case__in=relevant_cases_qs,
                task_id=settings.ADDITIONAL_DEMAND["CREATE_TASK"],
                status=WorkItem.STATUS_READY,
            ).values_list("case_id", flat=True)
        )

        all_relevant_case_ids = set(relevant_cases_qs.values_list("pk", flat=True))
        missing_case_ids = all_relevant_case_ids - cases_with_valid_work_items
        unexpected_case_ids = cases_with_valid_work_items - all_relevant_case_ids

        count_valid = len(cases_with_valid_work_items)

        self.stdout.write(f"   - Active Cases ({target_states}): {active_cases_count}")
        self.stdout.write(f"   - With Ready 'Init' Work Item:    {count_valid}")

        if not missing_case_ids and not unexpected_case_ids:
            self.stdout.write(
                self.style.SUCCESS("   All active cases have a Ready 'Init' Work Item.")
            )

        if missing_case_ids:
            error_msg = f"Invalid State: {len(missing_case_ids)} active cases are missing a Ready 'Init' Work Item."
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))
            errors_found.append(error_msg)

            missing_instance_ids = Case.objects.filter(
                pk__in=missing_case_ids
            ).values_list("instance__pk", flat=True)

            self.stdout.write(
                self.style.WARNING(
                    "    Instance IDs with missing/non-ready 'Init' Work Item:"
                )
            )

            for instance_id in sorted(missing_instance_ids):
                self.stdout.write(f"      - Instance ID: {instance_id}")

        if unexpected_case_ids:
            error_msg = f"Invalid State: {len(unexpected_case_ids)} cases have a Ready 'Init' Work Item but should not."
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))
            errors_found.append(error_msg)

            unexpected_instance_ids = Case.objects.filter(
                pk__in=unexpected_case_ids
            ).values_list("instance__pk", flat=True)

            self.stdout.write(
                self.style.WARNING(
                    "    Instance IDs with ready 'Init' Work Item that should not have one:"
                )
            )

            for instance_id in sorted(unexpected_instance_ids):
                self.stdout.write(f"      - Instance ID: {instance_id}")

        if errors_found:
            return "; ".join(errors_found)

        return None

    def _verify_storage_files(self, attachments_qs):
        missing_data = []
        error_data = []
        errors_found = []

        for attachment in tqdm(attachments_qs, desc="Checking Attachment Files"):
            if attachment.path and attachment.path.name:
                instance_pk = attachment.instance.pk
                attachment_path = attachment.path.name
                try:
                    if not attachment.path.storage.exists(attachment_path):
                        missing_data.append(
                            (str(attachment.pk), str(instance_pk), str(attachment_path))
                        )
                except Exception as e:
                    tqdm.write(
                        f"  Exception when checking Attachment ID: {attachment.pk} (Instance ID: {instance_pk}, Path: {attachment_path}): {e}"
                    )
                    error_data.append(
                        (str(attachment.pk), str(instance_pk), str(attachment_path))
                    )

        if missing_data:
            error_msg = f"Found missing files: {len(missing_data)} attachment paths do not exist on storage."
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))

            self.stdout.write(
                self.style.WARNING("   Attachment IDs with missing files:")
            )

            for attachment_pk, instance_pk, attachment_path in missing_data:
                self.stdout.write(
                    f"      - Attachment ID: {attachment_pk} (Instance ID: {instance_pk}, Path: {attachment_path})"
                )

            errors_found.append(error_msg)

        if error_data:
            error_msg = f"Error raised for {len(error_data)} files. Could not verify if attachment paths exist on storage."
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))

            self.stdout.write(
                self.style.WARNING(
                    "   Attachment IDs with files where verification raised an error:"
                )
            )

            for attachment_pk, instance_pk, attachment_path in error_data:
                self.stdout.write(
                    f"      - Attachment ID: {attachment_pk} (Instance ID: {instance_pk}, Path: {attachment_path})"
                )

            errors_found.append(error_msg)

        if errors_found:
            return "; ".join(errors_found)
        else:
            self.stdout.write(
                self.style.SUCCESS("   All source attachment files exist on storage.")
            )
            return None

    def check_source_attachments_files(self):
        self.stdout.write(
            "\n => Checking Source Attachments (Pre-Migration Storage Check)..."
        )

        nfd_work_item = WorkItem.objects.filter(case_id=OuterRef("pk"), task_id="nfd")

        eligible_cases_qs = Case.objects.filter(
            Exists(nfd_work_item), instance__isnull=False
        ).exclude(workflow_id="migrated")

        eligible_documents = Document.objects.filter(
            form_id=SOURCE_FORM_ID,
            family__work_item__task_id="nfd",
            family__work_item__case__in=eligible_cases_qs,
            answers__question_id="nfd-tabelle-behoerde",
            answers__value__isnull=False,
        ).values_list("pk", flat=True)

        document_ids = [str(pk) for pk in eligible_documents]

        source_attachments_qs = Attachment.objects.filter(
            context__claimId__in=document_ids
        )

        count = source_attachments_qs.count()

        self.stdout.write(f"   => Checking {count} source attachments...")

        return self._verify_storage_files(source_attachments_qs)

    def check_migrated_attachments_reference(self):
        self.stdout.write("\n => Checking Migrated Attachments (Links)...")
        migrated_attachments_qs = Attachment.objects.filter(
            context__has_key=MIGRATION_META_CLAIM_ID_KEY,
        ).select_related("instance")
        total_count = migrated_attachments_qs.count()

        if total_count == 0:
            self.stdout.write("   - No migrated attachments found to check.")
            return None

        valid_migrated_doc_ids = set(
            str(pk)
            for pk in Document.objects.filter(
                meta__has_key=MIGRATION_META_CLAIM_ID_KEY,
                form_id=FILL_DEMAND_FORM_ID,
            ).values_list("pk", flat=True)
        )

        self.stdout.write(
            f"   => Checking {total_count} attachments against {len(valid_migrated_doc_ids)} migrated claim documents..."
        )

        broken_links_data = []

        for attachment in migrated_attachments_qs:
            claim_id = attachment.context.get("claimId")

            if not claim_id or str(claim_id) not in valid_migrated_doc_ids:
                instance_pk = attachment.instance.pk
                broken_links_data.append((str(attachment.pk), str(instance_pk)))

        if broken_links_data:
            error_msg = f"Broken Links: {len(broken_links_data)} attachments point to non-existent/non-migrated claim documents."
            self.stdout.write(self.style.ERROR(f"   {error_msg}"))

            self.stdout.write(
                self.style.WARNING(
                    "    Attachments with broken links (missing/incorrect claimId):"
                )
            )
            for attachment_pk, instance_pk in broken_links_data:
                self.stdout.write(
                    f"      - Attachment ID: {attachment_pk} (Instance ID: {instance_pk})"
                )

            return error_msg
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "   All attachments link to valid migrated claim documents."
                )
            )
            return None

    def check_migrated_attachments_files(self):
        self.stdout.write("\n => Checking Migrated Attachments (Storage)...")

        migrated_attachments_qs = Attachment.objects.filter(
            context__has_key=MIGRATION_META_CLAIM_ID_KEY,
        ).select_related("instance")

        count = migrated_attachments_qs.count()
        self.stdout.write(f"   => Checking {count} migrated attachments...")

        return self._verify_storage_files(migrated_attachments_qs)
