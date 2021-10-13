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
from django.core import mail
from django.db import transaction

from camac.caluma.api import CalumaApi
from camac.instance.models import Instance
from camac.user import models as user_models
from camac.user.utils import unpack_service_emails

log = getLogger()


def get_caluma_setting(key, default=None):
    return settings.APPLICATION.get("CALUMA", {}).get(key, default)


def get_instance_id(work_item):
    return work_item.case.family.instance.pk


def get_instance(work_item):
    return Instance.objects.get(pk=get_instance_id(work_item))


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
    """Set needed meta attributes on the newly created work item.

    Some attributes just need a default value if they don't exist yet in the
    meta of the work item. Others will be passed in the context.
    """

    META_CONFIG = {
        "not-viewed": {"default": True},
        "notify-completed": {"default": False},
        "notify-deadline": {"default": True},
        "circulation-id": {
            "from_context": True,
            "tasks": [get_caluma_setting("CIRCULATION_TASK")],
        },
        "activation-id": {
            "from_context": True,
            "tasks": get_caluma_setting("ACTIVATION_TASKS"),
        },
    }

    for attribute, config in META_CONFIG.items():
        tasks = config.get("tasks")
        from_context = config.get("from_context")

        if attribute in work_item.meta:
            # attribute is already set on the meta
            continue

        if tasks and work_item.task_id not in tasks:
            # incorrect task
            continue

        if from_context and (not context or not context.get(attribute)):
            # context does not contain attribute
            log.warning(
                f"Attribute `{attribute}` is not passed in the context: {context}"
            )
            continue

        work_item.meta[attribute] = (
            context.get(attribute) if from_context else config.get("default")
        )

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

    instance = get_instance(work_item)
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

    # controlling services are notified
    services = user_models.Service.objects.filter(
        pk__in=work_item.controlling_groups
    ).filter(notification=True)

    recipients = unpack_service_emails(services)

    camac_user = user_models.User.objects.filter(username=user.username).first()

    closed_by_service = user_models.Service.objects.filter(pk=user.group).first()
    service_info_de = (
        f" ({closed_by_service.get_name('de')})" if closed_by_service else ""
    )
    service_info_fr = (
        f" ({closed_by_service.get_name('fr')})" if closed_by_service else ""
    )

    instance_id = get_instance_id(work_item)

    dossier_identification = instance_id
    title = f"Aufgabe abgeschlossen (Dossier-Nr. {dossier_identification})"

    if settings.APPLICATION.get("HAS_EBAU_NUMBER", False) and settings.APPLICATION.get(
        "IS_MULTILINGUAL", False
    ):
        dossier_identification = (
            f"{work_item.case.family.meta.get('ebau-number')} ({instance_id})"
        )
        title = f"Aufgabe abgeschlossen (eBau-Nr. {dossier_identification}) / tâche complétée (n° eBau {dossier_identification})"

    body = f"""Guten Tag

Die Aufgabe "{work_item.name}" im Dossier {dossier_identification} wurde von {camac_user.get_full_name()}{service_info_de} abgeschlossen.

{settings.INTERNAL_INSTANCE_URL_TEMPLATE.format(instance_id=instance_id)}

Sie erhalten diese Notifikation, weil Sie beim Erstellen der Aufgabe die Notifikationseinstellung "Bei Abschluss" gewählt haben.
"""

    if settings.APPLICATION.get("IS_MULTILINGUAL", False):
        body = (
            body
            + f"""
*** version française ***

Bonjour,

La tâche "{work_item.name}" dans le dossier {dossier_identification} a été terminée par {camac_user.get_full_name()}{service_info_fr}.

{settings.INTERNAL_INSTANCE_URL_TEMPLATE.format(instance_id=instance_id)}

Vous recevez cette notification parce que vous avez sélectionné le paramètre de notification "après achèvement" lorsque vous avez créé la tâche.
"""
        )

    emails = [
        mail.EmailMessage(title, body, settings.DEFAULT_FROM_EMAIL, to=[rec])
        for rec in recipients
    ]

    connection = mail.get_connection()
    connection.send_messages(emails)


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
