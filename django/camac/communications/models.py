import os.path

from django.contrib.postgres.fields import ArrayField
from django.db import models

from camac.user.permissions import permission_aware


def entity_for_current_user(request):
    """Return Entity string for the current user.

    This is the string "APPLICANT" if the user
    is an applicant (Ie. has no service groups)
    or the currently-relevant Service ID (also as string)
    """
    return EntityInfo(request).entity() or ""


class EntityInfo:
    def __init__(self, request):
        self.request = request
        self._resolved = None

    @permission_aware
    def entity(self):
        # Return the service ID of the default group, if the default group
        # actually has a service ID. Otherwise, fall back to the first group
        # of the user that does have a service ID.
        # Finally, fall back to empty string if that's also not the case.
        return str(
            self.request.group.service_id
            or self.request.user.get_default_group().service_id
            or (
                self.request.user.groups.filter(service__isnull=False)
                .first()
                .service_id
            )
        )

    def entity_for_applicant(self):
        return "APPLICANT"


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

    def __str__(self):
        atype = "uploaded" if self.file_attachment else "via docs module"
        msg = self.message_id and str(self.message) or "(no msg)"
        return f"Attachment on {msg}: {self.filename} ({atype})"

    @property
    def filename(self):
        if self.file_attachment:
            return os.path.basename(self.file_attachment.name)
        return os.path.basename(self.document_attachment.name)
