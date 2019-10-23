import logging

from django.conf import settings
from django.dispatch import receiver
from pyxb import (
    IncompleteElementContentError,
    UnprocessedElementContentError,
    UnprocessedKeywordContentError,
)

from camac.caluma import get_admin_token

from .data_preparation import get_document
from .formatters import delivery, submit
from .models import Message
from .signals import instance_submitted

logger = logging.getLogger(__name__)


class BaseEventHandler:
    def __init__(self, instance, group_pk):
        self.instance = instance
        self.group_pk = group_pk

    def get_data(self):
        auth_header = get_admin_token()
        return get_document(self.instance.pk, auth_header, self.group_pk)

    def get_xml(self, caluma_data):  # pragma: no cover
        raise NotImplementedError()

    def create_message(self, xml):
        message = Message.objects.create(
            body=xml, receiver=self.instance.active_service
        )
        return message

    def run(self):
        caluma_data = self.get_data()
        xml = self.get_xml(caluma_data)
        return self.create_message(xml)


class SubmitEventHandler(BaseEventHandler):
    def get_xml(self, caluma_data):
        try:
            return delivery(
                self.instance,
                caluma_data,
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, caluma_data
                ),
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
