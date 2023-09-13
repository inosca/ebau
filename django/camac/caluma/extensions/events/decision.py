from datetime import timedelta

from caluma.caluma_core.events import on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_noop

from camac.core.utils import create_history_entry
from camac.ech0211.signals import ruling
from camac.instance import domain_logic
from camac.instance.utils import (
    copy_instance,
    fill_ebau_number,
    get_lead_authority,
    set_construction_control,
)
from camac.notification.utils import send_mail_without_request
from camac.stats.cycle_time import compute_cycle_time
from camac.user.models import Group, Service, User

from .general import get_caluma_setting, get_instance


def get_notification_config(instance):
    if instance.case.workflow_id == "preliminary-clarification":
        return settings.APPLICATION["NOTIFICATIONS"].get(
            "DECISION_PRELIMINARY_CLARIFICATION", []
        )
    elif instance.case.meta.get("is-appeal") and settings.APPEAL:
        return settings.APPEAL["NOTIFICATIONS"].get("APPEAL_DECISION", [])

    return settings.APPLICATION["NOTIFICATIONS"].get("DECISION", [])


def copy_municipality_tags(instance, construction_control):
    municipality_tags = instance.tags.filter(
        service=Service.objects.filter(
            service_group__name="municipality",
            trans__language="de",
            trans__name=construction_control.trans.get(language="de").name.replace(
                "Baukontrolle", "Leitbehörde"
            ),
        ).first()
    )

    for tag in municipality_tags:
        instance.tags.create(service=construction_control, name=tag.name)


def handle_appeal_decision(instance, work_item, user, camac_user):
    if not settings.APPEAL or not instance.case.meta.get("is-appeal"):
        return

    if work_item.document.answers.filter(
        question_id=settings.APPEAL["QUESTIONS"]["DECISION"],
        value=settings.APPEAL["ANSWERS"]["DECISION"]["REJECTED"],
    ).exists():
        new_instance = copy_instance(
            instance=instance,
            group=Group.objects.get(pk=user.camac_group),
            user=camac_user,
            caluma_user=user,
            skip_submit=True,
            # Mark the new instance as result of a rejected appeal so the
            # frontend can find it in the copies of the previous instance to
            # redirect after the decision was submitted.
            new_meta={"is-rejected-appeal": True},
        )

        fill_ebau_number(
            instance=new_instance,
            ebau_number=instance.case.meta.get("ebau-number"),
            caluma_user=user,
        )


def copy_responsible_person_lead_authority(instance, construction_control):
    lead_authority = get_lead_authority(construction_control)

    responsible_service = instance.responsible_services.filter(
        service=lead_authority
    ).first()

    if lead_authority.responsibility_construction_control and responsible_service:
        instance.responsible_services.create(
            service=construction_control,
            responsible_user=responsible_service.responsible_user,
        )


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_workflow_answer(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("DECISION_TASK"):
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
def set_cycle_time_post_decision_complete(sender, work_item, user, context, **kwargs):
    if work_item.task_id == get_caluma_setting("DECISION_TASK"):
        instance = get_instance(work_item)
        instance.case.meta.update(compute_cycle_time(instance))
        instance.case.save()


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_decision(sender, work_item, user, context, **kwargs):  # noqa: C901
    if work_item.task_id == get_caluma_setting("DECISION_TASK"):
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)

        workflow = work_item.case.workflow_id
        history_text = gettext_noop("Evaluation completed")
        instance_state_name = "finished"

        if workflow == "building-permit":
            history_text = gettext_noop("Decision decreed")

            if domain_logic.CreateDecisionLogic.should_continue_after_decision(
                instance, work_item
            ):
                if settings.APPLICATION_NAME == "kt_be":
                    # set the construction control as responsible service
                    construction_control = set_construction_control(instance)
                    instance_state_name = "sb1"

                    # copy municipality tags for sb1
                    copy_municipality_tags(instance, construction_control)
                    copy_responsible_person_lead_authority(
                        instance, construction_control
                    )
                else:
                    construction_monitoring_task = Task.objects.get(
                        pk=settings.APPLICATION["CALUMA"][
                            "CONSTRUCTION_MONITORING_TASK"
                        ]
                    )
                    WorkItem.objects.create(
                        task=construction_monitoring_task,
                        name=construction_monitoring_task.name,
                        addressed_groups=work_item.addressed_groups,
                        controlling_groups=work_item.controlling_groups,
                        case=instance.case,
                        status=WorkItem.STATUS_READY,
                        created_by_user=user.username,
                        created_by_group=user.group,
                        deadline=(
                            timezone.now()
                            + timedelta(seconds=construction_monitoring_task.lead_time)
                        ),
                    )

            handle_appeal_decision(instance, work_item, user, camac_user)

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
        instance.set_instance_state(instance_state_name, camac_user)

        # trigger ech message for status change
        ruling.send(
            sender="post_complete_decision",
            instance=instance,
            user_pk=camac_user.pk,
            group_pk=user.camac_group,
        )

        if not context or not context.get("no-notification"):
            for config in get_notification_config(instance):
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
