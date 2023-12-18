from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_user.models import OIDCUser
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction

from camac.core.utils import create_history_entry
from camac.instance.models import Instance
from camac.notification.utils import send_mail_without_request
from camac.user.models import Group, User
from camac.user.permissions import get_role_name


class WithdrawalLogic:
    @classmethod
    def has_permission(
        cls,
        instance: Instance,
        camac_user: User,
        camac_group: Group,
    ) -> bool:
        if not settings.WITHDRAWAL:
            return False

        return (
            instance.instance_state.name
            in settings.WITHDRAWAL["ALLOWED_INSTANCE_STATES"]
            and get_role_name(camac_group) == "applicant"
            and instance.involved_applicants.filter(invitee=camac_user).exists()
        )

    @classmethod
    @transaction.atomic
    def withdraw_instance(
        cls,
        instance: Instance,
        camac_user: User,
        camac_group: Group,
        caluma_user: OIDCUser,
    ) -> Instance:
        # process work items
        for task_id, action in settings.WITHDRAWAL["PROCESS_WORK_ITEMS"]:
            for work_item in WorkItem.objects.filter(
                task_id=task_id,
                status=WorkItem.STATUS_READY,
                case__family__instance=instance,
            ):
                getattr(workflow_api, f"{action}_work_item")(work_item, caluma_user)

        # pre-fill decision answer
        save_answer(
            document=instance.case.work_items.get(
                task_id=settings.DECISION["TASK"], status=WorkItem.STATUS_READY
            ).document,
            question=Question.objects.get(
                pk=settings.DECISION["QUESTIONS"]["DECISION"]
            ),
            value=settings.DECISION["ANSWERS"]["DECISION"]["WITHDRAWAL"],
            user=caluma_user,
        )

        # set instance state
        instance.set_instance_state(settings.WITHDRAWAL["INSTANCE_STATE"], camac_user)

        # history entry
        create_history_entry(
            instance,
            camac_user,
            settings.WITHDRAWAL["HISTORY_ENTRIES"]["REQUESTED"],
        )

        # send notifications
        for notification in settings.WITHDRAWAL["NOTIFICATIONS"]:
            send_mail_without_request(
                notification["template_slug"],
                camac_user.username,
                camac_group.pk,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=notification["recipient_types"],
            )

        return instance
