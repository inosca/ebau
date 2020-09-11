from logging import getLogger

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.events import (
    post_complete_case,
    post_complete_work_item,
    post_create_work_item,
    pre_complete_work_item,
    pre_skip_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.core import mail
from django.template.loader import get_template
from django.utils.translation import gettext as _

from camac.caluma.api import CalumaApi
from camac.user import models as user_models
from camac.user.utils import unpack_service_emails

log = getLogger()

COMPLETE_WORKITEM_SUBJECT = _("Abgeschlossene Aufgabe")


def get_caluma_setting(key, default=None):
    return settings.APPLICATION.get("CALUMA", {}).get(key, default)


@on(post_create_work_item)
def copy_sb_personal(sender, work_item, **kwargs):
    for config in get_caluma_setting("COPY_PERSONAL", []):
        if work_item.task_id == config["TASK"]:
            CalumaApi().copy_table_answer(
                source_document=config["DOCUMENT"](work_item),
                target_document=work_item.document,
                source_question=config["SOURCE"],
                target_question=config["TARGET"],
                source_question_fallback=config["FALLBACK"],
            )


@on(post_create_work_item)
def copy_paper_answer(sender, work_item, **kwargs):
    if work_item.task_id in get_caluma_setting("COPY_PAPER_ANSWER_TO", []):
        # copy answer to the papierdossier question in the case document to the
        # newly created work item document
        try:
            work_item.document.answers.update_or_create(
                question_id="papierdossier",
                defaults={
                    "value": work_item.case.document.answers.get(
                        question_id="papierdossier"
                    ).value
                },
            )
        except caluma_form_models.Answer.DoesNotExist:
            log.warning(
                f"Could not find answer for question `papierdossier` in document for instance {work_item.case.meta.get('camac-instance-id')}"
            )


@on(post_create_work_item)
def set_meta_attributes(sender, work_item, user, context, **kwargs):
    """Set needed meta attributes on the newly created work item.

    Some attributes just need a default value if they don't exist yet in the
    meta of the work item. Others will be passed in the context.
    """

    META_CONFIG = {
        "not-viewed": {"default": True},
        "notify-completed": {"default": True},
        "notify-deadline": {"default": True},
        "circulation-id": {
            "from_context": True,
            "tasks": [get_caluma_setting("CIRCULATION_TASK")],
        },
        "activation-id": {
            "from_context": True,
            "tasks": get_caluma_setting("ACTIVATION_TASKS"),
        },
    }

    for attribute, config in META_CONFIG.items():
        tasks = config.get("tasks")
        from_context = config.get("from_context")

        if attribute in work_item.meta:
            # attribute is already set on the meta
            continue

        if tasks and work_item.task_id not in tasks:
            # incorrect task
            continue

        if from_context and not context.get(attribute):
            # context does not contain attribute
            log.warning(f"Attribute `{attribute}` is not passed in the context")
            continue

        work_item.meta[attribute] = (
            context.get(attribute) if from_context else config.get("default")
        )

    work_item.save()


@on(post_complete_work_item)
def notify_completed_work_item(sender, work_item, **kwargs):
    if not work_item.meta.get("notify-completed", True):
        return

    # controlling services are notified
    services = user_models.Service.objects.filter(
        pk__in=work_item.controlling_groups
    ).filter(notification=True)

    recipients = unpack_service_emails(services)

    closed_by = user_models.User.objects.filter(
        username=work_item.closed_by_user
    ).first()
    template = get_template("mails/notify_completed_workitem.txt")
    body = template.render({"work_item": work_item, "closed_by": closed_by})

    emails = [
        mail.EmailMessage(
            COMPLETE_WORKITEM_SUBJECT, body, settings.DEFAULT_FROM_EMAIL, to=[rec]
        )
        for rec in recipients
    ]

    connection = mail.get_connection()
    connection.open()
    connection.send_messages(emails)
    connection.close()


@on(pre_skip_work_item)
@on(pre_complete_work_item)
def pre_complete_work_item(sender, work_item, user, **kwargs):
    # Completed work items should always be marked as read
    work_item.meta["not-viewed"] = False
    work_item.save()

    config = get_caluma_setting("PRE_COMPLETE", {}).get(work_item.task_id)

    if config:
        for action_name, tasks in config.items():
            action = getattr(workflow_api, f"{action_name}_work_item")

            for item in work_item.case.work_items.filter(
                task_id__in=tasks, status=WorkItem.STATUS_READY
            ):
                action(item, user)


@on(post_complete_case)
def post_complete_circulation(sender, case, user, **kwargs):
    if case.workflow_id == get_caluma_setting("CIRCULATION_WORKFLOW"):
        parent_work_item = WorkItem.objects.filter(
            child_case=case,
            task_id=get_caluma_setting("CIRCULATION_TASK"),
            status=WorkItem.STATUS_READY,
        ).first()

        if parent_work_item:
            workflow_api.complete_work_item(parent_work_item, user)
