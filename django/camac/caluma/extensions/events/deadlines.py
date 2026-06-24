from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import (
    post_cancel_work_item,
    post_complete_work_item,
    post_create_work_item,
    post_redo_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.event_utils import (
    filter_by_canton,
    filter_by_task,
    if_module_enabled,
    setting,
)
from camac.caluma.extensions.events.general import get_instance
from camac.caluma.models import Inquiry
from camac.deadlines import models as deadlines_models
from camac.user.models import Service


def _get_inquiry_decision_answer(work_item):
    fill_work_item = (
        work_item
        if work_item.task.slug == settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"]
        else (
            WorkItem.objects.filter(
                case=work_item.child_case,
                task__slug=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
            )
            .order_by("-created_at")
            .first()
        )
    )
    decision_answer = (
        fill_work_item.case.document.answers.filter(
            question__slug=settings.DISTRIBUTION["QUESTIONS"]["STATUS"]
        ).first()
        if fill_work_item and fill_work_item.case.document
        else None
    )
    return decision_answer.value if decision_answer else None


@on(post_create_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task("withdrawal-check")
@transaction.atomic
def post_create_withdrawal_check_closes_suspensions(
    sender, work_item, user, context=None, **kwargs
):
    """Close all open suspensions when the withdrawal is requested."""
    instance = get_instance(work_item)

    for service in Service.objects.filter(pk__in=work_item.addressed_groups):
        if deadline := instance.deadlines.filter(service=service).first():
            for suspension in deadline.suspensions.for_deadline(deadline).only_open():
                suspension.complete()


@on(post_create_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task(setting("ADDITIONAL_DEMAND", "FILL_TASK"))
@transaction.atomic
def post_create_fill_additional_demand(sender, work_item, user, context=None, **kwargs):
    """Create a deadline suspension when an additional demand is created.

    When an additional demand is created, a new deadline suspension will start.
    This suspension will be linked to the workitem, and automatically completed when
    the additional demand is completed.
    """

    main_workitem = (
        WorkItem.objects.filter(
            child_case=work_item.case, task__slug=settings.ADDITIONAL_DEMAND.get("TASK")
        )
        .order_by("-created_at")
        .first()
    )
    if main_workitem:
        service = Service.objects.get(pk=main_workitem.created_by_group)
        instance = get_instance(main_workitem)

        if deadline := instance.deadlines.filter(service=service).first():
            deadlines_models.Suspension.objects.create(
                deadline=deadline,
                work_item=main_workitem,
                reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND,
                start_date=now(),
            )
            deadline.recalculate_progression()


@on(post_cancel_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task(setting("ADDITIONAL_DEMAND", "TASK"))
@transaction.atomic
def post_cancel_additional_demand(sender, work_item, user, context=None, **kwargs):
    """Update the deadline when an additional demand is canceled.

    The suspension will be closed and the deadline will be recalculated.
    """

    service = Service.objects.get(pk=work_item.created_by_group)
    instance = get_instance(work_item)

    if deadline := instance.deadlines.filter(service=service).first():
        if suspension := (
            deadlines_models.Suspension.objects.for_deadline(deadline)
            .for_workitem(work_item=work_item)
            .order_by("-created_at")
            .first()
        ):
            suspension.complete()


@on(post_complete_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task(setting("ADDITIONAL_DEMAND", "FILL_TASK"))
@transaction.atomic
def post_complete_fill_additional_demand(
    sender, work_item, user, context=None, **kwargs
):
    """Complete a suspension when an additional demand is completed."""

    main_workitem = (
        WorkItem.objects.filter(
            child_case=work_item.case, task__slug=settings.ADDITIONAL_DEMAND.get("TASK")
        )
        .order_by("-created_at")
        .first()
    )
    if main_workitem:
        service = Service.objects.get(pk=main_workitem.created_by_group)
        instance = get_instance(main_workitem)

        if deadline := instance.deadlines.filter(service=service).first():
            if suspension := (
                deadlines_models.Suspension.objects.for_deadline(deadline)
                .for_workitem(work_item=main_workitem)
                .order_by("-created_at")
                .first()
            ):
                suspension.complete()


@on(post_create_work_item, raise_exception=True)
@filter_by_canton("kt_gr")
@if_module_enabled("DEADLINES")
@filter_by_task(setting("PUBLICATION", "FILL_TASKS.PUBLIC"))
@transaction.atomic
def post_create_publication(sender, work_item, user, context=None, **kwargs):
    """Reset the responsible service start-date when a publication workitem is created."""

    instance = get_instance(work_item)
    for deadline in deadlines_models.InstanceDeadline.objects.for_instance(instance):
        if deadline.service == instance.responsible_service():
            # Recalculate with a new start date
            deadline.start_date = None
            deadline.save(update_fields=["start_date"])
        deadline.recalculate_progression()


@on(post_complete_work_item, raise_exception=True)
@filter_by_canton("kt_gr")
@if_module_enabled("DEADLINES")
@filter_by_task(setting("PUBLICATION", "FILL_TASKS.PUBLIC"), "formal-exam")
@transaction.atomic
def post_complete_publication_or_formal_exam(
    sender, work_item, user, context=None, **kwargs
):
    """Update the deadlines when a publication or formal exam is completed."""

    instance = get_instance(work_item)

    for deadline in deadlines_models.InstanceDeadline.objects.for_instance(instance):
        if deadline.service == instance.responsible_service():
            # Recalculate with a new start date
            deadline.start_date = None
            deadline.save(update_fields=["start_date"])
        deadline.recalculate_progression()


@on(post_redo_work_item, raise_exception=True)
@filter_by_canton("kt_ag")
@if_module_enabled("DEADLINES")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
@transaction.atomic
def post_redo_inquiry_ag(sender, work_item, user, context=None, **kwargs):
    """Create a suspension for the time between redoing the inquiry in AG."""
    instance = get_instance(work_item)
    fill_work_item = (
        WorkItem.objects.filter(
            case=work_item.child_case,
            task__slug=settings.DISTRIBUTION["INQUIRY_ANSWER_FILL_TASK"],
        )
        .order_by("-created_at")
        .first()
    )
    for service in Service.objects.filter(pk__in=fill_work_item.addressed_groups):
        # If the inquiry is re-opened, we create a new suspension starting at the
        # existing inquiry close date, unless the decision answer
        # is "Unterlagenergänzung"
        if deadline := instance.deadlines.filter(service=service).first():
            decision_answer = _get_inquiry_decision_answer(fill_work_item)
            if decision_answer != settings.DISTRIBUTION["ANSWERS"]["STATUS"][
                "CLAIM"
            ] and not (
                deadlines_models.Suspension.objects.for_deadline(deadline)
                .for_workitem(work_item)
                .only_open()
                .exists()
            ):
                suspension = deadlines_models.Suspension.objects.create(
                    deadline=deadline,
                    work_item=work_item,
                    start_date=fill_work_item.closed_at,
                    reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
                )
                suspension.complete()

            # Close any existing open inquiry claim suspensions for the deadline.
            for suspension in deadline.suspensions.only_open().filter(
                reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
            ):
                suspension.complete()


@on(post_create_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_ANSWER_FILL_TASK"))
@transaction.atomic
def post_create_inquiry(sender, work_item, user, context=None, **kwargs):
    """Create a deadline when an inquiry is sent.

    If the deadline already exists, close any existing open inquiry
    claim suspensions.

    If a previous inquiry exists, create a new suspension for the time between
    the previous inquiry and the new inquiry.
    """
    instance = get_instance(work_item)
    for service in Service.objects.filter(pk__in=work_item.addressed_groups):
        instance.deadlines.create_deadline(instance=instance, service=service)

        # If the service is re-invited (previous inquiry exists), we create a
        # new suspension starting at the previous inquiry close date, unless
        # the decision answer is "Unterlagenergänzung" (only exists in AG).
        if deadline := instance.deadlines.filter(service=service).first():
            workitem_inquiry = (
                Inquiry.objects.addressed_to(service.pk)
                .only_active()
                .filter(child_case=work_item.case)
                .order_by("-created_at")
                .first()
            )
            previous_inquiry = (
                Inquiry.objects.for_distribution_case(workitem_inquiry.case)
                .addressed_to(work_item.addressed_groups)
                .only_answered()
                .exclude(pk=workitem_inquiry.pk)
                .order_by("-created_at")
                .first()
            )
            if (
                previous_inquiry
                and _get_inquiry_decision_answer(previous_inquiry)
                != settings.DISTRIBUTION["ANSWERS"]["STATUS"]["CLAIM"]
                and not (
                    deadlines_models.Suspension.objects.for_deadline(deadline)
                    .for_workitem(previous_inquiry)
                    .only_open()
                    .exists()
                )
            ):
                suspension = deadlines_models.Suspension.objects.create(
                    deadline=deadline,
                    work_item=previous_inquiry,
                    start_date=previous_inquiry.closed_at,
                    reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
                )
                suspension.complete()

            # Close any existing open inquiry claim suspensions for the deadline.
            for suspension in deadline.suspensions.only_open().filter(
                reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
            ):
                suspension.complete()


@on(post_complete_work_item, raise_exception=True)
@filter_by_canton("kt_ag")
@if_module_enabled("DEADLINES")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_ANSWER_FILL_TASK"))
@transaction.atomic
def post_complete_inquiry_fill_ag(sender, work_item, user, context=None, **kwargs):
    """Create a suspension for inquired service based on the decision."""
    instance = get_instance(work_item)
    decision_answer = _get_inquiry_decision_answer(work_item)

    # If the decision is not "Unterlagenergänzung", we do not create a suspension.
    if decision_answer != settings.DISTRIBUTION["ANSWERS"]["STATUS"]["CLAIM"]:
        return

    for service in Service.objects.filter(pk__in=work_item.addressed_groups):
        if deadline := instance.deadlines.filter(service=service).first():
            workitem_inquiry = (
                Inquiry.objects.addressed_to(service.pk)
                .only_active()
                .filter(child_case=work_item.case)
                .order_by("-created_at")
                .first()
            )
            if not (
                deadline.suspensions.for_deadline(deadline)
                .for_workitem(workitem_inquiry)
                .first()
            ):
                deadlines_models.Suspension.objects.create(
                    deadline=deadline,
                    work_item=workitem_inquiry,
                    start_date=now().date(),
                    reason=deadlines_models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_INQUIRY_CLAIM,
                )

            deadline.recalculate_progression()


@on(post_complete_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
@transaction.atomic
def post_complete_inquiry(sender, work_item, user, context=None, **kwargs):
    """Update the deadline when an inquiry is completed."""

    instance = get_instance(work_item)
    for deadline in deadlines_models.InstanceDeadline.objects.for_instance(instance):
        deadline.recalculate_progression()


@on(post_complete_work_item, raise_exception=True)
@if_module_enabled("DEADLINES")
@filter_by_task(setting("DECISION", "TASK"))
@transaction.atomic
def post_complete_decision(sender, work_item, user, context=None, **kwargs):
    """Update the process deadline date when a decision is completed."""

    instance = get_instance(work_item)
    for deadline in deadlines_models.InstanceDeadline.objects.for_instance(instance):
        deadline.recalculate_progression()
