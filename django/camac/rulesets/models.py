from datetime import date, timedelta

from caluma.caluma_form.models import Form
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django.db.models import Q

from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.rulesets.holidays import AargauAdministrationHolidays
from camac.settings.modules.rulesets_schema import DistributionDeadlineRuleConfig
from camac.user.models import Service, User
from camac.utils import is_weekend_day


class ResponsibleUserRuleQuerySet(models.QuerySet):
    def get_responsible_user_for_instance(
        self,
        instance: Instance,
        service: Service,
    ) -> User | None:
        """Get the responsible user of instance for a given service.

        This method tries to match the responsible user rules to a given
        instance and will return the responsible user of the first rule that
        matches. The priority of the rules is determined via the sort property.
        """

        municipality = MasterData.from_case_id(instance.case_id).municipality_slug
        form_slug = instance.case.document.form_id

        match_filters = Q(application_types__pk=form_slug)

        if municipality is not None:
            match_filters |= Q(municipalities__pk=int(municipality))

        match = (
            self.select_related("responsible_user")
            .filter(Q(service=service) & Q(match_filters))
            .first()
        )

        if not match:
            return None

        return match.responsible_user


class ResponsibleUserRule(models.Model):
    """Rule to define a designated responsible user on any instance for a service.

    This represents a rule where depending on the application type or the
    municipality of a given instance a designated responsible user is returned.

    Each service can define their own rules that will be evaluated every time
    that service is being involved in an instance (instance submitted, inquiry
    sent, read only permission granted). If the defined rules match a user, that
    user will be automatically assigned as responsible user for that service on
    that instance.

    The rules will be evaluated in a user defined order - the first one that
    matches on the given instance will be returned and used.
    """

    sort = models.PositiveIntegerField(default=0)
    application_types = models.ManyToManyField(to=Form, blank=True)
    municipalities = models.ManyToManyField(to=Service, blank=True)
    service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name="+",
    )
    responsible_user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name="+",
    )

    objects: ResponsibleUserRuleQuerySet = ResponsibleUserRuleQuerySet.as_manager()

    class Meta:
        unique_together = ("service", "sort")
        ordering = ["sort"]
        indexes = [models.Index(fields=["sort"])]


class DistributionDeadlineRuleQuerySet(models.QuerySet):
    def get_default_deadline_for_inquiry(self, inquiry: WorkItem) -> date | None:
        """Get the default deadline (if available) for a given inquiry."""

        rule = self.filter(
            source_service_id=int(inquiry.controlling_groups[0]),
            target_service_id=int(inquiry.addressed_groups[0]),
        ).first()

        if not rule:
            return None

        return rule.get_deadline()


class DistributionDeadlineRule(models.Model):
    """Rule to define a default deadline for inquiries.

    Every service may define a lead time for each other service that will be
    suggested in the distribution module when inviting the target service.

    For services belonging to the specified service groups, certain holidays may
    be excluded from the calculated deadline.
    """

    source_service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name="+",
    )
    target_service = models.ForeignKey(
        to=Service,
        on_delete=models.CASCADE,
        related_name="+",
    )
    lead_time = models.PositiveIntegerField(validators=[MaxValueValidator(365)])

    def should_exclude_holidays(self) -> bool:
        module_config: DistributionDeadlineRuleConfig = (
            settings.RULESETS.distribution_deadline_rule
        )

        return (
            self.target_service.service_group.name
            in module_config.exclude_holidays_for_service_groups
        )

    def get_deadline(self) -> date:
        today = date.today()
        deadline = today + timedelta(days=self.lead_time)

        exclude_holidays = self.should_exclude_holidays()
        affected_years = [year for year in range(today.year, deadline.year + 2)]
        holidays = AargauAdministrationHolidays(years=affected_years)

        current_date = today
        while current_date <= deadline:
            if exclude_holidays and not holidays.is_working_day(current_date):
                deadline += timedelta(days=1)
            elif is_weekend_day(current_date):
                deadline += timedelta(days=1)

            current_date += timedelta(days=1)

        return deadline

    objects: DistributionDeadlineRuleQuerySet = (
        DistributionDeadlineRuleQuerySet.as_manager()
    )

    class Meta:
        unique_together = ("source_service", "target_service")
