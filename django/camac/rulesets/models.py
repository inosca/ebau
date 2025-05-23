from caluma.caluma_form.models import Form
from django.db import models
from django.db.models import Q

from camac.instance.master_data import MasterData
from camac.instance.models import Instance
from camac.user.models import Service, User


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
