from datetime import datetime, timedelta

import pytz
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.db.models import Case as DjangoCase, CharField, Exists, F, OuterRef, When
from django.db.models.functions import Cast
from tqdm import tqdm

from camac.core.models import InstanceService


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("--reset", dest="reset", action="store_true", default=False)

    def reset(self):
        WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"]
        ).delete()

    @transaction.atomic
    def handle(self, *args, **options):
        if options.get("reset"):
            self.reset()

        tqdm.write("Cancelling check-inquiries with no deadline")

        # Delete ready check-inquiries without deadline
        WorkItem.objects.filter(
            task_id=settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
            status=WorkItem.STATUS_READY,
            deadline__isnull=True,
        ).delete()

        tqdm.write("Adding check-distribution work-items")

        # Create a check-distribution work-item for all distribution cases that have
        # already been initialized (or skipped and re-opened) and don't have any
        # pending inquiries addressed to the lead authority left.
        distribution_cases_to_migrate = Case.objects.filter(
            ~Exists(
                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                    status=WorkItem.STATUS_READY,
                    case_id=OuterRef("pk"),
                )
            ),
            ~Exists(
                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                    status=WorkItem.STATUS_READY,
                    case_id=OuterRef("pk"),
                    controlling_groups=OuterRef("parent_work_item__addressed_groups"),
                )
            ),
            workflow_id="distribution",
            status=Case.STATUS_RUNNING,
        )

        check_distribution_task = Task.objects.get(
            pk=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
        )

        check_distribution_work_items = []
        for distribution_case in tqdm(
            distribution_cases_to_migrate,
            mininterval=1,
            maxinterval=2,
        ):

            try:
                last_completed_inquiry = (
                    distribution_case.work_items.filter(
                        task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                        # Include skipped for distribution cases where the distribution
                        #  was terminated prematurely. Relevant when inquiries were
                        # skipped after completing some of the inquiries. The date of the
                        # case re-opening would be relevant (heuristically the latest date
                        # of the skipped inquiries), not the date of the last completed
                        # inquiry.
                        status__in=[WorkItem.STATUS_SKIPPED, WorkItem.STATUS_COMPLETED],
                        controlling_groups=distribution_case.parent_work_item.addressed_groups,
                        closed_at__isnull=False,
                    )
                    .order_by("-closed_at")
                    .first()
                )

                last_completed_inquiry_closed_at = (
                    last_completed_inquiry.closed_at
                    if last_completed_inquiry
                    # Relevant for re-opened distribution cases
                    # with no inquiries (skipped)
                    else distribution_case.modified_at
                )

                check_distribution_work_items.append(
                    WorkItem(
                        task=check_distribution_task,
                        name=check_distribution_task.name,
                        addressed_groups=distribution_case.parent_work_item.addressed_groups,
                        case=distribution_case,
                        status=WorkItem.STATUS_READY,
                        deadline=pytz.utc.localize(
                            datetime.combine(
                                (
                                    last_completed_inquiry_closed_at
                                    + timedelta(
                                        seconds=check_distribution_task.lead_time
                                    )
                                ).date(),
                                datetime.min.time(),
                            )
                        ),
                        previous_work_item=last_completed_inquiry,
                        meta={
                            "not-viewed": True,
                            "notify-completed": False,
                            "notify-deadline": True,
                        },
                    )
                )

            except Exception as e:  # noqa: B902
                raise CommandError(
                    f"Exception ocurred during migration of instance {distribution_case.instance.pk}: {str(e)}"
                )

        tqdm.write("Bulk creating work-items")
        WorkItem.objects.bulk_create(check_distribution_work_items)

        tqdm.write("Updating created-at of work-items")
        WorkItem.objects.filter(
            pk__in=[work_item.pk for work_item in check_distribution_work_items]
        ).annotate(
            last_completed_inquiry_closed_at=WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                case=OuterRef("case"),
                status__in=[WorkItem.STATUS_SKIPPED, WorkItem.STATUS_COMPLETED],
                controlling_groups=OuterRef("addressed_groups"),
                closed_at__isnull=False,
            )
            .order_by("-closed_at")
            .values("closed_at")[:1],
            distribution_case_modified_at=Case.objects.filter(
                pk=OuterRef("case"),
            ).values("modified_at")[:1],
        ).update(
            created_at=DjangoCase(
                When(
                    last_completed_inquiry_closed_at__isnull=False,
                    then=F("last_completed_inquiry_closed_at"),
                ),
                default=F("distribution_case_modified_at"),
            )
        )

        tqdm.write("Migration completed")

        ready_check_distribution_in_wrong_state = (
            WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
                status=WorkItem.STATUS_READY,
            )
            .exclude(
                case__family__instance__instance_state__name__in=[
                    "circ",
                    "nfd",
                    "circulation",
                ]
            )
            .count()
        )

        self.log_result(
            ready_check_distribution_in_wrong_state == 0,
            "All ready check-distribution work-items are in a circulation instance state",
        )

        if settings.APPLICATION_NAME == "kt_bern":
            check_distribution_wrong_addressed_group = WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"]
            ).exclude(
                addressed_groups__0=Cast(
                    InstanceService.objects.filter(
                        active=1,
                        instance_id=OuterRef("case__family__instance_id"),
                        **(
                            settings.APPLICATION.get("ACTIVE_SERVICES", {})
                            .get("MUNICIPALITY", {})
                            .get("FILTERS", {})
                        ),
                    ).values_list("service")[:1],
                    output_field=CharField(),
                )
            )
        else:
            check_distribution_wrong_addressed_group = (
                WorkItem.objects.filter(
                    task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
                )
                .exclude(
                    addressed_groups__0=Cast(
                        "case__family__instance__group__service_id",
                        output_field=CharField(),
                    ),
                )
                .count()
            )

        self.log_result(
            check_distribution_wrong_addressed_group == 0,
            "All check-distribution work-items are addressed to lead authority",
        )

    def log_result(self, condition, label):
        result = (
            self.style.SUCCESS("PASSED")
            if bool(condition)
            else self.style.ERROR("FAILED")
        )

        self.stdout.write(f"{label}: {result}")
