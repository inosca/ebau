import reversion
from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.constants.kt_bern import DECISIONS_BEWILLIGT
from camac.core.models import DocxDecision
from camac.core.utils import create_history_entry
from camac.echbern.signals import ruling
from camac.instance.models import InstanceState
from camac.instance.utils import set_construction_control
from camac.notification.serializers import (
    PermissionlessNotificationTemplateSendmailSerializer,
)
from camac.notification.views import send_mail
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_complete_work_item)
@transaction.atomic
def post_complete_decision(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("DECISION_TASK"):
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)

        workflow = work_item.case.workflow_id
        history_text = gettext_noop("Evaluation completed")
        instance_state_name = "finished"

        if workflow == "building-permit":
            approved = DocxDecision.objects.filter(
                instance=instance.pk,
                decision=DECISIONS_BEWILLIGT,
            ).exists()
            history_text = gettext_noop("Decision decreed")

            if approved:
                # set the construction control as responsible service
                set_construction_control(instance)
                instance_state_name = "sb1"

        elif workflow == "preliminary-clarification":
            instance_state_name = "evaluated"

        elif workflow == "internal":
            instance_state_name = "finished_internal"
            ebau_work_item = work_item.case.work_items.filter(
                task_id=get_caluma_setting("EBAU_NUMBER_TASK"),
                status=WorkItem.STATUS_READY,
            ).first()
            if ebau_work_item:
                # this could also be done in the PRE_COMPLETE config but it's
                # way too risky since it could break the workflow of currently
                # broken instances in production and should only happen for
                # internal instances that do not require an ebau number.
                skip_work_item(ebau_work_item, user, context)

        # go to next instance state
        with reversion.create_revision():
            reversion.set_user(camac_user)

            instance.previous_instance_state = instance.instance_state
            instance.instance_state = InstanceState.objects.get(
                name=instance_state_name
            )
            instance.save()

        # trigger ech message for status change
        ruling.send(
            sender="post_complete_decision",
            instance=instance,
            user_pk=camac_user.pk,
            group_pk=context.get("group-id"),
        )

        # send notifications to applicant, municipality and all involved services
        for config in settings.APPLICATION["NOTIFICATIONS"]["DECISION"]:
            send_mail(
                config["template_slug"],
                context={},
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=config["recipient_types"],
                serializer=PermissionlessNotificationTemplateSendmailSerializer,
            )

        # create history entry
        create_history_entry(instance, camac_user, history_text)
