from datetime import datetime, timedelta

import pytz
from caluma.caluma_core.events import on
from caluma.caluma_workflow.api import skip_work_item, start_case
from caluma.caluma_workflow.events import (
    post_cancel_case,
    post_complete_case,
    post_complete_work_item,
    post_create_work_item,
)
from caluma.caluma_workflow.models import Workflow, WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext as _

from camac.caluma.utils import filter_by_task_base, filter_by_workflow_base
from camac.core.utils import create_history_entry
from camac.notification.utils import send_mail_without_request
from camac.user.models import User

from .general import get_instance


def get_construction_monitoring_settings(settings_keys):
    return filter(
        None,
        [
            settings.CONSTRUCTION_MONITORING.get(settings_key)
            for settings_key in (
                [settings_keys]
                if not isinstance(settings_keys, list)
                else settings_keys
            )
        ],
    )


def filter_by_workflow(settings_keys):
    return filter_by_workflow_base(settings_keys, get_construction_monitoring_settings)


def filter_by_task(settings_keys):
    return filter_by_task_base(settings_keys, get_construction_monitoring_settings)


def construction_step_can_continue(work_item):
    if not settings.CONSTRUCTION_MONITORING or not work_item.meta.get("construction-step-id"):
        return True  # pragma: no cover

    needs_approval_question = work_item.meta["construction-step"].get("needs-approval")

    if not needs_approval_question:
        return True

    answer_is_approved = (
        work_item.document.answers.filter(question_id=needs_approval_question)
        .values_list("value", flat=True)
        .first()
    )

    construction_step_is_approved = f"{needs_approval_question}-yes"

    return answer_is_approved == construction_step_is_approved


def can_perform_construction_monitoring(instance):
    if not settings.CONSTRUCTION_MONITORING:
        return False

    allow_forms = settings.CONSTRUCTION_MONITORING.get("ALLOW_FORMS")
    if not allow_forms:
        return True

    form_family = instance.form.family
    return form_family and form_family.name in allow_forms


CONSTRUCTION_STEP_TRANSLATIONS = {
    "construction-step-plan-construction-stage": _("Baubegleitung planen"),
    "construction-step-baufreigabe": _("Baufreigabe"),
    "construction-step-baubeginn": _("Baubeginn"),
    "construction-step-schnurgeruestabnahme": _("Schnurgeruestabnahme"),
    "construction-step-kanalisationsabnahme": _("Kanalisationsabnahme"),
    "construction-step-rohbauabnahme": _("Rohbauabnahme"),
    "construction-step-zwischenkontrolle": _("Zwischenkontrolle"),
    "construction-step-schlussabnahme-gebaeude": _("Schlussabnahme Gebaeude"),
    "construction-step-schlussabnahme-projekt": _("Schlussabnahme Projekt"),
}


@on(post_complete_work_item, raise_exception=True)
@filter_by_task(["INIT_CONSTRUCTION_MONITORING_TASK"])
@transaction.atomic
def post_complete_init_construction_monitoring(
    sender, work_item, user, context, **kwargs
):
    if context and context["skip"]:
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)
        history_text = _("Construction monitoring skipped")
        create_history_entry(instance, camac_user, history_text)


@on(post_create_work_item, raise_exception=True)
@filter_by_task("CONSTRUCTION_STAGE_TASK")
@transaction.atomic
def post_create_construction_stage(sender, work_item, user, context=None, **kwargs):
    # Start construction stage child case
    start_case(
        workflow=Workflow.objects.get(
            pk=settings.CONSTRUCTION_MONITORING["CONSTRUCTION_STAGE_WORKFLOW"]
        ),
        user=user,
        parent_work_item=work_item,
        context=context,
    )

    set_complete_construction_monitoring_deadline(work_item.child_case)


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def post_create_construction_step_work_item(sender, work_item, user, context, **kwargs):
    """Set needed meta attributes on the newly created work item."""

    if not settings.CONSTRUCTION_MONITORING or not work_item.task.meta.get("construction-step-id"):
        return

    if (
        work_item.task.meta["construction-step-id"]
        != settings.CONSTRUCTION_MONITORING["CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK"]
    ):
        work_item.name = f"{work_item.name} ({work_item.case.parent_work_item.name})"

    # Construction-step configuration contained in task meta
    work_item.meta.update(work_item.task.meta)
    work_item.save(update_fields=["meta", "name"])


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def post_complete_construction_step_work_item(
    sender, work_item, user, context, **kwargs
):
    """Set needed meta attributes on the newly created work item."""

    if not settings.CONSTRUCTION_MONITORING or not work_item.task.meta.get("construction-step-id"):
        return

    instance = get_instance(work_item)
    if (
        work_item.task.pk == settings.CONSTRUCTION_MONITORING["CONSTRUCTION_STEP_PLAN_CONSTRUCTION_STAGE_TASK"]
        and instance.instance_state.name
        == settings.CONSTRUCTION_MONITORING["PREVIOUS_INSTANCE_STATE"]
    ):
        camac_user = User.objects.get(username=user.username)
        history_text = _("Construction monitoring started")
        create_history_entry(instance, camac_user, history_text)

        instance.set_instance_state(
            settings.CONSTRUCTION_MONITORING["CONSTRUCTION_MONITORING_INSTANCE_STATE"],
            camac_user,
        )

    notifications = settings.CONSTRUCTION_MONITORING["NOTIFICATIONS"].get(
        work_item.task.pk, []
    )
    if construction_step_can_continue(work_item):
        for config in notifications:
            send_mail_without_request(
                config["template_slug"],
                user.username,
                user.camac_group,
                recipient_types=config["recipient_types"],
                instance={"id": instance.pk, "type": "instances"},
                work_item={"id": work_item.pk, "type": "work-items"},
            )


@on(post_complete_work_item, raise_exception=True)
@filter_by_task(["COMPLETE_CONSTRUCTION_MONITORING_TASK"])
@transaction.atomic
def post_complete_construction_monitoring(sender, work_item, user, context, **kwargs):
    for work_item in work_item.case.work_items.filter(
        task_id=settings.CONSTRUCTION_MONITORING["CONSTRUCTION_STAGE_TASK"],
        status=WorkItem.STATUS_READY,
    ):
        # Unfinished construction stages must be skipped
        skip_work_item(work_item=work_item, user=user, context=context)

    instance = get_instance(work_item)
    camac_user = User.objects.get(username=user.username)
    history_text = _("Construction monitoring completed")
    create_history_entry(instance, camac_user, history_text)


def set_complete_construction_monitoring_deadline(case):
    if not settings.CONSTRUCTION_MONITORING:
        return  # pragma: no cover

    main_case_work_items = case.parent_work_item.case.work_items
    has_running_construction_stages = main_case_work_items.filter(
        task_id=settings.CONSTRUCTION_MONITORING["CONSTRUCTION_STAGE_TASK"],
        child_case__status="running",
    ).exists()
    complete_construction_monitoring = main_case_work_items.filter(
        task_id=settings.CONSTRUCTION_MONITORING[
            "COMPLETE_CONSTRUCTION_MONITORING_TASK"
        ]
    ).first()

    deadline = None
    if not has_running_construction_stages:
        deadline = pytz.utc.localize(
            datetime.combine(
                datetime.now() + timedelta(seconds=864000), datetime.min.time()
            )
        )

    complete_construction_monitoring.deadline = deadline
    complete_construction_monitoring.save()


@on(post_cancel_case, raise_exception=True)
@filter_by_workflow(["CONSTRUCTION_STAGE_WORKFLOW"])
@transaction.atomic
def post_cancel_construction_stage(sender, case, user, context, **kwargs):
    set_complete_construction_monitoring_deadline(case)


@on(post_complete_case, raise_exception=True)
@filter_by_workflow(["CONSTRUCTION_STAGE_WORKFLOW"])
@transaction.atomic
def post_complete_construction_stage(sender, case, user, context, **kwargs):
    set_complete_construction_monitoring_deadline(case)

    notifications = settings.CONSTRUCTION_MONITORING["NOTIFICATIONS"].get(
        case.workflow.pk, []
    )
    for config in notifications:
        send_mail_without_request(
            config["template_slug"],
            user.username,
            user.camac_group,
            recipient_types=config["recipient_types"],
            instance={"id": case.family.instance.pk, "type": "instances"},
            case={"id": case.pk, "type": "cases"},
        )


@on(post_complete_work_item, raise_exception=True)
@filter_by_task(["COMPLETE_INSTANCE_TASK"])
@transaction.atomic
def post_complete_instance(sender, work_item, user, context, **kwargs):  # pragma: todo cover
    instance = get_instance(work_item)

    notifications = settings.CONSTRUCTION_MONITORING["NOTIFICATIONS"].get(
        work_item.task.pk, []
    )

    if (
        work_item
        and work_item.document.answers.filter(
            question_id="steuerverwaltung-informieren",
            value__contains=[
                "steuerverwaltung-informieren-steuerverwaltung-informieren"
            ],
        ).exists()
    ):
        notifications.append(
            {
                "template_slug": "notify-complete-instance",
                "recipient_types": ["tax_administration"],
            }
        )

    for config in notifications:
        send_mail_without_request(
            config["template_slug"],
            user.username,
            user.camac_group,
            recipient_types=config["recipient_types"],
            instance={"id": instance.pk, "type": "instances"},
            work_item={"id": work_item.pk, "type": "work-items"},
        )
