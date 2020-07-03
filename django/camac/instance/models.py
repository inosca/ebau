import logging

import reversion
from django.conf import settings
from django.contrib.postgres.fields import JSONField
from django.db import models

from camac.constants.kt_bern import (
    INSTANCE_STATE_DONE,
    INSTANCE_STATE_SB1,
    INSTANCE_STATE_SB2,
    INSTANCE_STATE_TO_BE_FINISHED,
)
from camac.core.models import HistoryActionConfig, InstanceService

from ..core import models as core_models

log = logging.getLogger(__name__)


class FormState(models.Model):
    form_state_id = models.AutoField(db_column="FORM_STATE_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=50)

    class Meta:
        managed = True
        db_table = "FORM_STATE"


class Form(core_models.MultilingualModel, models.Model):
    """Represents type of a form."""

    form_id = models.AutoField(db_column="FORM_ID", primary_key=True)
    form_state = models.ForeignKey(
        FormState, models.DO_NOTHING, db_column="FORM_STATE_ID", related_name="+"
    )
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM"


class FormT(models.Model):
    form = models.ForeignKey(
        Form, models.CASCADE, db_column="FORM_ID", related_name="trans"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM_T"


class InstanceState(core_models.MultilingualModel, models.Model):
    instance_state_id = models.AutoField(
        db_column="INSTANCE_STATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    sort = models.IntegerField(db_column="SORT", db_index=True, default=0)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE"


class InstanceStateT(models.Model):
    instance_state = models.ForeignKey(
        InstanceState,
        models.CASCADE,
        db_column="INSTANCE_STATE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE_T"


class InstanceStateDescription(models.Model):
    """
    Instance state description.

    Obsolete as integrated into core now. Still added for backwards
    compatability with Kanton URI project.
    """

    instance_state = models.OneToOneField(
        InstanceState,
        models.DO_NOTHING,
        db_column="INSTANCE_STATE_ID",
        primary_key=True,
        related_name="+",
    )
    description = models.CharField(db_column="DESCRIPTION", max_length=255)

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE_DESCRIPTION"


@reversion.register()
class Instance(models.Model):
    """
    Instance is the case entity of any request.

    Instance is always based on a type of form.
    """

    instance_id = models.AutoField(db_column="INSTANCE_ID", primary_key=True)
    instance_state = models.ForeignKey(
        InstanceState,
        models.DO_NOTHING,
        db_column="INSTANCE_STATE_ID",
        related_name="+",
    )
    form = models.ForeignKey(
        Form, models.DO_NOTHING, db_column="FORM_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    creation_date = models.DateTimeField(db_column="CREATION_DATE")
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    previous_instance_state = models.ForeignKey(
        InstanceState,
        models.DO_NOTHING,
        db_column="PREVIOUS_INSTANCE_STATE_ID",
        related_name="+",
    )
    identifier = models.CharField(
        db_column="IDENTIFIER", max_length=50, blank=True, null=True
    )
    location = models.ForeignKey(
        "user.Location", models.PROTECT, null=True, blank=True, db_column="LOCATION_ID"
    )
    services = models.ManyToManyField("user.Service", through="core.InstanceService")

    def active_service(self, service_filters=None):
        service_filters = (
            service_filters
            if service_filters
            else settings.APPLICATION.get("ACTIVE_SERVICE_FILTERS", {})
        )
        instance_services = InstanceService.objects.filter(
            active=1, instance=self, **service_filters
        ).order_by("-pk")
        instance_service = instance_services.first()

        if instance_services.count() > 1:
            log.warning(
                f"Instance {self.pk}: Multiple active services, picking most recent one: {instance_service.service}!"
            )

        return instance_service.service if instance_service else None

    def _responsible_service_kt_bern(self):
        service_filters = settings.APPLICATION.get("ACTIVE_SERVICE_FILTERS", {})
        if self.instance_state.pk in [
            INSTANCE_STATE_SB1,
            INSTANCE_STATE_SB2,
            INSTANCE_STATE_TO_BE_FINISHED,
            INSTANCE_STATE_DONE,
        ]:
            service_filters = settings.APPLICATION.get(
                "ACTIVE_BAUKONTROLLE_FILTERS", {}
            )
        return self.active_service(service_filters)

    def responsible_service(self):
        """
        Call application specific method and fallback to active_service.

        Application specific methods have to be named like this:
        _responsible_service_{application_name}
        """
        func = f"_responsible_service_{settings.APPLICATION_NAME}"
        if hasattr(self, func):
            return getattr(self, func)()
        return self.active_service()

    class Meta:
        managed = True
        db_table = "INSTANCE"


class InstanceResponsibility(models.Model):
    instance = models.ForeignKey(
        Instance, models.CASCADE, related_name="responsibilities"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, db_column="SERVICE_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        db_column="USER_ID",
        related_name="responsibilities",
    )

    class Meta:
        unique_together = (("instance", "user", "service"),)


class JournalEntry(models.Model):
    instance = models.ForeignKey(Instance, models.CASCADE, related_name="journal")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey("user.User", models.DO_NOTHING, related_name="+")
    text = models.TextField(blank=True, null=True)
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField()


class HistoryEntry(core_models.MultilingualModel, models.Model):
    instance = models.ForeignKey(Instance, models.CASCADE, related_name="history")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey("user.User", models.DO_NOTHING, related_name="+")
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.TextField(blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    history_type = models.CharField(
        max_length=20, choices=HistoryActionConfig.HISTORY_TYPES_TUPLE
    )


class HistoryEntryT(models.Model):
    title = models.TextField()
    body = models.TextField(blank=True, null=True)
    history_entry = models.ForeignKey(
        HistoryEntry, models.CASCADE, related_name="trans"
    )
    language = models.CharField(max_length=2)


class Issue(models.Model):
    STATE_OPEN = "open"
    STATE_DELAYED = "delayed"
    STATE_DONE = "done"
    STATE_CHOICES = (STATE_OPEN, STATE_DELAYED, STATE_DONE)
    STATE_CHOICES_TUPLE = ((choice, choice) for choice in STATE_CHOICES)

    instance = models.ForeignKey(Instance, models.CASCADE, related_name="issues")
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    deadline_date = models.DateField()
    state = models.CharField(
        max_length=20, choices=STATE_CHOICES_TUPLE, default=STATE_OPEN
    )
    text = models.TextField()


class IssueTemplate(models.Model):
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    deadline_length = models.PositiveIntegerField()
    text = models.TextField()


class IssueTemplateSet(models.Model):
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    issue_templates = models.ManyToManyField(
        IssueTemplate, related_name="issue_template_sets", blank=True
    )
    name = models.CharField(max_length=500)


@reversion.register()
class FormField(models.Model):
    """
    Represents fields of an instance form.

    What form type field references is assigned on instance itself.
    """

    instance = models.ForeignKey(Instance, models.CASCADE, related_name="fields")
    name = models.CharField(max_length=500)
    value = JSONField()

    class Meta:
        unique_together = (("instance", "name"),)
