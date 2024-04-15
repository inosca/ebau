from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.core.utils import create_history_entry
from camac.ech0211.signals import ruling
from camac.instance import domain_logic
from camac.notification.utils import send_mail_without_request
from camac.permissions import events as permissions_events
from camac.permissions.config.kt_gr import gr_include_gvg
from camac.stats.cycle_time import compute_cycle_time
from camac.user.models import User

from .general import get_caluma_setting, get_instance


def get_notification_config(instance):
    if instance.case.workflow_id == "preliminary-clarification":
        return settings.APPLICATION["NOTIFICATIONS"].get(
            "DECISION_PRELIMINARY_CLARIFICATION", []
        )
    elif instance.case.meta.get("is-appeal") and settings.APPEAL:
        return settings.APPEAL["NOTIFICATIONS"].get("APPEAL_DECISION", [])
    # TODO(GR): replace by preliminary clarification workflow
    elif instance.case.document.form.slug in [
        "bauanzeige",
        "vorlaeufige-beurteilung",
    ]:  # pragma: no cover
        return settings.APPLICATION["NOTIFICATIONS"].get(
            "NON_BUILDING_PERMIT_DECISION", []
        )

    return settings.APPLICATION["NOTIFICATIONS"].get("DECISION", [])


def send_notifications(instance, context, user):
    notification_config = get_notification_config(instance)

    if not gr_include_gvg(instance):
        notification_config = [
            config
            for config in notification_config
            if config["recipient_types"] != ["gvg"]
        ]

    if not context or not context.get("no-notification"):
        for config in notification_config:
            send_mail_without_request(
                config["template_slug"],
                user.username,
                user.camac_group,
                instance={"id": instance.pk, "type": "instances"},
                recipient_types=config["recipient_types"],
            )


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
@filter_events(lambda work_item: work_item.task.slug == settings.DECISION.get("TASK"))
def set_workflow_answer(sender, work_item, user, context, **kwargs):
    decision_workflow_question = Question.objects.filter(pk="decision-workflow")

    if decision_workflow_question:
        save_answer(
            document=work_item.document,
            question=decision_workflow_question[0],
            value=work_item.case.workflow_id,
            user=user,
        )


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(lambda work_item: work_item.task.slug == settings.DECISION.get("TASK"))
def set_cycle_time_post_decision_complete(sender, work_item, user, context, **kwargs):
    if settings.DECISION.get("ENABLE_STATS"):
        instance = get_instance(work_item)
        instance.case.meta.update(compute_cycle_time(instance))
        instance.case.save()


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(lambda work_item: work_item.task.slug == settings.DECISION.get("TASK"))
def post_complete_decision(sender, work_item, user, context, **kwargs):
    instance = get_instance(work_item)
    camac_user = User.objects.get(username=user.username)
    workflow = work_item.case.workflow_id

    if workflow == "building-permit":
        domain_logic.DecisionLogic.post_complete_decision_building_permit(
            instance, work_item, user, camac_user
        )

    elif workflow == "preliminary-clarification":
        instance.set_instance_state("evaluated", camac_user)

    elif workflow == "internal":
        instance.set_instance_state("finished_internal", camac_user)
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
    else:
        instance.set_instance_state("finished", camac_user)

    permissions_events.Trigger.decision_decreed(None, instance)

    # trigger ech message for status change
    ruling.send(
        sender="post_complete_decision",
        instance=instance,
        user_pk=camac_user.pk,
        group_pk=user.camac_group,
    )
    send_notifications(instance, context, user)

    history_text = gettext_noop("Evaluation completed")
    if (
        settings.WITHDRAWAL
        and instance.instance_state.name
        == settings.WITHDRAWAL["INSTANCE_STATE_CONFIRMED"]
    ):
        history_text = settings.WITHDRAWAL["HISTORY_ENTRIES"]["CONFIRMED"]
    elif workflow == "building-permit":
        history_text = gettext_noop("Decision decreed")

    # create history entry
    if not context or not context.get("no-history"):
        create_history_entry(instance, camac_user, history_text)
