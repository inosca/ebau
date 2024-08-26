from caluma.caluma_core.events import on
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.api import complete_work_item, start_case
from caluma.caluma_workflow.events import (
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


def _has_pending_checks(work_item):
    return WorkItem.objects.filter(
        task_id=settings.ADDITIONAL_DEMAND["CHECK_TASK"],
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

    instance = get_instance(work_item)
    has_pending_checks = _has_pending_checks(work_item)

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

    if settings.ADDITIONAL_DEMAND.get("STATES") and not has_pending_checks:
        camac_user = User.objects.get(username=user.username)

        instance.set_instance_state(
            settings.ADDITIONAL_DEMAND["STATES"]["AFTER_ADDITIONAL_DEMANDS"],
            camac_user,
        )

    if settings.APPLICATION_NAME == "kt_uri":
        # if the "init-distribution" work item has been suspended
        # because of the "Vollständigkeitsprüfung" we need to resume it
        if (
            decision == settings.ADDITIONAL_DEMAND["ANSWERS"]["DECISION"]["ACCEPTED"]
            and not has_pending_checks
        ):
            if suspended_distribution_work_item := WorkItem.objects.filter(
                task_id=settings.DISTRIBUTION["DISTRIBUTION_INIT_TASK"],
                case__family=instance.case,
                status=WorkItem.STATUS_SUSPENDED,
            ).first():
                workflow_api.resume_work_item(
                    work_item=suspended_distribution_work_item, user=user
                )
