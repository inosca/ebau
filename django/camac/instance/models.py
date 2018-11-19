import reversion
from django.contrib.postgres.fields import JSONField
from django.db import models


class FormState(models.Model):
    form_state_id = models.AutoField(db_column="FORM_STATE_ID", primary_key=True)
    name = models.CharField(db_column="NAME", max_length=50)

    class Meta:
        managed = True
        db_table = "FORM_STATE"


class Form(models.Model):
    """Represents type of a form."""

    form_id = models.AutoField(db_column="FORM_ID", primary_key=True)
    form_state = models.ForeignKey(
        FormState, models.DO_NOTHING, db_column="FORM_STATE_ID", related_name="+"
    )
    name = models.CharField(db_column="NAME", max_length=500, unique=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM"


class FormT(models.Model):
    form = models.ForeignKey(
        Form, models.CASCADE, db_column="FORM_ID", related_name="+"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=500, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "FORM_T"


class InstanceState(models.Model):
    instance_state_id = models.AutoField(
        db_column="INSTANCE_STATE_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100, unique=True)
    sort = models.IntegerField(db_column="SORT", db_index=True, default=0)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=1000, blank=True, null=True
    )

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = "INSTANCE_STATE"


class InstanceStateT(models.Model):
    instance_state = models.ForeignKey(
        InstanceState, models.CASCADE, db_column="INSTANCE_STATE_ID", related_name="+"
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
    group = models.ForeignKey("user.Group", models.DO_NOTHING, related_name="+")
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", null=True
    )
    user = models.ForeignKey("user.User", models.DO_NOTHING, related_name="+")
    duration = models.DurationField(null=True, blank=True)
    text = models.TextField()
    creation_date = models.DateTimeField()
    modification_date = models.DateTimeField()


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


@reversion.register()
class FormField(models.Model):
    """
    Represents fields of an instance form.

    What form type field references is assigned on instance itself.
    """

    instance = models.ForeignKey(Instance, models.CASCADE, related_name="fields")
    name = models.CharField(max_length=500)
    value = JSONField(db_index=True)

    class Meta:
        unique_together = (("instance", "name"),)
