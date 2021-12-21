import reversion
from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.db.models import Q
from django.utils.translation import gettext_noop

from camac.constants.kt_bern import (
    DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
    DECISIONS_ABGELEHNT,
    DECISIONS_BEWILLIGT,
)
from camac.core.models import DocxDecision
from camac.core.utils import create_history_entry
from camac.echbern.signals import ruling
from camac.instance.models import InstanceState
from camac.instance.utils import set_construction_control
from camac.notification.utils import send_mail_without_request
from camac.stats.cycle_time import compute_cycle_time
from camac.user.models import User

from .general import get_caluma_setting, get_instance


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def set_cycle_time_post_decision_complete(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("DECISION_TASK"):
        instance = get_instance(work_item)
        instance.case.meta.update(compute_cycle_time(instance))
        instance.case.save()


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_decision(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("DECISION_TASK"):
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)

        workflow = work_item.case.workflow_id
        history_text = gettext_noop("Evaluation completed")
        instance_state_name = "finished"

        if workflow == "building-permit":
            approved = (
                DocxDecision.objects.filter(instance=instance)
                .filter(
                    Q(decision=DECISIONS_BEWILLIGT)
                    | Q(
                        decision=DECISIONS_ABGELEHNT,
                        decision_type=DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
                    ),
                )
                .exists()
            )
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
            group_pk=user.camac_group,
        )

        if not context or not context.get("no-notification"):
            notification_config = settings.APPLICATION["NOTIFICATIONS"].get(
                "DECISION_PRELIMINARY_CLARIFICATION"
                if workflow == "preliminary-clarification"
                else "DECISION",
                [],
            )

            # send notifications to applicant, municipality and all involved services
            for config in notification_config:
                send_mail_without_request(
                    config["template_slug"],
                    user.username,
                    user.camac_group,
                    instance={"id": instance.pk, "type": "instances"},
                    recipient_types=config["recipient_types"],
                )

        # create history entry
        if not context or not context.get("no-history"):
            create_history_entry(instance, camac_user, history_text)
