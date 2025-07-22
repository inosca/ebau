from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import (
    post_cancel_work_item,
    post_complete_work_item,
    post_create_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.extensions.events.general import get_instance
from camac.deadlines import models as deadlines_models
from camac.user.models import Service


def filter_by_tasks(task_ids):
    """Filter events by a list of task slug constants."""
    return filter_events(lambda work_item: work_item.task.slug in task_ids)


def filter_by_additional_demand_task(settings_key):
    """Filter events by the additional demand task slug defined in settings."""
    return filter_events(
        lambda work_item: work_item.task.slug
        == settings.ADDITIONAL_DEMAND.get(settings_key)
    )


def filter_by_distribution_task(settings_key):
    """Filter events by the distribution task slug defined in settings."""
    return filter_events(
        lambda work_item: work_item.task.slug == settings.DISTRIBUTION.get(settings_key)
    )


def filter_by_decision_task(settings_key):
    """Filter events by the decision task slug defined in settings."""
    return filter_events(
        lambda work_item: work_item.task.slug == settings.DECISION.get(settings_key)
    )


@on(post_create_work_item, raise_exception=True)
@filter_by_additional_demand_task("FILL_TASK")
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
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
@filter_by_additional_demand_task("TASK")
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
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
            .for_additional_demand(work_item=work_item)
            .order_by("-created_at")
            .first()
        ):
            suspension.complete()


@on(post_complete_work_item, raise_exception=True)
@filter_by_additional_demand_task("FILL_TASK")
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
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
                .for_additional_demand(work_item=main_workitem)
                .order_by("-created_at")
                .first()
            ):
                suspension.complete()


@on(post_complete_work_item, raise_exception=True)
@filter_by_tasks(["fill-publication", "formal-exam"])
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
@transaction.atomic
def post_complete_publication(sender, work_item, user, context=None, **kwargs):
    """Update the deadlines when a publication or formal exam is completed."""

    instance = get_instance(work_item)

    for deadline in deadlines_models.InstanceDeadline.objects.for_instance(instance):
        deadline.recalculate_progression()


@on(post_create_work_item, raise_exception=True)
@filter_by_distribution_task("INQUIRY_ANSWER_FILL_TASK")
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
@transaction.atomic
def post_create_inquiry(sender, work_item, user, context=None, **kwargs):
    """Create a deadline when an inquiry is sent."""

    instance = get_instance(work_item)
    for service in Service.objects.filter(pk__in=work_item.addressed_groups):
        instance.deadlines.create_deadline(instance=instance, service=service)


@on(post_complete_work_item, raise_exception=True)
@filter_by_distribution_task("INQUIRY_TASK")
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
@transaction.atomic
def post_complete_inquiry(sender, work_item, user, context=None, **kwargs):
    """Update the deadline when an inquiry is completed."""

    instance = get_instance(work_item)
    for service in Service.objects.filter(pk__in=work_item.addressed_groups):
        instance.deadlines.update_service_deadline(instance=instance, service=service)


@on(post_complete_work_item, raise_exception=True)
@filter_by_decision_task("TASK")
@filter_events(lambda: settings.DEADLINES and settings.DEADLINES.enabled)
@transaction.atomic
def post_complete_decision(sender, work_item, user, context=None, **kwargs):
    """Update the process deadline date when a decision is completed.

    Only when no process deadline date is set already.
    """

    instance = get_instance(work_item)
    service = instance.responsible_service()

    deadline = instance.deadlines.filter(service=service).first()
    if deadline and not deadline.process_deadline_date:
        answer_deadline = work_item.document.answers.filter(
            question__slug="decision-date"
        ).first()

        deadline.process_deadline_date = (
            answer_deadline.date if answer_deadline else None
        )
        deadline.save()
