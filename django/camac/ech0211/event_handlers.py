import logging
from functools import wraps
from uuid import uuid4

from alexandria.core.models import Document
from django.conf import settings
from django.db.models import Q
from django.dispatch import receiver
from django.utils import timezone
from pyxb import (
    IncompleteElementContentError,
    UnprocessedElementContentError,
    UnprocessedKeywordContentError,
)

from camac.constants.kt_bern import (
    ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
    ECH_ACCOMPANYING_REPORT,
    ECH_CHANGE_RESPONSIBILITY,
    ECH_CLAIM,
    ECH_FILE_SUBSEQUENTLY,
    ECH_SUBMIT,
    ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION,
)
from camac.document.models import Attachment
from camac.user.models import Service

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
    exam_completed,
    file_subsequently,
    finished,
    instance_submitted,
    rejected,
    rejection_reverted,
    ruling,
    sb1_submitted,
    sb2_submitted,
    task_send,
)

logger = logging.getLogger(__name__)


class EventHandlerException(BaseException):
    pass


class BaseEventHandler:
    def __init__(self, instance, user_pk=None, group_pk=None):
        self.instance = instance
        self.user_pk = user_pk
        self.group_pk = group_pk

        self.message_date = timezone.now()
        self.message_id = uuid4()
        self.message_receiver = self.instance.responsible_service()

    def get_xml(self, **kwargs):  # pragma: no cover
        raise NotImplementedError()

    def create_message(self, xml):
        if not self.message_receiver:
            # Due to possible misconfiguration of the instance, the
            # fallback to active_service might not work (and return
            # None). This needs to be caught
            logger.error(
                f"Instance {self.instance.pk} has no active_service and no "
                "receiver given. Cannot store eCH message! eCH Message content: "
                f"{xml}"
            )
            return

        return Message.objects.create(
            body=xml,
            receiver=self.message_receiver,
            created_at=self.message_date,
            id=self.message_id,
        )

    def run(self):
        xml = self.get_xml()
        return self.create_message(xml)


class SubmitEventHandler(BaseEventHandler):
    event_type = "submit"
    message_type = ECH_SUBMIT

    def get_xml(self):
        try:
            return delivery(
                self.instance,
                subject=self.event_type,
                message_type=self.message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, self.event_type
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise

    def run(self):
        return self.create_message(self.get_xml())


class FileSubsequentlyEventHandler(BaseEventHandler):
    event_type = "file subsequently"
    message_type = ECH_FILE_SUBSEQUENTLY

    def get_xml(self):
        try:
            return delivery(
                self.instance,
                subject=self.event_type,
                message_type=self.message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventSubmitPlanningPermissionApplication=submit(
                    self.instance, self.event_type
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
    event_type = "status notification"

    def get_message_type(self):
        for rule in settings.ECH0211.get("STATUS_NOTIFICATION_TYPES", []):
            if new_state := rule.get("new_state"):
                new_states = new_state if isinstance(new_state, list) else [new_state]
                if self.instance.instance_state.name in new_states:
                    return rule["type"]
            if prev_state := rule.get("prev_state"):
                prev_states = (
                    prev_state if isinstance(prev_state, list) else [prev_state]
                )
                if self.instance.previous_instance_state.name in prev_states:
                    return rule["type"]

        raise RuntimeError(
            f'Unknown `message_type` for instance {self.instance.pk} changing status from "{self.instance.previous_instance_state.name}" to "{self.instance.instance_state.name}"'
        )  # pragma: no cover

    def get_xml(self, message_type):
        try:
            return delivery(
                self.instance,
                subject=self.event_type,
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
        xml = self.get_xml(self.get_message_type())
        return self.create_message(xml)


class WithdrawPlanningPermissionApplicationEventHandler(BaseEventHandler):
    event_type = "withdraw planning permission application"
    message_type = ECH_WITHDRAW_PLANNING_PERMISSION_APPLICATION

    def get_xml(self):
        try:
            return delivery(
                self.instance,
                subject=self.event_type,
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

    def __init__(self, instance, user_pk=None, group_pk=None, inquiry=None):
        super().__init__(instance, user_pk, group_pk)

        self.inquiry = inquiry

        if inquiry:
            self.message_receiver = Service.objects.get(pk=inquiry.addressed_groups[0])

    def get_xml(self):
        config = settings.ECH0211["TASK_MAP"][
            "circulation" if self.inquiry else self.instance.instance_state.name
        ]

        if settings.APPLICATION.get("DOCUMENT_BACKEND") == "camac-ng":
            documents = Attachment.objects.filter(
                instance=self.instance,
                attachment_sections__pk=config["attachment_section"],
            )
        else:
            documents = Document.objects.filter(
                instance_document__instance=self.instance, category=config["category"]
            )

        try:
            return delivery(
                self.instance,
                subject=self.event_type,
                message_type=config["message_type"],
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventRequest=request(
                    self.instance,
                    self.event_type,
                    comment=str(config["comment"]),
                    deadline=self.inquiry.deadline if self.inquiry else None,
                    documents=documents,
                ),
            ).toxml()
        except (
            IncompleteElementContentError,
            UnprocessedElementContentError,
            UnprocessedKeywordContentError,
        ) as e:  # pragma: no cover
            logger.error(e.details())
            raise


class ClaimEventHandler(WithdrawPlanningPermissionApplicationEventHandler):
    event_type = "claim"
    message_type = ECH_CLAIM


class AccompanyingReportEventHandler(BaseEventHandler):
    event_type = "accompanying report"
    message_type = ECH_ACCOMPANYING_REPORT

    def __init__(
        self, instance, inquiry, user_pk=None, group_pk=None, attachments=None
    ):
        super().__init__(instance, user_pk, group_pk)

        self.inquiry = inquiry
        if not attachments:
            self.attachments = self.instance.attachments.filter(
                attachment_sections__pk=ATTACHMENT_SECTION_BETEILIGTE_BEHOERDEN,
                group__service__in=Service.objects.filter(
                    Q(pk=self.inquiry.addressed_groups[0])
                    | Q(service_parent_id=self.inquiry.addressed_groups[0])
                ),
            )
        else:
            self.attachments = attachments

    def get_xml(self):
        try:
            return delivery(
                self.instance,
                subject=self.event_type,
                message_type=self.message_type,
                message_date=self.message_date,
                message_id=str(self.message_id),
                eventAccompanyingReport=accompanying_report(
                    self.instance,
                    self.event_type,
                    self.attachments,
                    self.inquiry,
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
    message_type = ECH_CHANGE_RESPONSIBILITY

    def get_xml(self):
        try:
            return delivery(
                self.instance,
                subject=self.event_type,
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


def if_ech_enabled(api_level="basic"):
    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            instance = kwargs.get("instance")
            if (
                settings.ECH0211
                and (api_level != "full" or settings.ECH0211.get("API_LEVEL") == "full")
                and instance.case.workflow_id not in settings.ECH_EXCLUDED_WORKFLOWS
                and instance.case.document.form_id not in settings.ECH_EXCLUDED_FORMS
            ):
                return func(*args, **kwargs)

        return wrapper

    return decorate


@receiver(instance_submitted)
@if_ech_enabled()
def submit_callback(sender, instance, user_pk, group_pk, **kwargs):
    SubmitEventHandler(instance, user_pk=user_pk, group_pk=group_pk).run()


@receiver(assigned_ebau_number)
@receiver(circulation_started)
@receiver(circulation_ended)
@receiver(exam_completed)
@receiver(ruling)
@receiver(finished)
@receiver(rejected)
@receiver(rejection_reverted)
@if_ech_enabled(api_level="full")
def send_status_notification(sender, instance, user_pk, group_pk, **kwargs):
    handler = StatusNotificationEventHandler(
        instance, user_pk=user_pk, group_pk=group_pk
    )
    handler.run()


@receiver(task_send)
@receiver(sb1_submitted)
@receiver(sb2_submitted)
@if_ech_enabled(api_level="full")
def task_callback(sender, instance, user_pk, group_pk, inquiry=None, **kwargs):
    handler = TaskEventHandler(
        instance,
        user_pk=user_pk,
        group_pk=group_pk,
        inquiry=inquiry,
    )
    handler.run()


@receiver(accompanying_report_send)
@if_ech_enabled(api_level="full")
def accompanying_report_callback(
    sender, instance, user_pk, group_pk, inquiry, attachments, **kwargs
):
    handler = AccompanyingReportEventHandler(
        instance,
        user_pk=user_pk,
        group_pk=group_pk,
        inquiry=inquiry,
        attachments=attachments,
    )
    handler.run()


@receiver(file_subsequently)
@if_ech_enabled(api_level="full")
def file_subsequently_callback(sender, instance, user_pk, group_pk, **kwargs):
    handler = FileSubsequentlyEventHandler(instance, user_pk=user_pk, group_pk=group_pk)
    handler.run()


@receiver(change_responsibility_signal)
@if_ech_enabled(api_level="full")
def change_responsibility_callback(sender, instance, user_pk, group_pk, **kwargs):
    handler = ChangeResponsibilityEventHandler(
        instance, user_pk=user_pk, group_pk=group_pk
    )
    handler.run()
