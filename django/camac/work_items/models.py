import uuid_extensions
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from localized_fields.fields import LocalizedCharField

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
    class ResponsibilityRuleChoices(models.TextChoices):
        NONE = "NONE", _("No service")
        RESPONSIBLE_USER = (
            "RESPONSIBLE_USER",
            _("Current service and responsible user (if exists)"),
        )
        CURRENT_USER = "CURRENT_USER", _("Current service and current user")
        NO_USER = "NO_USER", _("Current service and no user")

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
    responsibility_rule = models.CharField(
        choices=ResponsibilityRuleChoices.choices,
        max_length=20,
        verbose_name=_("Responsibility rule"),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Work item template")
        verbose_name_plural = _("Work item templates")
        ordering = ["sort"]


class WorkItemListFilterPreset(models.Model):
    class PresetCategoryChoices(models.TextChoices):
        STANDARD = "STANDARD", _("Standard filter preset category")
        SERVICE = (
            "SERVICE",
            _("Service filter preset category"),
        )
        SERVICE_GROUP = "SERVICE_GROUP", _("Service group filter preset category")

    id = models.UUIDField(
        primary_key=True,
        default=uuid_extensions.uuid7,
        editable=False,
        verbose_name=_("ID"),
    )
    name = LocalizedCharField(verbose_name=_("Name"))
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
    query_params = models.JSONField(verbose_name=_("Query params"))
    prefilter_work_item_templates = models.BooleanField(
        default=False, verbose_name=_("Prefilter work item templates")
    )
    work_item_templates = models.ManyToManyField(
        "work_items.WorkItemTemplate",
        related_name="filter_presets",
        blank=True,
        verbose_name=_("Work item templates"),
    )
    prefilter_tasks = models.BooleanField(
        default=False, verbose_name=_("Prefilter tasks")
    )
    tasks = ArrayField(
        models.CharField(max_length=150),
        default=list,
        blank=True,
        verbose_name=_("Tasks"),
    )

    def __str__(self):
        return self.name.get()

    class Meta:
        verbose_name = _("Work item list filter preset")
        verbose_name_plural = _("Work item list filter presets")
