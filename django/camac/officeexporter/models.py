from django.db import models


class OfficeExporterDocx(models.Model):
    officeexporter_docx_id = models.AutoField(
        db_column="OFFICEEXPORTER_DOCX_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    php_class = models.CharField(db_column="PHP_CLASS", max_length=100)

    class Meta:
        managed = True
        db_table = "OFFICEEXPORTER_DOCX"


class OfficeExporterDocxT(models.Model):
    officeexporter_docx = models.ForeignKey(
        OfficeExporterDocx,
        models.CASCADE,
        db_column="OFFICEEXPORTER_DOCX_ID",
        related_name="+",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100)

    class Meta:
        managed = True
        db_table = "OFFICEEXPORTER_DOCX_T"
        unique_together = (("officeexporter_docx", "language"),)


class OfficeExporterDocxLog(models.Model):
    officeexporter_docx_log_id = models.AutoField(
        db_column="OFFICEEXPORTER_DOCX_LOG_ID", primary_key=True
    )
    modification_date = models.DateTimeField(db_column="MODIFICATION_DATE")
    user_id = models.IntegerField(db_column="USER_ID")
    action = models.CharField(db_column="ACTION", max_length=500)
    data = models.TextField(db_column="DATA")
    id = models.IntegerField(db_column="ID")

    class Meta:
        managed = True
        db_table = "OFFICEEXPORTER_DOCX_LOG"


class OfficeExporterDocxRole(models.Model):
    officeexporter_docx = models.ForeignKey(
        OfficeExporterDocx,
        models.CASCADE,
        db_column="OFFICEEXPORTER_DOCX_ID",
        related_name="+",
    )
    role = models.ForeignKey(
        "user.Role", models.CASCADE, db_column="ROLE_ID", related_name="+"
    )

    class Meta:
        managed = True
        db_table = "OFFICEEXPORTER_DOCX_ROLE"
        unique_together = (("officeexporter_docx", "role"),)
