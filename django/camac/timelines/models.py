import uuid_extensions
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import models
from django.db.models import Count
from django.utils.timezone import datetime, now
from django.utils.translation import gettext_lazy as _

from camac.instance.models import Instance


class FormTimelineQuerySet(models.QuerySet):
    def annotate_cases_count(self):
        """Add a cases count which is used to determine the label of the timeline."""
        return self.annotate(cases_count=Count("cases", distinct=True))

    def for_instance(self, instance: Instance):
        return self.filter(instance=instance)

    def only_open(self):
        return self.filter(end_date__isnull=True)


class FormTimelineManager(models.Manager):
    def add_instance_timeline(
        self,
        instance: Instance,
        timeline_type: str,
        start_date: datetime,
        end_date: datetime | None = None,
        close_previous: bool = True,
    ) -> "FormTimeline":
        """Create a new form timeline entry for the given instance.

        And close any previously open timelines for the same instance.
        """
        if close_previous:
            self.close_open_timelines(instance)

        form_timeline = self.create(
            instance=instance,
            timeline_type=timeline_type,
            start_date=start_date,
            end_date=end_date,
        )

        return form_timeline

    def open_additional_demand(self, work_item: WorkItem) -> "FormTimeline":
        """Open an additional demand timeline for the given work item.

        If it already exists, add the workitem to the timeline.
        """
        instance = work_item.case.family.instance
        task_id = settings.ADDITIONAL_DEMAND["TASK"]
        assert work_item.task_id == task_id, (
            f"Work item must be of task {task_id}, but got {work_item.task_id}"
        )

        timeline = (
            self.get_queryset()
            .for_instance(instance)
            .only_open()
            .filter(timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND)
            .first()
        )

        if not timeline:
            timeline = self.add_instance_timeline(
                instance=instance,
                timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND,
                start_date=now(),
            )

        case_ids = list(timeline.cases.values_list("pk", flat=True))
        additional_demand_case = work_item.child_case
        if additional_demand_case.pk not in case_ids:
            timeline.cases.add(additional_demand_case)

        instance.case.family.meta["additional-demand-changes"] = [
            str(pk) for pk in list(timeline.cases.values_list("pk", flat=True))
        ]
        instance.case.family.save(update_fields=["meta"])

        return timeline

    def close_additional_demand(self, work_item: WorkItem) -> None:
        """Close an additional demand timeline for the given work item."""
        instance = work_item.case.family.instance

        task_id = settings.ADDITIONAL_DEMAND["TASK"]
        assert work_item.task_id == task_id, (
            f"Work item must be of task {task_id}, but got {work_item.task_id}"
        )

        timeline = (
            self.get_queryset()
            .for_instance(instance)
            .only_open()
            .filter(
                timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND,
            )
            .first()
        )
        if timeline:
            case_ids = list(timeline.cases.values_list("pk", flat=True))
            additional_demand_case = work_item.child_case
            if additional_demand_case.pk in case_ids:
                timeline.cases.remove(additional_demand_case)

            if timeline.cases.count() == 0:
                self.close_open_timelines(
                    instance=instance,
                    timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND.value,
                )

            instance.case.family.meta["additional-demand-changes"] = [
                str(pk) for pk in list(timeline.cases.values_list("pk", flat=True))
            ]
            instance.case.family.save(update_fields=["meta"])

    def close_open_timelines(
        self, instance: Instance, timeline_type: str | None = None
    ) -> None:
        """Close timelines for the given instance and conditions."""

        timelines = self.get_queryset().for_instance(instance).only_open()

        if timeline_type:
            timelines = timelines.filter(timeline_type=timeline_type)

        timelines.update(end_date=now())


class FormTimeline(models.Model):
    class Type(models.TextChoices):
        PROJECT_CHANGE = ("project-change", _("Project Change"))
        SUBMIT_AFTER_REJECTION = (
            "submit-after-rejection",
            _("Submit After Rejection"),
        )
        ADDITIONAL_DEMAND = ("additional-demand", _("Additional Demand"))
        CORRECTION = ("correction", _("Correction"))

    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        related_name="form_timelines",
    )
    timeline_type = models.CharField(
        max_length=50,
        choices=Type.choices,
    )
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # related additional demand cases
    cases = models.ManyToManyField(
        "caluma_workflow.Case",
        related_name="form_timelines",
        blank=True,
    )

    @property
    def label(self):
        if not hasattr(self, "cases_count"):
            raise AttributeError(
                "The label property requires the cases_count annotation. "
                "Please annotate the queryset with .annotate_cases_count()"
            )

        cases_count = getattr(self, "cases_count", None)

        if (
            self.timeline_type == FormTimeline.Type.ADDITIONAL_DEMAND.value
            and cases_count > 1
        ):
            return _("Additional Demands")

        return FormTimeline.Type(self.timeline_type).label

    objects: FormTimelineManager = FormTimelineManager.from_queryset(
        FormTimelineQuerySet
    )()
