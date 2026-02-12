from datetime import date, datetime, timedelta
from typing import Optional, TypeVar

import uuid_extensions
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import models, transaction
from django.db.models import Exists, OuterRef, Q
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField

from camac.caluma.models import Inquiry
from camac.core.utils import canton_aware
from camac.deadlines.mixins import DeadlinePermissionMixin
from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.user.models import Service
from camac.utils import is_public_holiday, is_weekend_day

TSuspension = TypeVar("TSuspension", bound="SuspensionQuerySet")
TInstanceDeadline = TypeVar("TInstanceDeadline", bound="InstanceDeadlinesQuerySet")
TDeadlineType = TypeVar("TDeadlineType", bound="DeadlineTypeQuerySet")


def _fields_have_changed(old, new, fields) -> bool:
    """Check if any of the specified fields have changed between two model instances."""
    return not old or any(
        getattr(old, field, None) != getattr(new, field, None) for field in fields
    )


class DeadlineTypeQuerySet(DeadlinePermissionMixin, models.QuerySet["DeadlineType"]):
    def for_service(self: TDeadlineType, service: Service) -> TDeadlineType:
        return (
            self.filter(
                (Q(services__isnull=True) | Q(services=service))
                & (
                    Q(service_groups__isnull=True)
                    | Q(service_groups=service.service_group)
                )
            )
            if self.has_deadline_access(service)
            else self.none()
        )

    def for_instance(self: TDeadlineType, instance: Instance) -> TDeadlineType:
        return self.filter(
            Q(form_types__isnull=True)
            | Q(form_types=[])
            | Q(form_types__contains=[str(instance.case.family.document.form.pk)])
        )

    def get_default(
        self: TDeadlineType, service: Service, instance: Instance
    ) -> Optional["DeadlineType"]:
        """Return the first default deadline type for the service.

        If no default deadline type exists, return the first deadline type
        available for the service.
        """
        base_query = (
            DeadlineType.objects.for_service(service)
            .for_instance(instance)
            .order_by("lead_time")
        )
        first_default = base_query.filter(is_default=True).first()

        return first_default if first_default else base_query.first()


class SuspensionQuerySet(DeadlinePermissionMixin, models.QuerySet["Suspension"]):
    def for_service(self: TSuspension, service: Service) -> TSuspension:
        return (
            self.filter(deadline__service=service)
            if self.has_deadline_access(service)
            else self.none()
        )

    def for_deadline(self: TSuspension, deadline: "InstanceDeadline") -> TSuspension:
        return self.filter(deadline=deadline)

    def for_workitem(self: TSuspension, work_item: WorkItem) -> TSuspension:
        return self.filter(
            work_item=work_item,
        )

    def for_additional_demand(self: TSuspension, work_item: WorkItem) -> TSuspension:
        return self.for_workitem(
            work_item=work_item,
        ).filter(
            reason=Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND
        )

    def for_inquiry(self: TSuspension, work_item: WorkItem) -> TSuspension:
        return self.for_workitem(
            work_item=work_item,
        ).filter(
            reason=Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM
        )

    def only_open(self: TSuspension) -> TSuspension:
        """Filter to only include suspensions that are currently open."""
        return self.filter(end_date__isnull=True)

    def only_closed(self: TSuspension) -> TSuspension:
        """Filter to only include suspensions that are currently closed."""
        return self.filter(end_date__isnull=False)


class InstanceDeadlinesQuerySet(
    DeadlinePermissionMixin, models.QuerySet["InstanceDeadline"]
):
    def for_service(
        self: TInstanceDeadline, service: Service | None
    ) -> TInstanceDeadline:
        return (
            self.filter(service=service)
            if service and self.has_deadline_access(service)
            else self.none()
        )

    def for_instance(self: TInstanceDeadline, instance: Instance) -> TInstanceDeadline:
        return self.filter(instance=instance)

    def only_running(self: TInstanceDeadline) -> TInstanceDeadline:
        """Query deadlines that are still running."""
        return self.annotate(
            has_open_suspension=Exists(
                Suspension.objects.only_open().filter(deadline=OuterRef("pk"))
            )
        ).filter(
            Q(
                process_deadline_date__isnull=True,
            )
            | Q(process_deadline_date__gt=now().date())
            | Q(has_open_suspension=True)
        )

    def create_deadline(
        self, instance: Instance, service: Service
    ) -> Optional["InstanceDeadline"]:
        if not self.has_instance_access(instance=instance, service=service):
            return None

        deadline, _ = InstanceDeadline.objects.get_or_create(
            instance=instance,
            service=service,
            defaults={
                "deadline_type": DeadlineType.objects.get_default(
                    service=service,
                    instance=instance,
                )
            },
        )

        deadline.save()

        return deadline

    def recalculate_deadlines(self, process_all=False):
        updated = []
        qs_deadlines = self.all() if process_all else self.only_running()

        for deadline in qs_deadlines.iterator(chunk_size=100):
            deadline.recalculate_progression()
            updated.append(deadline)

        return updated


class DeadlineType(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    services = models.ManyToManyField(
        "user.Service", blank=True, verbose_name=_("Services")
    )
    service_groups = models.ManyToManyField(
        "user.ServiceGroup", blank=True, verbose_name=_("Service groups")
    )
    form_types = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_("Form types"),
        help_text=_(
            "List of form IDs this deadline type applies to. If empty, applies to all forms."
        ),
    )
    name = LocalizedCharField(verbose_name=_("Name"))
    lead_time = models.PositiveIntegerField(
        verbose_name=_("Lead time in days"),
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_default = models.BooleanField(
        default=False,
        verbose_name=_("Is default"),
    )
    exclude_weekends = models.BooleanField(
        default=False,
        verbose_name=_("Exclude weekends"),
        help_text=_("If enabled, weekends are not counted towards deadlines."),
    )
    exclude_public_holidays = models.BooleanField(
        default=False,
        verbose_name=_("Exclude public holidays"),
        help_text=_("If enabled, public holidays are not counted towards deadlines."),
    )

    objects: DeadlineTypeQuerySet = DeadlineTypeQuerySet.as_manager()

    def __str__(self):
        return self.name.get()

    class Meta:
        verbose_name = _("Deadline type")
        verbose_name_plural = _("Deadline types")


class Suspension(models.Model):
    class SuspensionReasonChoices(models.TextChoices):
        SUSPENSION_TYPE_ADDITIONAL_DEMAND = (
            "additional_demand_suspension",
            _("Additional demand suspension"),
        )
        SUSPENSION_TYPE_INQUIRY_CLAIM = (
            "inquiry_claim_suspension",
            _("Inquiry claim suspension"),
        )
        SUSPENSION_TYPE_MANUAL = "manual_suspension", _("Manual suspension")

    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    deadline = models.ForeignKey(
        "InstanceDeadline",
        models.DO_NOTHING,
        related_name="suspensions",
    )
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    work_item = models.ForeignKey(
        "caluma_workflow.WorkItem",
        on_delete=models.CASCADE,
        related_name="+",
        blank=True,
        null=True,
    )
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    reason = models.CharField(
        choices=SuspensionReasonChoices.choices,
        default=SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL,
    )
    reason_text = models.TextField(
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    objects: SuspensionQuerySet = SuspensionQuerySet.as_manager()

    def save(self, *args, **kwargs):
        # fetch the original, to compare which fields have changed,
        # because even a new object already has a UUIDv7 pk,
        # we need to use a try-except block to handle the case where the object does not
        # exist yet.
        try:
            old = type(self).objects.get(pk=self.pk)
        except (ValueError, self.DoesNotExist):
            old = None

        super().save(*args, **kwargs)

        # only when the related values have been changed, trigger recalculation.
        if _fields_have_changed(old, self, ["start_date", "end_date"]):
            self.deadline.trigger_side_effect()

    @property
    def reason_formatted(self) -> str:
        """Format the reason for the suspension.

        If the reason is a manual suspension, return the custom reason text.
        Otherwise, return the label of the suspension reason choice.
        """
        return self.reason_text or Suspension.SuspensionReasonChoices(self.reason).label

    @property
    def author_formatted(self) -> str:
        """Format the author of the suspension.

        Return the name of the user who created the suspension. Fallback to group name if user is not set.
        If neither user nor group is set, return "Automatic".
        """
        if self.user:
            return self.user.get_full_name()

        if self.group and self.group.name:
            return self.group.name

        return _("Automatic")

    def complete(self, end_date=None) -> None:
        """Complete the suspension by setting the end date."""
        if not self.end_date:
            self.end_date = end_date or now().date()
            self.save(update_fields=["end_date"])

    def get_suspension_dates(self) -> set[date]:
        start = datetime.combine(self.start_date, datetime.min.time())
        # if the suspension has no end date, it's considered ongoing
        end = self.end_date or now()
        end = datetime.combine(end, datetime.min.time())
        tmp_date = start

        suspension_dates = []
        while tmp_date < end:
            # Ignore weekends and public holidays if configured to do so
            if self.deadline.exclude_suspension_date(tmp_date):
                tmp_date += timedelta(days=1)
                continue

            suspension_dates.append(tmp_date.date())
            tmp_date += timedelta(days=1)

        return set(suspension_dates)


class InstanceDeadline(models.Model):
    # the side effects are enabled by default which will trigger recalculation on changing
    # certain values on the deadline. Disabling this flag (e.g. during the migration) we
    # prevent unnecessary recalculations.
    enable_side_effects = True

    id = models.UUIDField(
        primary_key=True, default=uuid_extensions.uuid7, editable=False
    )
    deadline_type = models.ForeignKey(
        DeadlineType,
        models.PROTECT,
        related_name="+",
        blank=True,
        null=True,
    )
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        related_name="deadlines",
    )
    service = models.ForeignKey("user.Service", models.DO_NOTHING, related_name="+")
    start_date = models.DateField(blank=True, null=True)
    total_days_of_suspension = models.PositiveIntegerField(
        blank=True,
        null=True,
    )
    target_deadline_date = models.DateField(
        blank=True,
        null=True,
    )
    process_deadline_date = models.DateField(
        blank=True,
        null=True,
    )
    process_deadline_date_override = models.BooleanField(
        default=False,
        verbose_name=_("Process deadline date override"),
        help_text=_(
            "If set, the process deadline date is manually set and not calculated."
        ),
    )
    process_deadline_days = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Process deadline days"),
        help_text=_("The number of days processed since the start date."),
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _("Instance deadline")
        verbose_name_plural = _("Instance deadlines")

    objects: InstanceDeadlinesQuerySet = InstanceDeadlinesQuerySet.as_manager()

    def has_open_suspension(self) -> bool:
        """Query if an open suspension exists for the service/instance."""
        return self.suspensions.only_open().exists()

    def exclude_suspension_date(self, date: date) -> bool:
        deadline_type = self.deadline_type

        return (
            (
                (deadline_type.exclude_weekends and is_weekend_day(date))
                or (deadline_type.exclude_public_holidays and is_public_holiday(date))
            )
            if deadline_type
            else False
        )

    def save(self, *args, **kwargs):
        if not self.enable_side_effects:  # pragma: no cover
            return super().save(*args, **kwargs)

        # fetch the original, to compare which fields have changed,
        # because even a new object already has a UUIDv7 pk,
        # we need to use a try-except block to handle the case where the object does not
        # exist yet.
        try:
            old = type(self).objects.get(pk=self.pk)
        except (ValueError, self.DoesNotExist):
            old = None

        super().save(*args, **kwargs)

        # only when the related values have been changed, trigger recalculation.
        if _fields_have_changed(
            old,
            self,
            [
                "start_date",
                "deadline_type",
                "process_deadline_date",
                "process_deadline_date_override",
                "target_deadline_date",
            ],
        ):
            self.trigger_side_effect()

    def trigger_side_effect(self) -> None:
        """Recalculate the deadline progression on side effects."""
        return self.recalculate_progression()

    def recalculate_progression(self) -> None:
        """Recalculate the deadline progression.

        This will update the start date, progression, and instance case meta.
        """
        self.update_startdate()
        self.update_target_end_date()
        self.update_progression()
        self.update_instance_case_meta()

    def update_startdate(self) -> None:
        """Update the deadline start date if it is not already set."""
        if self.start_date:
            return

        old_start_date = self.start_date
        self.start_date = self._define_startdate()

        # only perform the save if any of the fields have actually changed.
        if old_start_date != self.start_date:
            self.save(update_fields=["start_date"])

    def update_target_end_date(self) -> None:
        """Update the target end date."""
        old_target_end_date = self.target_deadline_date
        self.target_deadline_date = (
            self._get_target_enddate() if self.start_date else None
        )

        # only perform the save if any of the fields have actually changed.
        if old_target_end_date != self.target_deadline_date:
            self.save(update_fields=["target_deadline_date"])

    @transaction.atomic
    def update_progression(self):
        """Update the deadline progression based on the current state.

        If no deadline exists, it will be created.

        The total days of suspension will be calculated based on the existing
        suspensions for the instance and service. Closed suspensions are calculated
        by end-start date, while open suspensions are calculated by now-start date.

        If no start date is set on the deadline, the progress will be unset.
        Otherwise, the progress is recalculated and saved only if changed.
        """
        instance = self.instance

        old_process_deadline_date = self.process_deadline_date
        old_process_deadline_days = self.process_deadline_days
        old_total_days_of_suspension = self.total_days_of_suspension

        self.total_days_of_suspension = len(self.get_suspension_dates())

        if not self.start_date:
            # Unset progress if no start date is set
            self.process_deadline_date = None
            self.process_deadline_days = None
        else:
            # Define the end date based on responsible/inquired service.
            responsible = instance.responsible_service()

            # Only update the process deadline date if it is not overridden or not set
            override = self.process_deadline_date_override
            has_date = self.process_deadline_date

            if not override or not has_date:
                self.process_deadline_date = (
                    self._get_enddate_responsible()
                    if responsible and responsible.pk == self.service.pk
                    else self._get_enddate_inquired()
                )
            self.process_deadline_days = self._get_process_deadline_days()

        # only perform the save if any of the fields have actually changed.
        if (
            old_process_deadline_date != self.process_deadline_date
            or old_process_deadline_days != self.process_deadline_days
            or old_total_days_of_suspension != self.total_days_of_suspension
        ):
            self.save(
                update_fields=[
                    "total_days_of_suspension",
                    "process_deadline_date",
                    "process_deadline_days",
                ]
            )

    def update_instance_case_meta(self):
        """Update the instance case meta to reflect the suspension status.

        Save a list of deadline services where an open suspension exist in the case
        meta.
        """
        if not self.instance.case:  # pragma: no cover
            return

        current_value = self.instance.case.meta.get("suspended-services", [])
        new_value = [
            str(d.service.pk)
            for d in self.instance.deadlines.all()
            if d.has_open_suspension()
        ]

        if current_value != new_value:
            self.instance.case.meta["suspended-services"] = new_value
            self.instance.case.save(update_fields=["meta"])

    def _define_startdate(self) -> Optional[datetime]:
        """Define the deadline start date based on the instance and service.

        The responsible service is calculated differently from a inquired service.
        """
        responsible = self.instance.responsible_service()
        return (
            self._get_startdate_responsible()
            if responsible and responsible.pk == self.service.pk
            else self._get_startdate_inquired()
        )

    def get_suspension_dates(self) -> set[date]:
        """Create a list of non-overlapping suspension dates for the deadline."""
        suspension_dates = []
        for suspension in self.suspensions.all():
            suspension_dates.extend(suspension.get_suspension_dates())

        today = now().date()
        offset_date = (
            self.process_deadline_date
            if self.process_deadline_date and self.process_deadline_date < today
            else today
        )

        # Ignore suspension dates that are outside the range of start date and
        # process deadline date (or today if no process deadline date is set).
        if self.start_date and offset_date:
            suspension_dates = [
                d for d in suspension_dates if self.start_date <= d < offset_date
            ]

        # only return unique suspension dates, no overlapping
        return set(suspension_dates)

    def _get_process_deadline_days(self) -> Optional[int]:
        """Calculate the number of days processed since the start date.

        This is the total number of days from the start date to the process deadline date,
        excluding weekends and public holidays if configured to do so.
        """
        today = now().date()
        tmp_date = self.start_date
        offset_date = (
            self.process_deadline_date
            if self.process_deadline_date and self.process_deadline_date < today
            else today
        )

        suspension_dates = self.get_suspension_dates()
        total_days = 0
        while tmp_date < offset_date:
            # If the current day is in the suspension dates, skip it
            if tmp_date in suspension_dates:
                tmp_date += timedelta(days=1)
                continue

            # Ignore weekends and public holidays if configured to do so
            if self.exclude_suspension_date(tmp_date):
                tmp_date += timedelta(days=1)
                continue

            total_days += 1
            tmp_date += timedelta(days=1)

        return total_days

    def _get_enddate_responsible(self) -> Optional[datetime]:
        decision_date = MasterData(self.instance.case).decision_date

        return (
            decision_date.date()
            if decision_date and isinstance(decision_date, datetime)
            else decision_date
        )

    @canton_aware
    def _get_enddate_inquired(self) -> Optional[datetime]:
        """For inquired services, the end date is set to the inquiry answer date."""
        work_item = (
            Inquiry.objects.for_instance(self.instance)
            .addressed_to(str(self.service.pk))
            .order_by("-created_at")
            .first()
        )

        return work_item.closed_at.date() if work_item and work_item.closed_at else None

    def _get_enddate_inquired_ag(self) -> Optional[datetime]:
        """For inquired services in AG, the end date is based on the decision.

        If the decision is set to "Unterlagenergänzung", a suspension is created,
        and no end date is set. For all other decisions, the end date is set to the
        inquiry answer date.
        """
        has_open_claim_suspension = (
            self.suspensions.only_open()
            .filter(
                reason=Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM
            )
            .exists()
        )

        if has_open_claim_suspension:
            return None

        work_item = (
            Inquiry.objects.for_instance(self.instance)
            .addressed_to(str(self.service.pk))
            .order_by("-created_at")
            .first()
        )

        return work_item.closed_at.date() if work_item and work_item.closed_at else None

    @canton_aware
    def _get_startdate_responsible(self) -> Optional[datetime]:
        """Will set the start date for responsible services to the submit date."""
        return self._get_submit_date()

    def _get_startdate_responsible_gr(self) -> Optional[datetime]:
        """Canton GR handles the responsible service start date differently.

        If the formal exam is simplified, the start date is set to the submission date.
        Otherwise, it is set to the publication date.
        """
        work_item = (
            WorkItem.objects.filter(
                case__family__instance=self.instance,
                task__slug="formal-exam",
            )
            .order_by("-created_at")
            .first()
        )
        if work_item:
            if work_item.status != WorkItem.STATUS_COMPLETED:
                # If the formal exam work item is not yet completed, do not set a start date
                return None

            verfahrensart_answer = (
                work_item.document.answers.filter(question="verfahrensart").first()
                if work_item
                else None
            )
            is_simplified = (
                verfahrensart_answer
                and verfahrensart_answer.value
                == "verfahrensart-vereinfachtes-baubewilligungsverfahren"
            )
        else:
            # If no formal exam work item exists for the case, assume simplified,
            # using the submit date as start date.
            is_simplified = True

        if is_simplified:
            return self._get_submit_date()

        # Use the publication date if a publication workitem exists for the given
        # instance type, otherwise fallback to use the submit date.
        publication_workitem = (
            WorkItem.objects.filter(
                case__family__instance=self.instance,
                task__slug="fill-publication",
            )
            .order_by("-created_at")
            .first()
        )
        return (
            self._get_publication_end_date()
            if publication_workitem
            else self._get_submit_date()
        )

    def _get_startdate_inquired(self) -> Optional[datetime]:
        """For inquired services, the start date is set to the inquiry date."""
        inquiry = (
            Inquiry.objects.for_instance(self.instance)
            .addressed_to(self.service)
            .order_by("-created_at")
            .first()
        )

        return inquiry.created_at.date() if inquiry and inquiry.created_at else None

    def _get_target_enddate(self) -> Optional[datetime]:
        suspension_dates = self.get_suspension_dates()

        # Start with the the base process deadline date
        process_deadline_date = self.start_date

        # Apply the lead time of the deadline type to the process deadline date.
        # Ignore the already suspended days.
        # Take into account weekends and public holidays if configured to do so.
        lead_time = self.deadline_type.lead_time if self.deadline_type else 0
        total_lead_days = 0
        while lead_time > 0:
            # If the lead day to add is already in the suspension dates,
            # skip it and continue to the next day.
            if process_deadline_date in suspension_dates:
                # remove matched overlapping suspension date
                suspension_dates.remove(process_deadline_date)
                process_deadline_date += timedelta(days=1)
                continue

            # Ignore weekends and public holidays if configured to do so
            if self.exclude_suspension_date(process_deadline_date):
                process_deadline_date += timedelta(days=1)
                continue

            process_deadline_date += timedelta(days=1)
            total_lead_days += 1
            lead_time -= 1

        # Add the total days of suspension that are not overlapping
        # to the process deadline date
        process_deadline_date += timedelta(days=(len(suspension_dates)))

        return process_deadline_date

    def _get_publication_end_date(self) -> Optional[datetime]:
        """Will return the publication date from the workitem."""
        work_item = (
            WorkItem.objects.filter(
                case__family__instance=self.instance,
                created_by_group=str(self.service.pk),
                task__slug="fill-publication",
            )
            .order_by("-created_at")
            .first()
        )
        publication_end_date_answer = (
            work_item.document.answers.filter(
                question=settings.PUBLICATION["QUESTIONS"]["MUNICIPALITY_END_DATE"]
            ).first()
            if work_item
            else None
        )

        return publication_end_date_answer.date if publication_end_date_answer else None

    def _get_submit_date(self) -> Optional[datetime]:
        submit_date = MasterData(self.instance.case).submit_date

        return (
            submit_date.date()
            if submit_date and isinstance(submit_date, datetime)
            else submit_date
        )
