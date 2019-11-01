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
from .formatters import (
    accompanying_report,
    change_responsibility,
    delivery,
    request,
    status_notification,
    submit,
)
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

    def get_xml(self, data):  # pragma: no cover
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
        data = self.get_data()
        xml = self.get_xml(data)
        return self.create_message(xml)


class SubmitEventHandler(BaseEventHandler):
    event_type = "submit"

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                url=f"{settings.INTERNAL_BASE_URL}/form/edit-page/instance-resource-id/20014/instance-id/{self.instance.pk}",
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, data, self.event_type
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

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
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


class WithdrawPlanningPermissionApplicationEventHandler(SubmitEventHandler):
    event_type = "withdraw planning permission application"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventRequest=request(self.instance, self.event_type),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class AccompanyingReportEventHandler(BaseEventHandler):
    event_type = "accompanying report"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        attachments = self.instance.attachments.filter(attachment_sections__pk=7)
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventAccompanyingReport=accompanying_report(
                    self.instance, self.event_type, attachments
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class ChangeResponsibilityEventHandler(BaseEventHandler):
    event_type = "change responsibility"

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventChangeResponsibility=change_responsibility(self.instance),
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
