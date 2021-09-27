from uuid import uuid4

import reversion
from django.conf import settings
from django.contrib.postgres.fields import ArrayField, JSONField
from django.core.validators import MaxValueValidator
from django.db import models
from django.utils import timezone

from camac.core import models as core_models

from . import permissions


def attachment_path_directory_path(attachment, filename):
    return "attachments/files/{0}/{1}".format(attachment.instance.pk, filename)


@reversion.register()
class Attachment(models.Model):
    attachment_id = models.AutoField(db_column="ATTACHMENT_ID", primary_key=True)
    uuid = models.UUIDField(default=uuid4, unique=True)  # needed for ECH
    name = models.CharField(db_column="NAME", max_length=255)
    instance = models.ForeignKey(
        "instance.Instance",
        models.CASCADE,
        db_column="INSTANCE_ID",
        related_name="attachments",
    )
    path = models.FileField(
        db_column="PATH", max_length=1024, upload_to=attachment_path_directory_path
    )
    size = models.IntegerField(db_column="SIZE")
    date = models.DateTimeField(db_column="DATE", default=timezone.now)
    user = models.ForeignKey(
        "user.User", models.PROTECT, db_column="USER_ID", related_name="attachments"
    )
    mime_type = models.CharField(db_column="MIME_TYPE", max_length=255)
    attachment_sections = models.ManyToManyField(
        "AttachmentSection", related_name="attachments"
    )
    is_parcel_picture = models.PositiveIntegerField(
        db_column="IS_PARCEL_PICTURE", default=0, validators=[MaxValueValidator(1)]
    )
    digital_signature = models.PositiveSmallIntegerField(
        db_column="DIGITAL_SIGNATURE", default=0, validators=[MaxValueValidator(1)]
    )
    is_confidential = models.PositiveSmallIntegerField(
        db_column="IS_CONFIDENTIAL", default=0, validators=[MaxValueValidator(1)]
    )

    identifier = models.CharField(
        db_column="IDENTIFIER", max_length=255, blank=True, null=True
    )
    """
    In old Camac Document module this identifier is used for identification
    and to build thumbnail path.
    Is only present for backwards compatability.
    """

    group = models.ForeignKey(
        "user.Group", models.SET_NULL, related_name="attachments", null=True
    )
    """
    Group attachment has been uploaded with. Needs to be nullable
    (but not blank!) for db backwards compatibility with old plain camac
    document module.
    """

    question = models.CharField(
        db_column="QUESTION", max_length=255, blank=True, null=True
    )
    """
    Used to reference to form question. Allows multiple attachments per question.
    """

    service = models.ForeignKey(
        "user.Service",
        models.SET_NULL,
        db_column="SERVICE_ID",
        related_name="+",
        blank=True,
        null=True,
    )
    """
    Service attachment has been uploaded with.
    """

    context = JSONField(default=dict)

    @property
    def display_name(self):
        """
        Get displayName from context; fall back to name without extension.

        This is only used by eCH at the moment.

        :return: str
        """
        display_name = self.context.get("displayName")
        if not display_name:
            display_name = ".".join(self.name.split(".")[:-1])
        return display_name

    class Meta:
        managed = True
        db_table = "ATTACHMENT"


class AttachmentSectionQuerySet(models.QuerySet):
    def filter_group(self, group, instance=None):
        permission_info = permissions.section_permissions(group, instance)
        visible_section_ids = permission_info.keys()

        return self.filter(pk__in=visible_section_ids)


def _get_default_mime_types():
    """Make sure the default of allowed_mime_types is a callable."""
    return settings.DEFAULT_DOCUMENT_MIMETYPES


class AttachmentSection(core_models.MultilingualModel, models.Model):
    RECIPIENT_TYPE_CHOICES = (
        ("applicant", "applicant"),
        ("municipality", "municipality"),
        ("service", "service"),
    )
    MIME_TYPE_CHOICES = (
        (entry, entry) for entry in settings.ALLOWED_DOCUMENT_MIMETYPES
    )
    objects = AttachmentSectionQuerySet.as_manager()
    attachment_section_id = models.AutoField(
        db_column="ATTACHMENT_SECTION_ID", primary_key=True
    )
    name = models.CharField(db_column="NAME", max_length=100)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=2000, blank=True, null=True
    )
    sort = models.IntegerField(db_column="SORT", db_index=True, default=0)
    notification_template = models.ForeignKey(
        "notification.NotificationTemplate",
        models.SET_NULL,
        null=True,
        blank=True,
        db_column="NOTIFICATION_TEMPLATE_ID",
        related_name="+",
    )
    recipient_types = ArrayField(
        models.CharField(max_length=12, choices=RECIPIENT_TYPE_CHOICES),
        null=True,
        blank=True,
    )
    allowed_mime_types = ArrayField(
        models.CharField(max_length=255, choices=MIME_TYPE_CHOICES),
        default=_get_default_mime_types,
    )

    def get_permission(self, group, instance=None):
        return permissions.section_permissions(group, instance).get(self.pk)

    def can_destroy(self, attachment, group):
        permission_class = self.get_permission(group, attachment.instance)
        return (
            permission_class.can_destroy(attachment, group)
            if permission_class
            else False
        )

    def can_write(self, attachment, group):
        permission_class = self.get_permission(
            group, attachment.instance if attachment else None
        )
        return (
            permission_class.can_write(attachment, group) if permission_class else False
        )

    class Meta:
        managed = True
        db_table = "ATTACHMENT_SECTION"


class AttachmentSectionT(models.Model):
    attachment_section = models.ForeignKey(
        AttachmentSection,
        models.CASCADE,
        db_column="ATTACHMENT_SECTION_ID",
        related_name="trans",
    )
    language = models.CharField(db_column="LANGUAGE", max_length=2)
    name = models.CharField(db_column="NAME", max_length=100, blank=True, null=True)
    description = models.CharField(
        db_column="DESCRIPTION", max_length=2000, blank=True, null=True
    )

    class Meta:
        managed = True
        db_table = "ATTACHMENT_SECTION_T"


class Template(models.Model):
    template_id = models.AutoField(db_column="TEMPLATE_ID", primary_key=True)
    name = models.CharField(max_length=255, db_column="NAME")
    path = models.FileField(max_length=1024, upload_to="templates", db_column="PATH")
    group = models.ForeignKey(
        "user.Group", models.CASCADE, null=True, blank=True, related_name="templates"
    )
    service = models.ForeignKey(
        "user.Service", models.CASCADE, null=True, related_name="templates"
    )

    class Meta:
        db_table = "TEMPLATE"
        unique_together = ["name", "service"]


class AttachmentDownloadHistory(models.Model):
    date_time = models.DateTimeField(default=timezone.now)
    keycloak_id = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    attachment = models.ForeignKey(
        "Attachment", models.CASCADE, related_name="download_history"
    )
    group = models.ForeignKey(
        "user.Group",
        models.CASCADE,
        related_name="attachment_download_history",
        null=True,
    )
