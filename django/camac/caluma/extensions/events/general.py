from logging import getLogger

from caluma.caluma_core.events import on
from caluma.caluma_form import models as caluma_form_models
from caluma.caluma_form.jexl import QuestionJexl
from caluma.caluma_form.structure import FieldSet
from caluma.caluma_workflow import api as workflow_api
from caluma.caluma_workflow.events import (
    post_complete_work_item,
    post_create_work_item,
    pre_complete_work_item,
    pre_skip_work_item,
)
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings
from django.db import transaction

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance
from camac.notification.utils import send_mail_without_request
from camac.user import models as user_models

log = getLogger()


def get_caluma_setting(key, default=None):
    return settings.APPLICATION.get("CALUMA", {}).get(key, default)


def get_instance_id(work_item, context=None):
    # When starting a new case, the foreign key relationship instance.case
    # and case.instance is only instantiated afterwards
    family = work_item.case.family
    if hasattr(family, "instance"):
        return family.instance.pk

    if context:
        return context.get("instance")

    return None  # pragma: no cover


def get_instance(work_item, context=None):
    return Instance.objects.get(pk=get_instance_id(work_item, context))


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
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


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def copy_tank_installation(sender, work_item, **kwargs):
    target_document = work_item.document
    for config in get_caluma_setting("COPY_TANK_INSTALLATION", []):
        if work_item.task_id == config["TASK"]:
            source_document = config["DOCUMENT"](work_item)
            structure = FieldSet(
                source_document,
                source_document.form,
            )
            qj = QuestionJexl(
                {
                    "document": source_document,
                    "form": source_document.form,
                    "structure": structure,
                }
            )
            table_field = structure.get_field("lagerung-von-stoffen-v2")
            if not table_field:
                return

            for row in table_field.children():
                field = row.get_field("bewilligungspflichtig-v2")
                hidden = qj.is_hidden(field)
                if work_item.task_id == config["TASK"] and hidden:
                    new_row = CalumaApi().copy_document(
                        row.document.pk, family=target_document.family
                    )
                    target_table, _ = target_document.answers.get_or_create(
                        question_id=config["TARGET"]
                    )
                    target_table.documents.add(new_row)


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def copy_paper_answer(sender, work_item, **kwargs):
    if (
        work_item.task_id in get_caluma_setting("COPY_PAPER_ANSWER_TO", [])
        and work_item.document
        and work_item.case.document
    ):
        # copy answer to the is-paper question in the case document to the
        # newly created work item document
        try:
            work_item.document.answers.update_or_create(
                question_id="is-paper",
                defaults={
                    "value": work_item.case.document.answers.get(
                        question_id="is-paper"
                    ).value
                },
            )
        except caluma_form_models.Answer.DoesNotExist:
            log.warning(
                f"Could not find answer for question `is-paper` in document for instance {get_instance_id(work_item)}"
            )


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_meta_attributes(sender, work_item, user, context, **kwargs):
    """Set needed meta attributes on the newly created work item."""

    META_DEFAULTS = {
        "not-viewed": True,
        "notify-completed": False,
        "notify-deadline": True,
    }

    work_item.meta = {**META_DEFAULTS, **work_item.meta}
    work_item.save()


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
def set_assigned_user(sender, work_item, user, **kwargs):
    addressed_group = next(
        (
            int(group)
            for group in work_item.addressed_groups
            if isinstance(group, int) or (isinstance(group, str) and group.isdigit())
        ),
        None,
    )

    if len(work_item.assigned_users) or not addressed_group:
        return

    instance = get_instance(work_item, context=kwargs.get("context"))
    service = user_models.Service.objects.get(pk=addressed_group)

    responsible = instance.responsible_services.filter(service=service).values_list(
        "responsible_user__username", flat=True
    )

    work_item.assigned_users = list(responsible)
    work_item.save()


@on(post_complete_work_item, raise_exception=True)
def notify_completed_work_item(sender, work_item, user, **kwargs):
    if not work_item.meta.get("notify-completed", False):
        return

    for notification_config in settings.APPLICATION["NOTIFICATIONS"].get(
        "COMPLETE_MANUAL_WORK_ITEM", []
    ):
        send_mail_without_request(
            notification_config["template_slug"],
            user.username,
            user.camac_group,
            instance={
                "id": work_item.case.family.instance.pk,
                "type": "instances",
            },
            work_item={"id": work_item.pk, "type": "work-items"},
            recipient_types=notification_config["recipient_types"],
        )


@on([pre_complete_work_item, pre_skip_work_item], raise_exception=True)
@transaction.atomic
def mark_as_read(work_item, **kwargs):
    # Completed and skipped work items should always be marked as read
    work_item.meta["not-viewed"] = False
    work_item.save()


@on(pre_complete_work_item, raise_exception=True)
@transaction.atomic
def handle_pre_complete_work_item(sender, work_item, user, **kwargs):
    config = get_caluma_setting("PRE_COMPLETE", {}).get(work_item.task_id)

    if config:
        for action_name, tasks in config.items():
            action = getattr(workflow_api, f"{action_name}_work_item")

            for item in work_item.case.work_items.filter(
                task_id__in=tasks, status=WorkItem.STATUS_READY
            ):
                action(item, user)


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
def set_is_published(sender, work_item, user, **kwargs):
    if work_item.task_id in [
        get_caluma_setting("FILL_PUBLICATION_TASK"),
        get_caluma_setting("INFORMATION_OF_NEIGHBORS_TASK"),
    ]:
        work_item.meta["is-published"] = True
        work_item.save()
