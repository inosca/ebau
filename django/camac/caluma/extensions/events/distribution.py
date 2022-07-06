from datetime import datetime

import pytz
from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form, Question
from caluma.caluma_workflow.api import (
    cancel_work_item,
    complete_work_item,
    skip_work_item,
    start_case,
    suspend_work_item,
)
from caluma.caluma_workflow.events import (
    post_complete_case,
    post_complete_work_item,
    post_create_work_item,
    post_resume_work_item,
    pre_complete_work_item,
)
from caluma.caluma_workflow.models import Workflow, WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.ech0211.signals import accompanying_report_send, task_send
from camac.notification.utils import send_mail_without_request
from camac.user.models import User


def send_inquiry_notification(settings_key, inquiry_work_item, user):
    notification_config = settings.DISTRIBUTION["NOTIFICATIONS"].get(settings_key)

    if notification_config:
        send_mail_without_request(
            notification_config["template_slug"],
            user.username,
            user.camac_group,
            instance={
                "id": inquiry_work_item.case.family.instance.pk,
                "type": "instances",
            },
            inquiry={"id": inquiry_work_item.pk, "type": "work-items"},
            recipient_types=notification_config["recipient_types"],
        )


def get_distribution_settings(settings_keys):
    return filter(
        None,
        [
            settings.DISTRIBUTION.get(settings_key)
            for settings_key in (
                [settings_keys]
                if not isinstance(settings_keys, list)
                else settings_keys
            )
        ],
    )


def filter_by_workflow(settings_keys):
    return filter_events(
        lambda case: case.workflow_id in get_distribution_settings(settings_keys)
    )


def filter_by_task(settings_keys):
    return filter_events(
        lambda work_item: work_item.task_id in get_distribution_settings(settings_keys)
    )


@on(post_complete_case, raise_exception=True)
@filter_by_workflow(["INQUIRY_WORKFLOW", "DISTRIBUTION_WORKFLOW"])
@transaction.atomic
def post_complete_inquiry_or_distribution_case(
    sender, case, user, context=None, **kwargs
):
    complete_work_item(work_item=case.parent_work_item, user=user, context=context)


@on(post_create_work_item, raise_exception=True)
@filter_by_task("DISTRIBUTION_TASK")
@transaction.atomic
def post_create_distribution(sender, work_item, user, context=None, **kwargs):
    # start distribution child case
    start_case(
        workflow=Workflow.objects.get(
            pk=settings.DISTRIBUTION["DISTRIBUTION_WORKFLOW"]
        ),
        user=user,
        parent_work_item=work_item,
        context=context,
    )


@on(post_create_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_create_inquiry(sender, work_item, user, context=None, **kwargs):
    # suspend work item so it's a draft
    suspend_work_item(work_item=work_item, user=user, context=context)

    # set initial deadline value
    save_answer(
        question=Question.objects.get(
            pk=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
        ),
        document=work_item.document,
        value=now().date() + settings.DISTRIBUTION["DEFAULT_DEADLINE_DELTA"],
        user=user,
        context=context,
    )


@on(post_resume_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_resume_inquiry(sender, work_item, user, context=None, **kwargs):
    # update work item deadline from form data
    deadline_date = work_item.document.answers.get(
        question_id=Question.objects.get(
            pk=settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]
        )
    ).date
    work_item.deadline = pytz.utc.localize(
        datetime.combine(deadline_date, datetime.min.time())
    )
    work_item.save()

    # start inquiry child case
    start_case(
        workflow=Workflow.objects.get(pk=settings.DISTRIBUTION["INQUIRY_WORKFLOW"]),
        form=Form.objects.get(pk=settings.DISTRIBUTION["INQUIRY_ANSWER_FORM"]),
        user=user,
        parent_work_item=work_item,
        context={
            **(context if context else {}),
            "addressed_groups": work_item.addressed_groups,
        },
    )

    # complete init distribution work item
    init_work_item = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
        status=WorkItem.STATUS_READY,
    ).first()

    if init_work_item:
        complete_work_item(work_item=init_work_item, user=user, context=context)

    # send notification to addressed service
    send_inquiry_notification("INQUIRY_SENT", work_item, user)

    if settings.DISTRIBUTION["ECH_EVENTS"]:
        camac_user = User.objects.get(username=user.username)
        task_send.send(
            sender="post_resume_inquiry",
            instance=work_item.case.family.instance,
            user_pk=camac_user.pk,
            group_pk=user.camac_group,
            inquiry=work_item,
        )


@on(post_complete_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_complete_inquiry(sender, work_item, user, context=None, **kwargs):
    # send notification to controlling service
    send_inquiry_notification("INQUIRY_ANSWERED", work_item, user)

    if settings.DISTRIBUTION["ECH_EVENTS"]:
        camac_user = User.objects.get(username=user.username)
        accompanying_report_send.send(
            sender="post_complete_inquiry",
            instance=work_item.case.family.instance,
            user_pk=camac_user.pk,
            group_pk=user.camac_group,
            inquiry=work_item,
            attachments=context.get("attachments") if context else None,
        )


@on(pre_complete_work_item, raise_exception=True)
@filter_by_task("DISTRIBUTION_COMPLETE_TASK")
@transaction.atomic
def pre_complete_distribution(sender, work_item, user, context=None, **kwargs):
    for work_item in work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["INQUIRY_TASK"], status=WorkItem.STATUS_READY
    ):
        # unanswered inquiries must be skipped
        skip_work_item(work_item=work_item, user=user, context=context)

    for work_item in work_item.case.work_items.filter(
        status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED]
    ):
        # everything else canceled
        cancel_work_item(work_item=work_item, user=user, context=context)
