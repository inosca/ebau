import logging
from uuid import uuid4

from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from pyxb import (
    IncompleteElementContentError,
    UnprocessedElementContentError,
    UnprocessedKeywordContentError,
)

from .data_preparation import get_document
from .formatters import delivery, status_notification, submit
from .models import Message
from .signals import instance_submitted

logger = logging.getLogger(__name__)


class BaseEventHandler:
    def __init__(self, instance, group_pk=None):
        self.instance = instance
        self.group_pk = group_pk

        self.message_date = timezone.now()
        self.message_id = uuid4()

    def get_data(self):
        return get_document(self.instance.pk)

    def get_xml(self, caluma_data):  # pragma: no cover
        raise NotImplementedError()

    def create_message(self, xml):
        message = Message.objects.create(
            body=xml,
            receiver=self.instance.active_service,
            created_at=self.message_date,
            id=self.message_id,
        )
        return message

    def run(self):
        caluma_data = self.get_data()
        xml = self.get_xml(caluma_data)
        return self.create_message(xml)


class SubmitEventHandler(BaseEventHandler):
    event_type = "submit"

    def get_xml(self, caluma_data):
        try:
            return delivery(
                self.instance,
                caluma_data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=f"{settings.INTERNAL_BASE_URL}/form/edit-page/instance-resource-id/20014/instance-id/{self.instance.pk}",
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, caluma_data, self.event_type
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class FileSubsequentlyEventHandler(SubmitEventHandler):
    event_type = "file subsequently"


class StatusNotificationEventHandler(BaseEventHandler):
    def get_data(self):
        return {"ech-subject": "status notification"}

    def get_xml(self, caluma_data):
        try:
            return delivery(
                self.instance,
                caluma_data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventStatusNotification=status_notification(self.instance),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


@receiver(instance_submitted)
def submit_callback(sender, instance, group_pk, **kwargs):
    if settings.ECH_API:
        handler = SubmitEventHandler(instance, group_pk)
        handler.run()
