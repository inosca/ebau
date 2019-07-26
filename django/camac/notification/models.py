from django.db import models

from ..core import models as core_models


class NotificationTemplate(core_models.MultilingualModel, models.Model):
    purpose = models.CharField(
        db_column="PURPOSE", max_length=100, db_index=True, blank=True, null=True
    )
    subject = models.TextField(db_column="SUBJECT", blank=True, null=True)
    body = models.TextField(db_column="BODY", blank=True, null=True)

    def __str__(self):
        return self.get_trans_attr("subject")

    class Meta:
        managed = True
        db_table = "NOTIFICATION_TEMPLATE"


class NotificationTemplateT(models.Model):
    template = models.ForeignKey(
        NotificationTemplate,
        models.CASCADE,
        db_column="TEMPLATE_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    purpose = models.CharField(db_column="PURPOSE", max_length=100)
    subject = models.TextField(db_column="SUBJECT")
    body = models.TextField(db_column="BODY")

    class Meta:
        managed = True
        db_table = "NOTIFICATION_TEMPLATE_T"
