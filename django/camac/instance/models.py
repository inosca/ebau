from django.contrib.postgres.fields import JSONField
from django.db import models


class FormState(models.Model):
    form_state_id = models.AutoField(
        db_column='FORM_STATE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=50)

    class Meta:
        managed = True
        db_table = 'FORM_STATE'


class Form(models.Model):
    """Represents type of a form."""

    form_id = models.AutoField(db_column='FORM_ID', primary_key=True)
    form_state = models.ForeignKey(
        FormState, models.DO_NOTHING, db_column='FORM_STATE_ID',
        related_name='+')
    name = models.CharField(db_column='NAME', max_length=500, unique=True)
    description = models.CharField(
        db_column='DESCRIPTION', max_length=1000, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'FORM'


class InstanceState(models.Model):
    instance_state_id = models.AutoField(
        db_column='INSTANCE_STATE_ID', primary_key=True)
    name = models.CharField(db_column='NAME', max_length=100, unique=True)
    sort = models.IntegerField(db_column='SORT')

    class Meta:
        managed = True
        db_table = 'INSTANCE_STATE'


class InstanceStateDescription(models.Model):
    # TODO move instance state description to instance state
    # migrate data
    instance_state = models.OneToOneField(
        InstanceState, models.DO_NOTHING, db_column='INSTANCE_STATE_ID',
        primary_key=True, related_name='description')
    description = models.CharField(db_column='DESCRIPTION', max_length=255)

    class Meta:
        managed = True
        db_table = 'INSTANCE_STATE_DESCRIPTION'


class Instance(models.Model):
    """
    Instance is the case entity of any request.

    Instance is always based on a type of form.
    """

    instance_id = models.AutoField(db_column='INSTANCE_ID', primary_key=True)
    instance_state = models.ForeignKey(
        InstanceState, models.DO_NOTHING, db_column='INSTANCE_STATE_ID',
        related_name='+')
    form = models.ForeignKey(Form, models.DO_NOTHING,
                             db_column='FORM_ID', related_name='+')
    user = models.ForeignKey('user.User', models.DO_NOTHING,
                             db_column='USER_ID', related_name='+')
    group = models.ForeignKey('user.Group', models.DO_NOTHING,
                              db_column='GROUP_ID', related_name='+')
    """
    TODO: might be removed? Not sure what use case this is needed for.
    """
    creation_date = models.DateTimeField(db_column='CREATION_DATE')
    modification_date = models.DateTimeField(db_column='MODIFICATION_DATE')
    previous_instance_state = models.ForeignKey(
        InstanceState, models.DO_NOTHING,
        db_column='PREVIOUS_INSTANCE_STATE_ID', related_name='+')
    identifier = models.CharField(db_column='IDENTIFIER', max_length=50,
                                  blank=True, null=True)
    location = models.ForeignKey('user.Location', models.PROTECT, null=True,
                                 blank=True, db_column='LOCATION_ID')

    class Meta:
        managed = True
        db_table = 'INSTANCE'


class FormField(models.Model):
    """
    Represents fields of an instance form.

    What form type field references is assigned on instance itself.
    """

    instance = models.ForeignKey(Instance, models.CASCADE,
                                 related_name='fields')
    name = models.CharField(max_length=500)
    value = JSONField()

    class Meta:
        unique_together = (('instance', 'name'),)
