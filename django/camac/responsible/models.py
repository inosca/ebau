from django.db import models


class ResponsibleAllocation(models.Model):
    allocation_id = models.AutoField(db_column="ALLOCATION_ID", primary_key=True)
    group = models.ForeignKey(
        "user.Group", models.DO_NOTHING, db_column="GROUP_ID", related_name="+"
    )
    location = models.ForeignKey(
        "user.Location", models.DO_NOTHING, db_column="LOCATION_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "RESPONSIBLE_ALLOCATION"


class IrEditresponsiblegroup(models.Model):
    instance_resource = models.OneToOneField(
        "core.InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    responsible_role = models.ForeignKey(
        "user.Role",
        models.CASCADE,
        db_column="RESPONSIBLE_ROLE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    table_name = models.CharField(db_column="TABLE_NAME", max_length=30)
    column_name = models.CharField(db_column="COLUMN_NAME", max_length=30)

    class Meta:
        managed = True
        db_table = "IR_EDITRESPONSIBLEGROUP"


class IrEditresponsibleuser(models.Model):
    instance_resource = models.OneToOneField(
        "core.InstanceResource",
        models.CASCADE,
        db_column="INSTANCE_RESOURCE_ID",
        primary_key=True,
        related_name="+",
    )
    table_name = models.CharField(
        db_column="TABLE_NAME", max_length=30, blank=True, null=True
    )
    column_name = models.CharField(
        db_column="COLUMN_NAME", max_length=30, blank=True, null=True
    )
    is_service_responsible = models.NullBooleanField(db_column="IS_SERVICE_RESPONSIBLE")
    is_required = models.NullBooleanField(db_column="IS_REQUIRED")

    class Meta:
        managed = True
        db_table = "IR_EDITRESPONSIBLEUSER"


class ASetresponsiblegroup(models.Model):
    action = models.OneToOneField(
        "core.Action",
        models.CASCADE,
        db_column="ACTION_ID",
        primary_key=True,
        related_name="+",
    )
    table_name = models.CharField(db_column="TABLE_NAME", max_length=30)
    column_name = models.CharField(db_column="COLUMN_NAME", max_length=30)
    is_service_responsible = models.NullBooleanField(db_column="IS_SERVICE_RESPONSIBLE")
    is_required = models.NullBooleanField(db_column="IS_REQUIRED")

    class Meta:
        managed = True
        db_table = "A_SETRESPONSIBLEGROUP"


class ResponsibleService(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )
    responsible_user = models.ForeignKey(
        "user.User",
        models.DO_NOTHING,
        db_column="RESPONSIBLE_USER_ID",
        related_name="+",
    )

    class Meta:
        managed = True
        db_table = "RESPONSIBLE_SERVICE"


class ResponsibleServiceLog(models.Model):
    responsible_service_log_id = models.AutoField(
        db_column="RESPONSIBLE_SERVICE_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID", blank=True, null=True)
    action = models.CharField(db_column="ACTION", max_length=5, blank=True, null=True)
    data = models.TextField(db_column="DATA", blank=True, null=True)
    id1 = models.IntegerField(db_column="ID1", blank=True, null=True)
    field1 = models.CharField(max_length=30, db_column="FIELD1", blank=True, null=True)
    id2 = models.IntegerField(db_column="ID2", blank=True, null=True)
    field2 = models.CharField(max_length=30, db_column="FIELD2", blank=True, null=True)

    class Meta:
        managed = True
        db_table = "RESPONSIBLE_SERVICE_LOG"


class ResponsibleServiceAllocation(models.Model):
    service_allocation_id = models.AutoField(
        db_column="SERVICE_ALLOCATION_ID", primary_key=True
    )
    location = models.ForeignKey(
        "user.Location", models.DO_NOTHING, db_column="LOCATION_ID", related_name="+"
    )
    user = models.ForeignKey(
        "user.User", models.DO_NOTHING, db_column="USER_ID", related_name="+"
    )
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, db_column="SERVICE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "RESPONSIBLE_SERVICE_ALLOCATION"
