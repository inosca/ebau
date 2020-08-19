from logging import getLogger

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_workflow.events import completed_work_item, created_work_item
from django.conf import settings
from django.core import mail
from django.template.loader import get_template
from django.utils.translation import gettext as _

from camac.caluma.api import CalumaApi
from camac.user import models as user_models
from camac.user.utils import unpack_service_emails

log = getLogger()

COMPLETE_WORKITEM_SUBJECT = _("Abgeschlossene Aufgabe")


@on(created_work_item)
def copy_sb_personal(sender, work_item, **kwargs):
    if work_item.task.slug == "sb1":
        CalumaApi().copy_table_answer(
            source_document=work_item.case.document,
            target_document=work_item.document,
            source_question="personalien-sb",
            target_question="personalien-sb1-sb2",
            source_question_fallback="personalien-gesuchstellerin",
        )

    if work_item.task.slug == "sb2":
        CalumaApi().copy_table_answer(
            source_document=work_item.case.work_items.get(task_id="sb1").document,
            target_document=work_item.document,
            source_question="personalien-sb1-sb2",
            target_question="personalien-sb1-sb2",
        )


@on(created_work_item)
def copy_paper_answer(sender, work_item, **kwargs):
    if work_item.task.slug in ["nfd", "sb1", "sb2"]:
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
def post_complete_work_item(sender, work_item, **kwargs):
    if "not-viewed" not in work_item.meta:
        work_item.meta.update(
            {"not-viewed": True, "notify-completed": True, "notify-deadline": True}
        )
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

    closed_by = user_models.User.objects.get(username=work_item.closed_by_user)
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
