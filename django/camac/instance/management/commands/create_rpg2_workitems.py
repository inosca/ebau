"""
Creates the rpg2 work-item for existing instances.

This was written for the migration of existing instances to the new RPG2 requirements.
The logic is designated for the cantons AG,BE & SZ and will filter for the following:
  * instance document is a form included in the 'forms' list
  * instance had an active circulation
  * instance circulation included service from 'rpg2_services'
"""

import time
from datetime import timedelta

from caluma.caluma_form.models import Document, Form
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Exists, OuterRef, Q
from django.utils import timezone

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.caluma.models import Inquiry
from camac.instance.models import Instance
from camac.user.models import Service


class Command(BaseCommand):
    help = "Create a rpg2 work-item for existing instances."

    def add_arguments(self, parser):
        # positional argument, default to settings.RPG2.allowed_forms
        parser.add_argument(
            "--forms",
            type=str,
            nargs="+",
            dest="forms",
            default=settings.RPG2.allowed_forms,
        )
        # positional argument, default settings.RPG2.service_slugs
        parser.add_argument(
            "--rpg2_services",
            type=str,
            nargs="+",
            dest="rpg2_services",
            default=settings.RPG2.service_slugs,
        )
        # optional argument
        parser.add_argument(
            "--commit", dest="commit", action="store_true", default=False
        )

    def _get_skip_trigger_tasks(self) -> [str]:
        """Retrieve a list of tasks that would lead to skipping the RPG2 work item on completion."""

        pre_complete_config = get_caluma_setting("PRE_COMPLETE", {})
        rpg2_task_slug = settings.RPG2.task

        skip_trigger_tasks = []
        for task_name, configured_actions in pre_complete_config.items():
            tasks_that_get_skipped = configured_actions.get("skip", [])
            if rpg2_task_slug in tasks_that_get_skipped:
                skip_trigger_tasks.append(task_name)

        return skip_trigger_tasks

    def _get_rpg2_work_item_status(
        self, instance: Instance, skip_trigger_tasks: [str]
    ) -> str:
        """
        Determine the RPG2 work item status.

        This will check the case status and check if any work item should have led to a skipped RPG2 work item.
        """
        if instance.case.work_items.filter(
            task_id__in=skip_trigger_tasks,
            status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
        ).exists():
            return WorkItem.STATUS_SKIPPED

        if instance.case.status == Case.STATUS_SUSPENDED:
            return WorkItem.STATUS_SUSPENDED

        if instance.case.status != Case.STATUS_RUNNING:
            return WorkItem.STATUS_SKIPPED

        return WorkItem.STATUS_READY

    @transaction.atomic
    def handle(self, *args, **options):
        if not options["commit"]:
            self.stdout.write(
                self.style.WARNING("The --commit option is off. This is a DRY run!!!")
            )

        form_slugs = options["forms"]
        service_slugs = options["rpg2_services"]

        self.stdout.write(
            f"\n{'=' * 50}\n"
            f"Starting migration of instances with the following parameters:\n"
            f" * form-slugs: {form_slugs}\n"
            f" * rpg2-services: {service_slugs}\n"
        )

        start_time = time.perf_counter()

        if not form_slugs or not service_slugs:
            self.stdout.write(
                self.style.ERROR(
                    "form-slugs or RPG2-services are not defined.\n"
                    "Please check the RPG2-module-settings or pass in form-slugs and rpg2-services via '--forms' or '--rpg2_services'.\n"
                    "EXITING!"
                )
            )
            return

        # Prepare task & groups for assigning the rpg2 work-item.
        # Assume task exists (created per canton) when module is enabled.
        task = Task.objects.get(pk=settings.RPG2.task)

        # The rpg2 work_item is addressed to all cantonal services configured.
        services = Service.objects.filter(slug__in=service_slugs)
        service_pks = [str(pk) for pk in services.values_list("pk", flat=True)]

        if not service_pks:
            self.stdout.write(
                self.style.ERROR(
                    "No services found for configured rpg 2 service slugs.\n"
                    "Please check the slugs of the relevant service(s).\n"
                    "EXITING!"
                )
            )
            return

        self.stdout.write(f"Found rpg2 service(s): {[str(s) for s in services]}\n")

        skip_trigger_tasks = self._get_skip_trigger_tasks()
        self.stdout.write(
            f"\nCompiled list of tasks that would put the RPG2-work-item into 'skipped' state:\n"
            f" * {skip_trigger_tasks}\n"
            f"{'=' * 50}\n"
        )

        sid = transaction.savepoint()

        stats = {
            "total_processed": 0,
            "total_updated": 0,
            "total_skipped": 0,
            "total_errors": 0,
        }

        # NOTE: We could also filter for all form_slugs at once, but chunking it could
        # yield the error location more clearly if anything goes wrong and performance
        # wise it won't make a huge difference.
        for slug in form_slugs:
            self.stdout.write(f"\n  Processing form slug: {slug}")
            versioned_forms = Form.objects.filter(slug__regex=rf"^{slug}(-v\d+)?$")
            self.stdout.write(
                f"\n  Found forms: {list(versioned_forms.values_list('slug', flat=True))}"
            )

            query_start_time = time.perf_counter()
            instances = Instance.objects.filter(
                Q(case__document__form__slug__in=versioned_forms)
                & Exists(
                    Inquiry.objects.for_instance(OuterRef("pk"))
                    .addressed_to(service_pks)
                    .only_active()
                )
            )

            total = instances.count()
            query_end_time = time.perf_counter()
            query_duration = timedelta(seconds=query_end_time - query_start_time)
            self.stdout.write(
                self.style.NOTICE(
                    f"  Queriering relevant instances took: {query_duration}"
                )
            )

            if total == 0:
                self.stdout.write(
                    self.style.WARNING(f"  No instances found for '{slug}', skipping.")
                )
                continue
            else:
                self.stdout.write(
                    self.style.NOTICE(
                        f"  Starting to process... {total} instances ahead of us."
                    )
                )

            slug_stats = {"processed": 0, "updated": 0, "skipped": 0, "errors": 0}

            for instance in instances.iterator(chunk_size=500):
                slug_stats["processed"] += 1
                try:
                    # 1. check if RPG2 work-item already exists
                    #   if so -- skip!
                    if instance.case.work_items.filter(
                        task_id=settings.RPG2.task
                    ).exists():
                        slug_stats["skipped"] += 1
                        continue  # "rpg2" work-item already exists

                    status = self._get_rpg2_work_item_status(
                        instance, skip_trigger_tasks
                    )

                    WorkItem.objects.create(
                        task=task,
                        name=task.name,
                        addressed_groups=service_pks,
                        case=instance.case,
                        status=status,
                        document=Document.objects.create_document_for_task(task, None),
                        meta={"migrated-at": timezone.now().isoformat()},
                    )

                    slug_stats["updated"] += 1
                    self.stdout.write(
                        self.style.NOTICE(
                            f"  ...created work-item (state: {status}, instance: {instance.pk})"
                        )
                    )

                except Exception as e:
                    slug_stats["errors"] += 1
                    self.stdout.write(
                        self.style.ERROR(f"  Error on Instance {instance.pk}: {e}")
                    )

            # per-slug summary
            self.stdout.write(
                self.style.SUCCESS(
                    f"  Instances based on '{slug}' done.\n"
                    f"  {slug_stats['processed']} processed, "
                    f"{slug_stats['updated']} updated, "
                    f"{slug_stats['skipped']} skipped, "
                    f"{slug_stats['errors']} errors"
                )
            )

            for key in ("processed", "updated", "skipped", "errors"):
                stats[f"total_{key}"] += slug_stats[key]

        if options["commit"]:
            transaction.savepoint_commit(sid)
        else:
            transaction.savepoint_rollback(sid)

        end_time = time.perf_counter()
        duration = timedelta(seconds=end_time - start_time)

        self.stdout.write(
            self.style.SUCCESS(
                f"\n{'=' * 50}\n"
                f"Migration completed in {duration}:\n"
                f"  Total processed: {stats['total_processed']}\n"
                f"  Total updated:   {stats['total_updated']}\n"
                f"  Total skipped:   {stats['total_skipped']}\n"
                f"  Total errors:    {stats['total_errors']}\n"
                f"{'=' * 50}"
            )
        )
