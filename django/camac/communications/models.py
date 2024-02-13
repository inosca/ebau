import os.path

from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


def entity_for_current_user(request):
    """Return Entity string for the current user.

    This is the string "APPLICANT" if the user
    is an applicant (Ie. has no service groups)
    or the currently-relevant Service ID (also as string)
    """
    return str((request.group and request.group.service_id) or "APPLICANT")


class CommunicationsTopic(models.Model):
    instance = models.ForeignKey(
        "instance.Instance",
        on_delete=models.CASCADE,
    )
    initiated_by = models.ForeignKey(
        "user.User", on_delete=models.DO_NOTHING, related_name="+"
    )
    subject = models.TextField()
    created = models.DateTimeField(auto_now_add=True)

    allow_replies = models.BooleanField(default=True)

    involved_entities = ArrayField(models.CharField(max_length=50), blank=True)
    initiated_by_entity = models.CharField(max_length=50)


class CommunicationsReadMarker(models.Model):
    read_at = models.DateTimeField(auto_now_add=True)
    message = models.ForeignKey(
        "CommunicationsMessage", on_delete=models.CASCADE, related_name="read_by"
    )
    entity = models.CharField(max_length=50)


class CommunicationsMessage(models.Model):
    topic = models.ForeignKey(
        CommunicationsTopic, on_delete=models.CASCADE, related_name="messages"
    )
    body = models.TextField()

    created_by = models.CharField(max_length=50)
    created_by_user = models.ForeignKey(
        "user.User", on_delete=models.DO_NOTHING, related_name="+", null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(default=None, null=True, blank=True)

    def mark_as_read_by_entity(self, entity):
        """Mark this message, and all messages before, as "read".

        When a message is marked as "read", we assume the user has also
        seen all messages in the same topic that were there before it.
        """
        # created_at__lte=self.created_at includes self, so no
        # explicit marking for "self"
        for message in self.topic.messages.filter(created_at__lte=self.created_at):
            message.read_by.get_or_create(entity=entity)


def attachment_path_directory_path(attachment, filename):
    return "communications/files/{0}/{1}/{2}".format(
        attachment.message.topic.instance_id, attachment.message.topic.pk, filename
    )


class CommunicationsAttachment(models.Model):
    message = models.ForeignKey(
        CommunicationsMessage, on_delete=models.CASCADE, related_name="attachments"
    )
    file_attachment = models.FileField(
        null=True, default=None, blank=True, upload_to=attachment_path_directory_path
    )
    file_type = models.CharField(max_length=250, null=True, default=None, blank=True)

    document_attachment = models.ForeignKey(
        "document.Attachment",
        on_delete=models.DO_NOTHING,
        related_name="+",
        blank=True,
        null=True,
        default=None,
    )
    alexandria_file = models.ForeignKey(
        "alexandria_core.File",
        on_delete=models.DO_NOTHING,
        related_name="+",
        blank=True,
        null=True,
        default=None,
    )

    def __str__(self):
        atype = "uploaded" if self.file_attachment else "via docs module"
        msg = self.message_id and str(self.message) or "(no msg)"
        return f"Attachment on {msg}: {self.filename} ({atype})"

    @property
    def filename(self):
        if self.file_attachment:
            return os.path.basename(self.file_attachment.name)

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            return os.path.basename(self.document_attachment.name)

        return self.alexandria_file.name

    @property
    def display_name(self):
        if self.file_attachment:
            return self.filename

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            return self.document_attachment.context.get("displayName", self.filename)

        return self.alexandria_file.document.title.translate()

    @property
    def is_replaced(self):
        if self.file_attachment:
            return False

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            return self.document_attachment.context.get("isReplaced", False)

        return self.alexandria_file.document.marks.filter(slug="void").exists()

    @property
    def content_type(self):
        if self.file_attachment:
            return self.file_type

        if settings.APPLICATION["DOCUMENT_BACKEND"] == "camac-ng":
            return self.document_attachment.mime_type

        return self.alexandria_file.mime_type
