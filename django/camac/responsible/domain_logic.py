from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.core.utils import canton_aware
from camac.notification.utils import send_mail_without_request
from camac.responsible.models import ResponsibleService
from camac.user.models import Group, User


class ResponsibleServiceDomainLogic:
    @classmethod
    def update_responsibility(
        cls,
        responsible_service: ResponsibleService,
        user: User,
        group: Group,
        old_user: User | None = None,
    ):
        """
        Perform the necessary steps after creating/updating ResponsibleService.

        All READY workitems in the related instance need to be updated
        and new responsible user of the instance can be notified.
        """
        cls.update_work_item_assigned_user(responsible_service, old_user)
        cls.send_notification(responsible_service, user, group)

    @classmethod
    @canton_aware
    def update_work_item_assigned_user(
        cls, responsible_service: ResponsibleService, old_user: User | None = None
    ):
        """Set assigned_users of all READY work items in the instance to the responsible_service user."""
        WorkItem.objects.filter(
            case__family__instance__pk=responsible_service.instance_id,
            addressed_groups=[responsible_service.service.pk],
            status=WorkItem.STATUS_READY,
        ).update(assigned_users=[responsible_service.responsible_user.username])

    @classmethod
    def update_work_item_assigned_user_ag(
        cls, responsible_service: ResponsibleService, old_user: User | None = None
    ):
        """Reassign ready work items when changing the responsible user.

        Kt. AG uses a different logic for this functionality than the rest of
        the cantons. Only work items that are assigned to the previously
        responsible user will be reassigned. If there's no responsible user yet,
        only unassigned work items will be assigned to the responsible user.
        """

        work_items = WorkItem.objects.filter(
            case__family__instance__pk=responsible_service.instance_id,
            addressed_groups=[responsible_service.service.pk],
            status=WorkItem.STATUS_READY,
        )

        if old_user:
            # If the responsible user changed, we only reassign the work items
            # that were assigned to the previous user to the new user.
            work_items = work_items.filter(assigned_users=[old_user.username])
        else:
            # If the responsiblity was only added, we only assign the work items
            # that are not assigned to anyone to the newly responsible user.
            # Unassigned work items that come from a template that bypasses the
            # responsible user assignment are explicitly excluded.
            work_items = work_items.filter(assigned_users=[]).exclude(
                **{
                    "meta__bypass-responsible-user": True,
                    "meta__bypass-responsible-user__isnull": False,
                }
            )

        work_items.update(
            assigned_users=[responsible_service.responsible_user.username]
        )

    @classmethod
    def send_notification(cls, responsible_service: ResponsibleService, user, group):
        """Send a notification to the new responsible user of the instance."""
        if responsible_service.responsible_user.id == user.id:
            return
        config = settings.APPLICATION["NOTIFICATIONS"].get("CHANGE_RESPONSIBLE_USER")

        if config:
            send_mail_without_request(
                config["template_slug"],
                user,
                group,
                recipient_types=["email_list"],
                email_list=responsible_service.responsible_user.email,
                instance={"type": "instances", "id": responsible_service.instance.pk},
            )
