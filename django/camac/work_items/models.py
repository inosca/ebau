import uuid_extensions
from django.db import models
from django.utils.translation import gettext_lazy as _

from camac.models import dynamic_default_value


@dynamic_default_value(0)
def next_sort():
    last = (
        WorkItemTemplate.objects.order_by("-sort")
        .values_list("sort", flat=True)
        .first()
    )

    return last + 1 if last else 0


class WorkItemTemplate(models.Model):
    id = models.UUIDField(
        primary_key=True,
        default=uuid_extensions.uuid7,
        editable=False,
        verbose_name=_("ID"),
    )
    sort = models.PositiveIntegerField(default=next_sort)
    services = models.ManyToManyField(
        "user.Service",
        blank=True,
        verbose_name=_("Services"),
    )
    service_groups = models.ManyToManyField(
        "user.ServiceGroup",
        blank=True,
        verbose_name=_("Service groups"),
    )
    name = models.CharField(
        blank=False,
        null=False,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name=_("Description"),
    )
    lead_time = models.PositiveIntegerField(
        blank=True,
        null=True,
        verbose_name=_("Lead time in days"),
        help_text=_(
            "The current date in addition to this value will determine the deadline"
        ),
    )
    addressed_to_current_service = models.BooleanField(
        default=False,
        verbose_name=_("Automatically addressed to current service"),
    )
    assigned_to_current_user = models.BooleanField(
        default=False,
        verbose_name=_("Automatically assigned to current user"),
        help_text=_(
            'This can only be enabled if "Automatically addressed to current service" is enabled as well'
        ),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Work item template")
        verbose_name_plural = _("Work item templates")
        ordering = ["sort"]
        constraints = [
            # Make sure that assigned_to_current_user can only be true if
            # addressed_to_current_service is true as well.
            models.CheckConstraint(
                check=models.Q(assigned_to_current_user=False)
                | models.Q(
                    assigned_to_current_user=True,
                    addressed_to_current_service=True,
                ),
                name="current_user_requires_current_service",
            )
        ]
