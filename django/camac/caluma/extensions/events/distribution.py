from datetime import datetime, timedelta
from itertools import chain

from caluma.caluma_core.events import on, send_event
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Form, Question
from caluma.caluma_workflow.api import (
    cancel_work_item,
    complete_work_item,
    reopen_case,
    skip_work_item,
    start_case,
    suspend_work_item,
)
from caluma.caluma_workflow.events import (
    post_cancel_work_item,
    post_complete_case,
    post_complete_work_item,
    post_create_work_item,
    post_redo_work_item,
    post_resume_work_item,
    pre_complete_work_item,
)
from caluma.caluma_workflow.models import Task, Workflow, WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.timezone import now

from camac.caluma.utils import (
    filter_by_task_base,
    filter_by_workflow_base,
    sync_inquiry_deadline,
)
from camac.constants import kt_bern as bern_constants
from camac.core.utils import create_history_entry
from camac.ech0211.signals import (
    accompanying_report_send,
    circulation_started,
    task_send,
)
from camac.notification.utils import send_mail_without_request
from camac.user.models import Service, User

from .general import get_instance


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
    return filter_by_workflow_base(settings_keys, get_distribution_settings)


def filter_by_task(settings_keys):
    return filter_by_task_base(settings_keys, get_distribution_settings)


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


@on(post_redo_work_item, raise_exception=True)
@filter_by_task("DISTRIBUTION_TASK")
@transaction.atomic
def post_redo_distribution(sender, work_item, user, context=None, **kwargs):
    check_distribution_work_item = (
        work_item.child_case.work_items.filter(
            task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
            status=WorkItem.STATUS_COMPLETED,
            addressed_groups=work_item.addressed_groups,
        )
        .order_by("-closed_at")
        .first()
    )

    reopen_case(
        case=work_item.child_case,
        work_items=list(
            chain(
                work_item.child_case.work_items.filter(
                    task_id=settings.DISTRIBUTION["DISTRIBUTION_COMPLETE_TASK"]
                ),
                [check_distribution_work_item] if check_distribution_work_item else [],
            )
        ),
        user=user,
        context=context,
    )

    # Create a new check-distribution work-item due to skipped distribution
    if not check_distribution_work_item:
        check_distribution_task = Task.objects.get(
            pk=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
        )

        check_distribution_work_item = WorkItem.objects.create(
            task=check_distribution_task,
            name=check_distribution_task.name,
            addressed_groups=work_item.addressed_groups,
            controlling_groups=work_item.addressed_groups,
            case=work_item.child_case,
            status=WorkItem.STATUS_READY,
            created_by_user=user.username,
            created_by_group=user.group,
            deadline=check_distribution_task.calculate_deadline(),
        )

        send_event(
            post_create_work_item,
            sender="post_redo_distribution",
            work_item=check_distribution_work_item,
            user=user,
            context={},
        )

    services = Service.objects.filter(
        pk__in=[
            *work_item.addressed_groups,
            *chain(
                *work_item.child_case.work_items.filter(
                    task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
                    status__in=[WorkItem.STATUS_COMPLETED, WorkItem.STATUS_SKIPPED],
                ).values_list("addressed_groups", flat=True)
            ),
        ]
    ).exclude(service_parent__isnull=False)

    create_inquiry_task = Task.objects.get(
        pk=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]
    )

    for service in services:
        WorkItem.objects.create(
            task=create_inquiry_task,
            name=create_inquiry_task.name,
            addressed_groups=[str(service.pk)],
            controlling_groups=[str(service.pk)],
            case=work_item.child_case,
            status=WorkItem.STATUS_READY,
            created_by_user=user.username,
            created_by_group=user.group,
        )

    instance = get_instance(work_item)
    camac_user = User.objects.get(username=user.username)

    instance.set_instance_state(
        settings.DISTRIBUTION["INSTANCE_STATE_DISTRIBUTION"],
        camac_user,
    )

    if settings.DISTRIBUTION["HISTORY"].get("REDO_DISTRIBUTION"):
        create_history_entry(
            instance,
            camac_user,
            settings.DISTRIBUTION["HISTORY"].get("REDO_DISTRIBUTION"),
        )

    if settings.DISTRIBUTION["ECH_EVENTS"]:
        circulation_started.send(
            sender="post_redo_distribution",
            instance=work_item.case.family.instance,
            user_pk=camac_user.pk,
            group_pk=user.camac_group,
        )

    redo_distribution_create_tasks = settings.DISTRIBUTION["REDO_DISTRIBUTION"].get(
        "CREATE_TASKS"
    )
    if redo_distribution_create_tasks:
        for task_name in redo_distribution_create_tasks:
            WorkItem.objects.create(
                task=Task.objects.get(slug=task_name),
                name=task_name,
                addressed_groups=work_item.addressed_groups,
                case=work_item.case,
                status=WorkItem.STATUS_READY,
                previous_work_item=work_item.previous_work_item,
            )


@on(post_redo_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_redo_inquiry(sender, work_item, user, context=None, **kwargs):
    # Get the last closed child work item of each task defined in `REDO_INQUIRY`
    reopen_work_items = [
        work_item.child_case.work_items.filter(task_id=task_id)
        .order_by("-closed_at")
        .values_list("pk", flat=True)
        .first()
        for task_id in settings.DISTRIBUTION["REDO_INQUIRY"].get("REOPEN_TASKS", [])
    ]

    reopen_case(
        case=work_item.child_case,
        work_items=work_item.child_case.work_items.filter(pk__in=reopen_work_items),
        user=user,
        context=context,
    )

    work_items_to_complete = work_item.child_case.work_items.filter(
        task_id__in=settings.DISTRIBUTION["REDO_INQUIRY"].get("COMPLETE_TASKS", []),
        status=WorkItem.STATUS_READY,
    )

    for work_item_to_complete in work_items_to_complete:
        complete_work_item(work_item=work_item_to_complete, user=user, context=context)


@on(post_create_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_create_inquiry(sender, work_item, user, context=None, **kwargs):
    # suspend work item so it's a draft
    suspend_work_item(work_item=work_item, user=user, context=context)

    default_deadline = now().date() + timedelta(
        days=settings.DISTRIBUTION["DEFAULT_DEADLINE_LEAD_TIME"]
    )
    default_answers = {
        settings.DISTRIBUTION["QUESTIONS"]["DEADLINE"]: default_deadline.isoformat(),
        **(context.get("answers", {}) if context else {}),
    }

    for slug, value in default_answers.items():
        question = Question.objects.get(pk=slug)

        if question.type == Question.TYPE_DATE:
            value = datetime.fromisoformat(value).date()

        save_answer(
            question=question,
            document=work_item.document,
            value=value,
            user=user,
            context=context,
        )

    sync_inquiry_deadline(work_item)


@on(post_resume_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_resume_inquiry(sender, work_item, user, context=None, **kwargs):
    # When correcting an instance in Kt. BE, the entire case is suspended and
    # resumed again when the correction is completed. Running inquiries are also
    # suspended and resumed again, which results in draft inquiries and already
    # sent inquiries from being (re-)sent. To mitigate this issue we only allow
    # corrections of the instance if there are no running inquiries. However,
    # checking for running inquiries fails, when only inquiries are running, which aren't
    # visible to the lead authority. This happens for example, when the lead authority
    # invites a service, which in turn invites subservices, but the invited service
    # already answers its own inquiry without waiting for the response of the
    # subservices.
    # In those cases, we ignore the resuming of the inquiry and for draft inquiries
    # restore the original status.
    if (
        settings.APPLICATION_NAME == "kt_bern"
        and work_item.case.family.instance.instance_state.pk
        == bern_constants.INSTANCE_STATE_CORRECTION_IN_PROGRESS
    ):
        if not work_item.child_case:
            work_item.status = WorkItem.STATUS_SUSPENDED
            work_item.save()

        return

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

    # sync inquiry deadline after starting child case to
    # ensure that potential child case work-items' deadlines
    # are also synced
    sync_inquiry_deadline(work_item)

    # complete init distribution work item
    init_work_item = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
        status=WorkItem.STATUS_READY,
    ).first()

    if init_work_item:
        complete_work_item(work_item=init_work_item, user=user, context=context)

    # cancel check-distribution work item
    check_distribution_work_item = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=work_item.controlling_groups,
    ).first()

    if check_distribution_work_item:
        cancel_work_item(
            work_item=check_distribution_work_item, user=user, context=context
        )

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

    addressed_check_work_item = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["INQUIRY_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=work_item.addressed_groups,
    ).first()

    # If there is a "check-inquiries" work item addressed to the service
    # that just completed an inquiry, it must be automatically completed
    if addressed_check_work_item:
        complete_work_item(
            work_item=addressed_check_work_item, user=user, context=context
        )

    pending_addressed_inquiries = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=work_item.addressed_groups,
    )

    # If there are no more pending inquiries addressed to the service that just
    # completed an inquiry and the addressed group is not the responsible service,
    # we need to cancel all create and redo inquiry work items in order to
    # prohibit new or reopened inquiries controlled by this service.
    responsible_service_id = work_item.case.family.instance.responsible_service(
        filter_type="municipality"
    ).pk
    if (
        not pending_addressed_inquiries.exists()
        and str(responsible_service_id) not in work_item.addressed_groups
    ):
        for work_item_to_cancel in work_item.case.work_items.filter(
            task_id__in=[
                settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                settings.DISTRIBUTION["INQUIRY_REDO_TASK"],
            ],
            status=WorkItem.STATUS_READY,
            addressed_groups=work_item.addressed_groups,
        ):
            cancel_work_item(work_item=work_item_to_cancel, user=user, context=context)

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

    check_distribution_work_item = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["DISTRIBUTION_CHECK_TASK"],
        status=WorkItem.STATUS_READY,
        addressed_groups=work_item.addressed_groups,
    ).first()

    if check_distribution_work_item:
        complete_work_item(
            work_item=check_distribution_work_item, user=user, context=context
        )

    for work_item in work_item.case.work_items.filter(
        status__in=[WorkItem.STATUS_READY, WorkItem.STATUS_SUSPENDED]
    ):
        # everything else canceled
        cancel_work_item(work_item=work_item, user=user, context=context)


@on(post_complete_work_item, raise_exception=True)
@filter_by_task("DISTRIBUTION_COMPLETE_TASK")
@transaction.atomic
def post_complete_distribution(sender, work_item, user, context=None, **kwargs):
    has_inquiries = (
        work_item.case.work_items.filter(task_id=settings.DISTRIBUTION["INQUIRY_TASK"])
        .exclude(status=WorkItem.STATUS_CANCELED)
        .exists()
    )

    text = (
        settings.DISTRIBUTION["HISTORY"].get("COMPLETE_DISTRIBUTION")
        if has_inquiries
        else settings.DISTRIBUTION["HISTORY"].get("SKIP_DISTRIBUTION")
    )

    if text:
        create_history_entry(
            work_item.case.family.instance,
            User.objects.get(username=user.username),
            text,
        )


@on(post_cancel_work_item, raise_exception=True)
@filter_by_task("INQUIRY_TASK")
@transaction.atomic
def post_cancel_inquiry(sender, work_item, user, context=None, **kwargs):
    service_inquiries = work_item.case.work_items.filter(
        task_id=settings.DISTRIBUTION["INQUIRY_TASK"],
        addressed_groups=work_item.addressed_groups,
    ).exclude(status=WorkItem.STATUS_CANCELED)

    if not service_inquiries.exists():
        # Cancel the create inquiry work item if no other inquiry for this
        # service exists
        try:
            create_inquiry_work_item = work_item.case.work_items.get(
                task_id=settings.DISTRIBUTION["INQUIRY_CREATE_TASK"],
                addressed_groups=work_item.addressed_groups,
                status=WorkItem.STATUS_READY,
            )

            cancel_work_item(
                work_item=create_inquiry_work_item, user=user, context=context
            )
        except WorkItem.DoesNotExist:
            # This is expected for subservices which must not have a create
            # inquiry work item
            pass
        except WorkItem.MultipleObjectsReturned:
            # If this happens, there must be some kind of issue in the workflow
            # since no service should ever have multiple ready create inquiry
            # work items
            service = Service.objects.get(pk=work_item.addressed_groups[0])

            raise RuntimeError(
                (
                    f'Service "{service.get_name()}" has multiple '
                    f'"{settings.DISTRIBUTION["INQUIRY_CREATE_TASK"]}" work '
                    f"items on instance {work_item.case.family.instance.pk}"
                )
            )


@on(post_complete_work_item, raise_exception=True)
@filter_by_task("INQUIRY_CHECK_TASK")
@transaction.atomic
def post_complete_inquiry_check(
    sender, work_item, user, context=None, **kwargs
):  # pragma: no cover
    if settings.ADDITIONAL_DEMAND:
        init_additional_demand = work_item.case.work_items.filter(
            task_id=settings.ADDITIONAL_DEMAND["ADDITIONAL_DEMAND_CREATE_TASK"],
            status=WorkItem.STATUS_READY,
            addressed_groups=work_item.previous_work_item.addressed_groups,
        ).first()
        if init_additional_demand:
            cancel_work_item(
                work_item=init_additional_demand, user=user, context=context
            )
