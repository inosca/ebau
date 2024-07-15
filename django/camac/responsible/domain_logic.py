from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.notification.utils import send_mail
from camac.responsible.models import ResponsibleService


class ResponsibleServiceDomainLogic:
    @classmethod
    def update_responsibility(
        cls, responsible_service: ResponsibleService, serializer_context: dict
    ):
        """
        Perform the necessary steps after creating/updating ResponsibleService.

        All READY workitems in the related instance need to be updated
        and new responsible user of the instance can be notified.
        """
        cls.update_work_item_assigned_user(responsible_service)
        cls.send_notification(responsible_service, serializer_context)

    @staticmethod
    def update_work_item_assigned_user(responsible_service: ResponsibleService):
        """Set assigned_users of all READY work items in the instance to the responsible_service user."""
        WorkItem.objects.filter(
            case__family__instance__pk=responsible_service.instance_id,
            addressed_groups=[responsible_service.service.pk],
            status=WorkItem.STATUS_READY,
        ).update(assigned_users=[responsible_service.responsible_user.username])

    @staticmethod
    def send_notification(
        responsible_service: ResponsibleService, serializer_context: dict
    ):
        """Send a notification to the new responsible user of the instance."""
        config = settings.APPLICATION["NOTIFICATIONS"].get("CHANGE_RESPONSIBLE_USER")

        if config:
            send_mail(
                config["template_slug"],
                serializer_context,
                recipient_types=["email_list"],
                email_list=responsible_service.responsible_user.email,
                instance={"type": "instances", "id": responsible_service.instance.pk},
            )
