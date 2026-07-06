from caluma.caluma_form.models import Form
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Count, Exists, OuterRef, Q

from camac.caluma.extensions.events.general import get_caluma_setting
from camac.caluma.models import Inquiry
from camac.instance.models import Instance
from camac.user.models import Service
from camac.utils import get_unversioned_slug


class Command(BaseCommand):
    help = "Verify generated rpg2 work-items (from management command create_rpg2_workitems)."

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

    def _get_skip_trigger_tasks(self) -> [str]:
        """Retrieve a list of tasks that would lead to skipping the rpg2 work item on completion."""

        pre_complete_config = get_caluma_setting("PRE_COMPLETE", {})
        rpg2_task_slug = settings.RPG2.task

        skip_trigger_tasks = []
        for task_name, configured_actions in pre_complete_config.items():
            tasks_that_get_skipped = configured_actions.get("skip", [])
            if rpg2_task_slug in tasks_that_get_skipped:
                skip_trigger_tasks.append(task_name)

        return skip_trigger_tasks

    def log_result(self, check_message, assertion, context=None):
        """Log result of check with additional messages for context."""

        if context is None:
            context = []

        result_message = "OK" if assertion else "NOT OK"
        self.stdout.write("----")
        self.stdout.write(f"{check_message}: {result_message}\n")
        for message in context:
            self.stdout.write(f"- {message}\n")

        return assertion

    def log_forms_with_inquiries(self, form_slugs, service_pks):
        """Log all forms for which the configured rpg2 service(s) have inquiries.

        The information is for verification purposes, to ensure that all necessary
        forms have been configured correctly.
        """

        forms_count = (
            Instance.objects.filter(
                Exists(
                    Inquiry.objects.addressed_to(service_pks)
                    .only_active()
                    .for_instance(OuterRef("pk"))
                )
            )
            .values("case__document__form__slug")
            .annotate(num=Count("case__document__form__slug"))
            .order_by("-num")
            .values_list("case__document__form__slug", "num")
        )

        form_results = {}
        for form, count in forms_count:
            slug = get_unversioned_slug(form)
            if slug in form_results:
                form_results[slug] = form_results[slug] + count
            else:
                form_results[slug] = count

        self.stdout.write(
            "Found rpg2 service inquiries for the following unversioned forms:"
        )
        for form, count in form_results.items():
            is_migrated = " (rpg2 migrated)" if form in form_slugs else ""
            self.stdout.write(f"- {form}: {count}{is_migrated}")

    def check_rpg2_workitems_addressed_groups(
        self, inquiries, rpg2_workitems, rpg2_workitems_addressed_agr
    ):
        """Check that all rpg2 work-items are addressed to configured rpg2 service."""

        return self.log_result(
            check_message="All rpg2 work-items are addressed to configured rpg2 service",
            assertion=len(rpg2_workitems) == len(rpg2_workitems_addressed_agr),
            context=[
                f"All rpg2 work-items: {len(rpg2_workitems_addressed_agr)}",
                f"rpg2 work-items addressed to rpg2 service: {len(rpg2_workitems)}",
            ],
        )

    def check_rpg2_workitems_instances(self, inquiry_instances, rpg2_instances):
        """Check that rgp2 work-items have been created for all instances with an inquiry addressed to rpg2 service."""

        inquiry_instances_set = set(inquiry_instances)
        rpg2_instances_set = set(rpg2_instances)

        return self.log_result(
            check_message="All instances (with relevant forms) with an inquiry to the rpg2-service have an rpg2 work-item",
            assertion=inquiry_instances_set == rpg2_instances_set,
            context=[
                f"Instances set with inquiries to rpg2 service: {len(inquiry_instances_set)}",
                f"Instances set with rpg2 work-item: {len(rpg2_instances_set)}",
                f"Instances with missing rpg2 work-item: {inquiry_instances_set - rpg2_instances_set}",
                f"Instances with unexpected rpg2 work-item: {rpg2_instances_set - inquiry_instances_set}",
            ],
        )

    def check_rpg2_workitems_count(self, inquiry_instances, rpg2_instances):
        """Check that exactly one rpg2 work-item was created per instance."""

        rpg2_instances_set = set(rpg2_instances)

        # relevant instances have exactly one rpg2 work-item
        single_match_rpg2 = len(rpg2_instances) == len(rpg2_instances_set)
        check_passed = self.log_result(
            check_message="Exactly one rpg2 work-item per instance",
            assertion=single_match_rpg2,
            context=[
                f"Instances with rpg2 work-item: {len(rpg2_instances)}",
                f"Instances with rpg2 work-item (no duplicates): {len(rpg2_instances_set)}",
            ],
        )

        if not single_match_rpg2:
            self.stdout.write(
                "> Determining missing / duplicate rpg2 work-items, this will take a while..."
            )

            instances_annotated_rpg2_count = Instance.objects.filter(
                pk__in=inquiry_instances
            ).annotate(
                num_rpg2=Count(
                    WorkItem.objects.filter(
                        task_id="rpg2", case__family=OuterRef("case")
                    ).values("pk")
                )
            )

            instances_missing_rpg2 = list(
                instances_annotated_rpg2_count.filter(num_rpg2=0).values_list(
                    "pk", flat=True
                )
            )
            self.stdout.write(
                f"- Instances missing rpg2 work-item: {instances_missing_rpg2}\n"
            )

            instances_duplicate_rpg2 = list(
                instances_annotated_rpg2_count.filter(num_rpg2__gt=1).values_list(
                    "pk", flat=True
                )
            )
            self.stdout.write(
                f"- Instances with duplicate rpg2 work-items: {instances_duplicate_rpg2}\n"
            )

        return check_passed

    def check_rpg2_workitems_status(self, rpg2_workitems_addressed_agr):
        """Check that all rpg2 work-items have an expected status."""

        unexpected_status_list = list(
            rpg2_workitems_addressed_agr.exclude(
                status__in=[
                    WorkItem.STATUS_READY,
                    WorkItem.STATUS_SKIPPED,
                    WorkItem.STATUS_SUSPENDED,
                ]
            ).values_list("pk", "status", "case__family__instance__pk")
        )

        return self.log_result(
            check_message="No rpg2 work-item has an unexpected status",
            assertion=not unexpected_status_list,
            context=[
                f"rpg2 work-items with unexpected status: {unexpected_status_list}",
            ],
        )

    def check_rpg2_workitems_status_skipped(self, rpg2_workitems_addressed_agr):
        """Check that all skipped rpg2 work-items are in the correct status."""

        skipped_unexpected_status_list = list(
            rpg2_workitems_addressed_agr.filter(
                ~Exists(
                    WorkItem.objects.filter(
                        task_id__in=self._get_skip_trigger_tasks(),
                        status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
                        case__family=OuterRef("case__family"),
                    )
                )
                & ~Q(
                    case__family__status__in=[
                        Case.STATUS_COMPLETED,
                        Case.STATUS_CANCELED,
                    ]
                ),
                status=WorkItem.STATUS_SKIPPED,
            ).values_list("pk", "status", "case__family__instance__pk")
        )

        return self.log_result(
            check_message="Status of all skipped rpg2 work-items is correct",
            assertion=not skipped_unexpected_status_list,
            context=[
                f"rpg2 work-items with incorrect status 'skipped': {skipped_unexpected_status_list}",
            ],
        )

    def check_rpg2_workitems_status_suspended(self, rpg2_workitems_addressed_agr):
        """Check that all suspended rpg2 work-items are in the correct status."""

        suspended_unexpected_status_list = list(
            rpg2_workitems_addressed_agr.filter(
                ~Q(case__family__status=Case.STATUS_SUSPENDED),
                status=WorkItem.STATUS_SUSPENDED,
            ).values_list("pk", "status", "case__family__instance__pk")
        )

        return self.log_result(
            check_message="Status of all suspended rpg2 work-items is correct",
            assertion=not suspended_unexpected_status_list,
            context=[
                f"rpg2 work-items with incorrect status 'suspended': {suspended_unexpected_status_list}",
            ],
        )

    def check_rpg2_workitems_status_ready(self, rpg2_workitems_addressed_agr):
        """Check that all ready rpg2 work-items are in the correct status."""

        ready_unexpected_status_list = list(
            rpg2_workitems_addressed_agr.filter(
                Exists(
                    WorkItem.objects.filter(
                        task_id__in=self._get_skip_trigger_tasks(),
                        status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
                        case__family=OuterRef("case__family"),
                    )
                )
                | ~Q(case__family__status=Case.STATUS_RUNNING),
                Q(status=WorkItem.STATUS_READY),
            ).values_list("pk", "status", "case__family__instance__pk")
        )

        return self.log_result(
            check_message="Status of all ready rpg2 work-items is correct",
            assertion=not ready_unexpected_status_list,
            context=[
                f"rpg2 work-items with incorrect status 'ready': {ready_unexpected_status_list}",
            ],
        )

    def check_rpg2_documents(self, rpg2_workitems_addressed_agr):
        """Check that all rpg2 work-items have an rpg2 document."""

        missing_rpg2_documents = list(
            rpg2_workitems_addressed_agr.filter(
                Q(document__isnull=True) | ~Q(document__form="rpg2")
            ).values_list("pk", "case__family__instance__pk")
        )
        return self.log_result(
            check_message="All rpg2 work-items have a document",
            assertion=not missing_rpg2_documents,
            context=[
                f"rpg2 work-items without document: {missing_rpg2_documents}",
            ],
        )

    @transaction.atomic
    def handle(self, *args, **options):
        form_slugs = options["forms"]
        service_slugs = options["rpg2_services"]

        # checking verification parameters
        self.stdout.write(
            f"\n{'=' * 50}\n"
            f"Verifying migration of instances with the following parameters:\n"
            f" * form-slugs: {form_slugs}\n"
            f" * rpg2-services: {service_slugs}\n"
            f" * skip trigger tasks: {self._get_skip_trigger_tasks()}\n"
        )

        services = Service.objects.filter(slug__in=service_slugs)
        service_pks = [str(pk) for pk in services.values_list("pk", flat=True)]
        self.stdout.write(f"Found rpg2 service(s): {[str(s) for s in services]}\n")

        if not form_slugs or not service_slugs or not service_pks:
            self.stdout.write("Configuration incomplete - please check.")
            return

        self.log_forms_with_inquiries(form_slugs, service_pks)

        # determine relevant forms
        form_filters = Q()
        for slug in form_slugs:
            form_filters |= Q(slug__regex=rf"^{slug}(-v\d+)?$")

        versioned_forms = Form.objects.filter(form_filters)

        # determine relevant inquiries addressed to rpg2 service
        inquiries = (
            Inquiry.objects.addressed_to(service_pks)
            .only_active()
            .filter(case__family__document__form__slug__in=versioned_forms)
        )

        # determine rpg2 work-items addressed to rpg2 service
        rpg2_workitems = WorkItem.objects.filter(task_id=settings.RPG2.task)
        rpg2_workitems_addressed_agr = rpg2_workitems.filter(
            addressed_groups__contains=service_pks
        )

        # determine instances with inquiry to rpg2 service
        inquiry_instances = list(
            inquiries.values_list("case__family__instance__pk", flat=True)
        )

        # determine instances with rpg2 work-item
        rpg2_instances = list(
            rpg2_workitems_addressed_agr.values_list(
                "case__family__instance__pk", flat=True
            )
        )

        verification_passed = all(
            [
                self.check_rpg2_workitems_addressed_groups(
                    inquiries,
                    rpg2_workitems,
                    rpg2_workitems_addressed_agr,
                ),
                self.check_rpg2_workitems_instances(
                    inquiry_instances,
                    rpg2_instances,
                ),
                self.check_rpg2_workitems_count(
                    inquiry_instances,
                    rpg2_instances,
                ),
                self.check_rpg2_workitems_status(
                    rpg2_workitems_addressed_agr,
                ),
                self.check_rpg2_workitems_status_skipped(
                    rpg2_workitems_addressed_agr,
                ),
                self.check_rpg2_workitems_status_suspended(
                    rpg2_workitems_addressed_agr,
                ),
                self.check_rpg2_workitems_status_ready(
                    rpg2_workitems_addressed_agr,
                ),
                self.check_rpg2_documents(
                    rpg2_workitems_addressed_agr,
                ),
            ]
        )

        self.stdout.write("----")
        verification_message = (
            "VERIFICATION PASSED" if verification_passed else "VERIFICATION FAILED"
        )
        self.stdout.write(f"{verification_message}")
