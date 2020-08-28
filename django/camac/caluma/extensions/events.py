from logging import getLogger

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.events import (
    completed_case,
    completed_work_item,
    created_work_item,
    skipped_work_item,
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


@on(created_work_item)
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


@on(created_work_item)
def copy_paper_answer(sender, work_item, **kwargs):
    if work_item.task_id in get_caluma_setting("COPY_PAPER_ANSWER_TO", []):
        # copy answer to the papierdossier question in the case document to the
        # newly created work item document
        try:
            work_item.document.answers.create(
                question_id="papierdossier",
                value=work_item.case.document.answers.get(
                    question_id="papierdossier"
                ).value,
            )
        except caluma_form_models.Answer.DoesNotExist:
            log.warning(
                f"Could not find answer for question `papierdossier` in document for instance {work_item.case.meta.get('camac-instance-id')}"
            )


@on(created_work_item)
def post_create_work_item(sender, work_item, user, context, **kwargs):
    if "not-viewed" not in work_item.meta:
        work_item.meta.update(
            {"not-viewed": True, "notify-completed": True, "notify-deadline": True}
        )

    if (
        context
        and context.get("circulation-id")
        and work_item.task_id == get_caluma_setting("CIRCULATION_TASK")
        and "circulation-id" not in work_item.meta
    ):
        # Circulation work item was created by completing the work item before.
        # Write the circulation ID passed in the context down to the newly
        # created work items meta property
        work_item.meta["circulation-id"] = context["circulation-id"]

    if (
        context
        and context.get("activation-id")
        and work_item.task_id == get_caluma_setting("ACTIVATION_TASK")
        and "activation-id" not in work_item.meta
    ):
        # Activation work item was created by creating a circulation child case
        # Write the activation ID passed in the context down to the newly
        # created work items meta property
        work_item.meta["activation-id"] = context["activation-id"]

    work_item.save()


@on(completed_work_item)
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


@on(skipped_work_item)
@on(completed_work_item)
def post_complete_work_item(sender, work_item, user, **kwargs):
    # Completed work items should always be marked as read
    work_item.meta["not-viewed"] = False
    work_item.save()

    config = get_caluma_setting("POST_COMPLETE", {}).get(work_item.task_id)

    if config:
        for action_name, tasks in config.items():
            action = getattr(workflow_api, f"{action_name}_work_item")

            for item in work_item.case.work_items.filter(
                task_id__in=tasks, status=WorkItem.STATUS_READY
            ):
                action(item, user)


@on(completed_case)
def post_complete_circulation(sender, case, user, **kwargs):
    if case.workflow_id == get_caluma_setting("CIRCULATION_WORKFLOW"):
        parent_work_item = WorkItem.objects.filter(
            child_case=case,
            task_id=get_caluma_setting("CIRCULATION_TASK"),
            status=WorkItem.STATUS_READY,
        ).first()

        if parent_work_item:
            workflow_api.complete_work_item(parent_work_item, user)
