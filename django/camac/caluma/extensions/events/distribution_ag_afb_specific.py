from datetime import timedelta

from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import cancel_work_item
from caluma.caluma_workflow.events import post_create_work_item, post_resume_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.models import Inquiry
from camac.caluma.utils import date_to_deadline
from camac.user.models import Service

from .distribution import filter_by_task


@on(post_resume_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def set_cantonal_exam_deadline(sender, work_item, user, context=None, **kwargs):
    if settings.APPLICATION_NAME != "kt_ag":
        return

    addressed_service = Service.objects.get(pk=int(work_item.addressed_groups[0]))

    if addressed_service.slug != "afb":
        return

    cantonal_exam = WorkItem.objects.filter(
        task_id="cantonal-exam",
        status=WorkItem.STATUS_READY,
        case=work_item.case.family,
        deadline__isnull=True,
    ).first()

    if not cantonal_exam:
        return

    cantonal_exam.deadline = date_to_deadline(now().date() + timedelta(days=5))
    cantonal_exam.save(update_fields=["deadline"])


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_cantonal_exam_deadline_anfrage_intern(
    sender, work_item, user, context=None, **kwargs
):
    if settings.APPLICATION_NAME != "kt_ag" or work_item.task_id != "cantonal-exam":
        return

    responsible_service = work_item.case.instance.responsible_service()

    if responsible_service.slug != "afb":
        return

    work_item.deadline = date_to_deadline(now().date() + timedelta(days=5))
    work_item.save(update_fields=["deadline"])


@on(post_resume_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def set_document_supplement_deadline(sender, work_item, user, context=None, **kwargs):
    if settings.APPLICATION_NAME != "kt_ag":
        return

    check_work_item = WorkItem.objects.filter(
        task_id="check-document-supplement",
        status=WorkItem.STATUS_READY,
        case=work_item.child_case,
    ).first()

    if not check_work_item:  # pragma: no cover
        # This should never happen as the workflow for inquiry should always
        # create such a work item in the same child case.
        return

    has_sibling_inquiry = (
        Inquiry.objects.for_distribution_case(work_item.case)
        .addressed_to(work_item.addressed_groups)
        .only_active()
        .exclude(pk=work_item.pk)
        .exists()
    )

    addressed_service = Service.objects.get(pk=int(work_item.addressed_groups[0]))

    if addressed_service.slug == "afb" and has_sibling_inquiry:
        # If the AfB is addressed and there are already other inquiries for the
        # AfB (which means the AfB was invited for the second or more time in
        # the distribution) we set the deadline of the "check document
        # supplement" work item in order to appear in the work item lists.
        check_work_item.deadline = date_to_deadline(now().date() + timedelta(days=5))
        check_work_item.save(update_fields=["deadline"])
    else:
        # If the AfB is not addressed or it's the first inquiry for them, we
        # don't need the work item at all and cancel it therefore
        cancel_work_item(check_work_item, user, context)
