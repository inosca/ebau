import reversion
from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_complete_work_item
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
        instance_state_name = "done"

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

        elif workflow == "building-police-procedure":
            instance_state_name = "done_internal"

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
