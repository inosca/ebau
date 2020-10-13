from django.db import models

from ..core import models as core_models


class NotificationTemplate(core_models.MultilingualModel, models.Model):
    slug = models.SlugField(max_length=100, unique=True, db_index=False)
    purpose = models.CharField(
        db_column="PURPOSE", max_length=100, db_index=True, blank=True, null=True
    )
    subject = models.TextField(db_column="SUBJECT", blank=True, null=True)
    body = models.TextField(db_column="BODY", blank=True, null=True)
    service = models.ForeignKey(
        "user.Service", models.DO_NOTHING, related_name="+", blank=True, null=True
    )
    EMAIL = "email"
    TEXT = "textcomponent"
    TYPE_CHOICES = [(EMAIL, "E-Mail"), (TEXT, "Textcomponent")]
    type = models.CharField(
        max_length=20, blank=True, null=True, choices=TYPE_CHOICES, default=EMAIL
    )

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
    template_slug = models.ForeignKey(
        NotificationTemplate, models.CASCADE, to_field="slug"
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    purpose = models.CharField(db_column="PURPOSE", max_length=100)
    subject = models.TextField(db_column="SUBJECT")
    body = models.TextField(db_column="BODY")

    class Meta:
        managed = True
        db_table = "NOTIFICATION_TEMPLATE_T"


class ProjectSubmitterData(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        on_delete=models.DO_NOTHING,
        db_column="INSTANCE_ID",
        related_name="+",
    )
    name = models.CharField(max_length=250, null=True)
    email = models.CharField(max_length=250, null=True)
    answer = models.CharField(max_length=250, null=True)

    class Meta:
        managed = False
        db_table = "PROJECT_SUBMITTER_DATA"
