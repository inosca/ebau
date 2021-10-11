import logging
from functools import wraps
from uuid import uuid4

from caluma.caluma_workflow.models import Case
from django.conf import settings
from django.dispatch import receiver
from django.utils import timezone
from pyxb import (
    IncompleteElementContentError,
    UnprocessedElementContentError,
    UnprocessedKeywordContentError,
)

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_BEILAGEN_GESUCH,
    ATTACHMENT_SECTION_BEILAGEN_SB1,
    ATTACHMENT_SECTION_BEILAGEN_SB2,
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
    ECH_ACCOMPANYING_REPORT,
    ECH_CHANGE_RESPONSIBILITY,
    ECH_CLAIM,
    ECH_FILE_SUBSEQUENTLY,
    ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN,
    ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN,
    ECH_STATUS_NOTIFICATION_IN_KOORDINATION,
    ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND,
    ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET,
    ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN,
    ECH_SUBMIT,
    ECH_TASK_SB1_SUBMITTED,
    ECH_TASK_SB2_SUBMITTED,
    ECH_TASK_STELLUNGNAHME,
    ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION,
    NOTICE_TYPE_NEBENBESTIMMUNG,
    NOTICE_TYPE_STELLUNGNAHME,
)
from camac.core.models import Activation, Notice
from camac.document.models import Attachment
from camac.user.models import Service

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
from .signals import (
    accompanying_report_send,
    assigned_ebau_number,
    change_responsibility as change_responsibility_signal,
    circulation_ended,
    circulation_started,
    file_subsequently,
    finished,
    instance_submitted,
    ruling,
    sb1_submitted,
    sb2_submitted,
    task_send,
)
from .utils import handle_string_values

logger = logging.getLogger(__name__)


class EventHandlerException(BaseException):
    pass


class BaseEventHandler:
    def __init__(self, instance, user_pk=None, group_pk=None, context=None):
        self.instance = instance
        self.user_pk = user_pk
        self.group_pk = group_pk
        self.context = context

        self.message_date = timezone.now()
        self.message_id = uuid4()

    def get_data(self):
        return get_document(self.instance.pk)

    def get_xml(self, data, **kwargs):  # pragma: no cover
        raise NotImplementedError()

    def create_message(self, xml, receiver=None):
        receiver = receiver if receiver else self.instance.responsible_service()

        if not receiver:
            # Due to possible misconfiguration of the instance, the
            # fallback to active_service might not work (and return
            # None). This needs to be caught
            logger.error(
                f"Instance {self.instance.pk} has no active_service and no "
                "receiver given. Cannot store eCH message! eCH Message content: "
                f"{xml}"
            )
            return

        message = Message.objects.create(
            body=xml,
            receiver=receiver,
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
    uri_instance_resource_id = 20014
    message_type = ECH_SUBMIT

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_type=self.message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
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


class FileSubsequentlyEventHandler(BaseEventHandler):
    event_type = "file subsequently"
    uri_instance_resource_id = 150000
    message_type = ECH_FILE_SUBSEQUENTLY

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_type=self.message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
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


class StatusNotificationEventHandler(BaseEventHandler):
    def get_data(self):
        return {"ech-subject": "status notification"}

    def get_message_type(self):
        message_type = "unkown"  # this should never be used

        if self.instance.instance_state.name == "circulation_init":
            message_type = ECH_STATUS_NOTIFICATION_EBAU_NR_VERGEBEN
        elif self.instance.instance_state.name == "circulation":
            message_type = ECH_STATUS_NOTIFICATION_ZIRKULATION_GESTARTET
        elif self.instance.instance_state.name == "sb1":
            message_type = ECH_STATUS_NOTIFICATION_SB1_AUSSTEHEND
        elif self.instance.instance_state.name == "evaluated":
            message_type = ECH_STATUS_NOTIFICATION_ABGESCHLOSSEN
        elif self.instance.instance_state.name == "rejected":  # pragma: no cover
            message_type = ECH_STATUS_NOTIFICATION_ZURUECKGEWIESEN
        elif self.instance.instance_state.name == "coordination":
            message_type = ECH_STATUS_NOTIFICATION_IN_KOORDINATION

        return message_type

    def get_xml(self, data, message_type):
        try:
            return delivery(
                self.instance,
                data,
                message_type=message_type,
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

    def run(self):
        data = self.get_data()
        xml = self.get_xml(data, self.get_message_type())
        return self.create_message(xml)


class WithdrawPlanningPermissionApplicationEventHandler(BaseEventHandler):
    event_type = "withdraw planning permission application"
    message_type = ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_type=self.message_type,
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


class TaskEventHandler(BaseEventHandler):
    event_type = "task"
    task_map = {
        "circulation": {
            "message_type": ECH_TASK_STELLUNGNAHME,
            "comment": "Anforderung einer Stellungnahme",
            "attachment_section": ATTACHMENT_SECTION_BEILAGEN_GESUCH,
        },
        "sb2": {
            "message_type": ECH_TASK_SB1_SUBMITTED,
            "comment": "SB1 eingereicht",
            "attachment_section": ATTACHMENT_SECTION_BEILAGEN_SB1,
        },
        "conclusion": {
            "message_type": ECH_TASK_SB2_SUBMITTED,
            "comment": "SB2 eingereicht",
            "attachment_section": ATTACHMENT_SECTION_BEILAGEN_SB2,
        },
    }

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data, message_type, comment, deadline=None, attachments=None):
        try:
            return delivery(
                self.instance,
                data,
                message_type=message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventRequest=request(
                    self.instance,
                    self.event_type,
                    comment=comment,
                    deadline=deadline,
                    attachments=attachments,
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise

    def _handle_activations(self, context, data, attachments):
        msgs = []
        for activation in Activation.objects.filter(
            circulation__instance=self.instance, ech_msg_created=False
        ):
            self.message_id = uuid4()
            xml = self.get_xml(
                data,
                message_type=context["message_type"],
                comment=context["comment"],
                deadline=activation.deadline_date,
                attachments=attachments,
            )
            msgs.append(self.create_message(xml, activation.service))
            activation.ech_msg_created = True
            activation.save()

        return msgs

    def run(self):
        data = self.get_data()
        context = self.task_map[self.instance.instance_state.name]

        attachments = Attachment.objects.filter(
            instance=self.instance,
            attachment_sections__pk=context["attachment_section"],
        )

        if self.instance.instance_state.name == "circulation":
            return self._handle_activations(context, data, attachments)

        xml = self.get_xml(
            data,
            message_type=context["message_type"],
            comment=context["comment"],
            attachments=attachments,
        )
        msg = self.create_message(xml)
        return [msg]


class ClaimEventHandler(WithdrawPlanningPermissionApplicationEventHandler):
    event_type = "claim"
    message_type = ECH_CLAIM

    def get_data(self):
        return {"ech-subject": self.event_type}


class AccompanyingReportEventHandler(BaseEventHandler):
    event_type = "accompanying report"
    message_type = ECH_ACCOMPANYING_REPORT

    def __init__(self, instance, user_pk=None, group_pk=None, context=None):
        super().__init__(instance, user_pk, group_pk, context)
        self.activation = self._get_activation()

    def get_data(self):
        return {"ech-subject": self.event_type}

    def _get_activation(self):
        return Activation.objects.get(pk=self.context["activation-id"])

    def _get_notices(self):
        def prepare(notice):
            if notice:
                return handle_string_values(notice.content)
            return notice

        stellungnahme = prepare(
            Notice.objects.filter(
                activation=self.activation, notice_type__pk=NOTICE_TYPE_STELLUNGNAHME
            ).first()
        )
        nebenbestimmung = prepare(
            Notice.objects.filter(
                activation=self.activation, notice_type__pk=NOTICE_TYPE_NEBENBESTIMMUNG
            ).first()
        )

        return stellungnahme, nebenbestimmung

    def get_xml(self, data, attachments, stellungnahme, nebenbestimmung):
        attachments = (
            attachments
            if attachments
            else self.instance.attachments.filter(
                attachment_sections__pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
                group__service__in=[
                    self.activation.service,
                    *Service.objects.filter(service_parent=self.activation.service),
                ],
            )
        )
        try:
            return delivery(
                self.instance,
                data,
                message_type=self.message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventAccompanyingReport=accompanying_report(
                    self.instance,
                    self.event_type,
                    attachments,
                    self.activation.circulation_answer,
                    stellungnahme,
                    nebenbestimmung,
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise

    def run(self, attachments=None):
        data = self.get_data()
        xml = self.get_xml(data, attachments, *self._get_notices())
        return self.create_message(xml)


class ChangeResponsibilityEventHandler(BaseEventHandler):
    event_type = "change responsibility"
    message_type = ECH_CHANGE_RESPONSIBILITY

    def get_data(self):
        return {"ech-subject": self.event_type}

    def get_xml(self, data):
        try:
            return delivery(
                self.instance,
                data,
                message_type=self.message_type,
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


def if_ech_enabled(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        instance = kwargs.get("instance")
        instance_ignored = (
            Case.objects.filter(
                instance__pk=instance.pk,
                document__form__in=settings.ECH_EXCLUDED_FORMS,
            ).exists()
            if instance
            else False
        )

        if settings.APPLICATION.get("ECH_API") and not instance_ignored:
            return func(*args, **kwargs)

    return wrapper


@receiver(instance_submitted)
@if_ech_enabled
def submit_callback(sender, instance, user_pk, group_pk, **kwargs):
    handler = SubmitEventHandler(instance, user_pk=user_pk, group_pk=group_pk)
    handler.run()


@receiver(assigned_ebau_number)
@receiver(circulation_started)
@receiver(circulation_ended)
@receiver(ruling)
@receiver(finished)
@if_ech_enabled
def send_status_notification(sender, instance, user_pk, group_pk, **kwargs):
    handler = StatusNotificationEventHandler(
        instance, user_pk=user_pk, group_pk=group_pk
    )
    handler.run()


@receiver(task_send)
@receiver(sb1_submitted)
@receiver(sb2_submitted)
@if_ech_enabled
def task_callback(sender, instance, user_pk, group_pk, **kwargs):
    handler = TaskEventHandler(instance, user_pk=user_pk, group_pk=group_pk)
    handler.run()


@receiver(accompanying_report_send)
@if_ech_enabled
def accompanying_report_callback(
    sender, instance, user_pk, group_pk, context, attachments, **kwargs
):
    handler = AccompanyingReportEventHandler(
        instance, user_pk=user_pk, group_pk=group_pk, context=context
    )
    handler.run(attachments)


@receiver(file_subsequently)
@if_ech_enabled
def file_subsequently_callback(sender, instance, user_pk, group_pk, **kwargs):
    handler = FileSubsequentlyEventHandler(instance, user_pk=user_pk, group_pk=group_pk)
    handler.run()


@receiver(change_responsibility_signal)
@if_ech_enabled
def change_responsibility_callback(sender, instance, user_pk, group_pk, **kwargs):
    handler = ChangeResponsibilityEventHandler(
        instance, user_pk=user_pk, group_pk=group_pk
    )
    handler.run()
