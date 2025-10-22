from caluma.caluma_core.events import on
from caluma.caluma_form import api as form_api
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import complete_work_item, start_case
from caluma.caluma_workflow.events import (
    post_cancel_work_item,
    post_complete_case,
    post_complete_work_item,
    post_create_work_item,
)
from caluma.caluma_workflow.models import Workflow, WorkItem
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext_noop

from camac.caluma.utils import filter_by_task_base, filter_by_workflow_base
from camac.core.utils import create_history_entry
from camac.ech0211.signals import file_subsequently
from camac.notification.utils import send_mail_without_request
from camac.user.models import User

from .general import get_instance


def get_additional_demand_settings(settings_keys):
    return filter(
        None,
        [
            settings.ADDITIONAL_DEMAND.get(settings_key)
            for settings_key in (
                [settings_keys]
                if not isinstance(settings_keys, list)
                else settings_keys
            )
        ],
    )


def filter_by_workflow(settings_keys):
    return filter_by_workflow_base(settings_keys, get_additional_demand_settings)


def filter_by_task(settings_keys):
    return filter_by_task_base(settings_keys, get_additional_demand_settings)


def _has_pending_work_items(work_item, task_id):
    return WorkItem.objects.filter(
        task_id=task_id,
        case__family=get_instance(work_item).case.family,
        status=WorkItem.STATUS_READY,
    ).exists()


@on(post_create_work_item, raise_exception=True)
@filter_by_task("TASK")
@transaction.atomic
def post_create_additional_demand(sender, work_item, user, context=None, **kwargs):
    # start child case
    start_case(
        workflow=Workflow.objects.get(pk=settings.ADDITIONAL_DEMAND["WORKFLOW"]),
        user=user,
        parent_work_item=work_item,
        context=context,
        created_by_user=user.group,
        created_by_group=user.group,
        modified_by_user=user.group,
        modified_by_group=user.group,
    )

    instance = get_instance(work_item)
    states = settings.ADDITIONAL_DEMAND.get("STATES")

    if states and instance.instance_state.name != states.get(
        "PENDING_ADDITIONAL_DEMANDS"
    ):
        camac_user = User.objects.get(username=user.username)

        instance.set_instance_state(
            states["PENDING_ADDITIONAL_DEMANDS"],
            camac_user,
        )


@on(post_complete_case, raise_exception=True)
@filter_by_workflow("WORKFLOW")
@transaction.atomic
def post_complete_additional_demand_workflow(
    sender, case, user, context=None, **kwargs
):
    complete_work_item(work_item=case.parent_work_item, user=user, context=context)


@on(post_complete_work_item, raise_exception=True)
@filter_by_task("CHECK_TASK")
@transaction.atomic
def post_complete_check_additional_demand(
    sender, work_item, user, context=None, **kwargs
):
    decision = work_item.document.answers.get(
        question_id=settings.ADDITIONAL_DEMAND["QUESTIONS"]["DECISION"]
    ).value
    decision_key = next(
        (
            key
            for key, value in settings.ADDITIONAL_DEMAND["ANSWERS"]["DECISION"].items()
            if value == decision
        ),
        None,
    )
    decision_is_positive = (
        decision == settings.ADDITIONAL_DEMAND["ANSWERS"]["DECISION"]["ACCEPTED"]
    )

    instance = get_instance(work_item)
    has_pending_checks = _has_pending_work_items(
        work_item, settings.ADDITIONAL_DEMAND["CHECK_TASK"]
    )

    for config in settings.ADDITIONAL_DEMAND["NOTIFICATIONS"].get(decision_key, []):
        send_mail_without_request(
            config["template_slug"],
            user.username,
            user.camac_group,
            recipient_types=config["recipient_types"],
            instance={"id": instance.pk, "type": "instances"},
            work_item={"id": work_item.pk, "type": "work-items"},
        )

    if history_entry := settings.ADDITIONAL_DEMAND["HISTORY_ENTRIES"].get(decision_key):
        create_history_entry(
            instance,
            User.objects.get(username=user.username),
            gettext_noop(history_entry),
        )

    if (
        settings.ADDITIONAL_DEMAND.get("STATES")
        and not has_pending_checks
        and decision_is_positive
    ):
        camac_user = User.objects.get(username=user.username)

        instance.set_instance_state(
            instance.previous_instance_state.name,
            camac_user,
        )

    if settings.APPLICATION_NAME == "kt_uri":
        # if the "init-distribution" work item has been suspended
        # because of the "Vollständigkeitsprüfung" we need to resume it
        if decision_is_positive and not has_pending_checks:
            if suspended_distribution_work_item := WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                case__family=instance.case,
                status=WorkItem.STATUS_SUSPENDED,
            ).first():
                workflow_api.resume_work_item(
                    work_item=suspended_distribution_work_item, user=user
                )


@on(post_cancel_work_item, raise_exception=True)
@filter_by_task("TASK")
@transaction.atomic
def post_cancel_additional_demand(sender, work_item, user, context=None, **kwargs):
    if settings.APPLICATION_NAME != "kt_uri":  # pragma: no cover
        return

    has_pending_additional_demands = _has_pending_work_items(
        work_item, settings.ADDITIONAL_DEMAND["TASK"]
    )

    if not has_pending_additional_demands:
        instance = get_instance(work_item)
        camac_user = User.objects.get(username=user.username)
        instance.set_instance_state(
            instance.previous_instance_state.name,
            camac_user,
        )


@on(post_complete_work_item, raise_exception=True)
@filter_by_task("FILL_TASK")
@transaction.atomic
def post_complete_fill_additional_demand_file_subsequently(
    sender, work_item, user, context=None, **kwargs
):
    """Send the file_subsequently signal when the fill task is completed."""
    if settings.ECH0211.get("API_LEVEL") == "full":
        camac_user = User.objects.get(username=user.username)
        file_subsequently.send(
            sender="post_complete_additional_demand_file_subsequently",
            instance=work_item.case.family.instance,
            user_pk=camac_user.pk,
            group_pk=user.camac_group,
            inquiry=work_item,
        )


@on(post_create_work_item, raise_exception=True)
@filter_by_task("CHECK_TASK")
@transaction.atomic
def post_create_check_additional_demand(
    sender, work_item, user, context=None, **kwargs
):
    """Autocomplete the check task when created through eCH0211.

    If the "fill-additional-demand" was created through eCH0211, immediately set the
    decision to "unknown" when the check task is created because the eCH-0211 V2 API
    spec doesn't cover the act of "checking an additional demand".
    """
    # ignore if the eCH0211 claim is not enabled
    if settings.ECH0211.get("API_LEVEL") != "full" or not settings.ECH0211.get(
        "CLAIM", {}
    ).get("ENABLED", False):
        return

    decision_unknown = settings.ADDITIONAL_DEMAND["ANSWERS"]["DECISION"].get(
        "UNKNOWN", None
    )
    if not decision_unknown:
        raise Exception(
            "The decision `UNKNOWN` value is not set in the settings. "
            "Please check the settings for ADDITIONAL_DEMAND."
        )

    fill_additional_demand = (
        work_item.case.work_items.filter(
            task_id=settings.ADDITIONAL_DEMAND["FILL_TASK"],
            status=WorkItem.STATUS_COMPLETED,
        )
        .order_by("-created_at")
        .first()
    )

    if fill_additional_demand.meta.get("ech-init-workitem"):
        # save the check task `additional-demand-ech0211` answer as "true".
        # this will be used in JEXL evaluation to show/hide fields.
        save_answer(
            document=work_item.document,
            question=Question.objects.get(slug="additional-demand-ech0211"),
            value="true",
        )

        # automatically set the decision to "unknown" and complete the work item
        form_api.save_answer(
            document=work_item.document,
            question=Question.objects.get(
                pk=settings.ADDITIONAL_DEMAND["QUESTIONS"]["DECISION"]
            ),
            value=decision_unknown,
        )
        workflow_api.complete_work_item(
            work_item=work_item,
            user=user,
            context=context,
        )
