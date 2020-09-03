from collections import namedtuple
from datetime import timedelta
from logging import getLogger

from caluma.caluma_user.models import BaseUser
from caluma.caluma_workflow import models as workflow_models
from caluma.caluma_workflow.utils import get_jexl_groups
from django.conf import settings
from django.db import migrations
from django.db.models import Count, F, OuterRef, Q, Subquery
from django.db.models.expressions import RawSQL
from django.utils import timezone

log = getLogger(__name__)


def suspend_case(models, case):
    models.Case.objects.filter(
        family=case, status=workflow_models.Case.STATUS_RUNNING
    ).update(status=workflow_models.Case.STATUS_SUSPENDED)

    models.WorkItem.objects.filter(
        case__family=case, status=workflow_models.WorkItem.STATUS_READY
    ).update(status=workflow_models.WorkItem.STATUS_SUSPENDED)


def cancel_case(models, case):
    models.Case.objects.filter(
        family=case, status=workflow_models.Case.STATUS_RUNNING
    ).update(status=workflow_models.Case.STATUS_CANCELED, closed_at=timezone.now())

    models.WorkItem.objects.filter(
        case__family=case, status=workflow_models.WorkItem.STATUS_READY
    ).update(status=workflow_models.WorkItem.STATUS_CANCELED, closed_at=timezone.now())


def complete_case(models, case):
    models.Case.objects.filter(
        family=case, status=workflow_models.Case.STATUS_RUNNING
    ).update(status=workflow_models.Case.STATUS_COMPLETED, closed_at=timezone.now())

    models.WorkItem.objects.filter(
        case__family=case, status=workflow_models.WorkItem.STATUS_READY
    ).update(status=workflow_models.WorkItem.STATUS_SKIPPED, closed_at=timezone.now())


def skip_task(case, task_slug):
    case.work_items.filter(task_id=task_slug).update(
        status=workflow_models.WorkItem.STATUS_SKIPPED, closed_at=timezone.now()
    )


def sync_work_item_names(models):
    models.WorkItem.objects.update(
        name=Subquery(
            models.Task.objects.filter(pk=OuterRef("task_id")).values_list("name")[:1]
        )
    )


def mark_all_work_items_unread(models):
    models.WorkItem.objects.filter(status=workflow_models.WorkItem.STATUS_READY).update(
        meta=RawSQL("""jsonb_set(meta, '{"not-viewed"}', 'true', true)""", [])
    )


def set_ebau_number_deadlines(models):
    task = models.Task.objects.get(pk="ebau-number")

    models.WorkItem.objects.filter(task_id=task.pk).update(
        deadline=timezone.now() + timedelta(seconds=task.lead_time)
    )


def create_work_item_from_task(
    models, case, task_slug, meta={}, child_case=None, context={}, deadline=None
):
    task = models.Task.objects.get(pk=task_slug)

    meta = {
        "migrated": True,
        "not-viewed": True,
        "notify-deadline": True,
        "notify-completed": True,
        **meta,
    }

    deadline = (
        deadline
        or task.lead_time
        and (timezone.now() + timedelta(seconds=task.lead_time))
    )

    return models.WorkItem.objects.create(
        case=case,
        task=task,
        meta=meta,
        name=task.name,
        status=workflow_models.WorkItem.STATUS_READY,
        child_case=child_case,
        deadline=deadline,
        addressed_groups=get_jexl_groups(
            task.address_groups, task, case, BaseUser(), None, context
        ),
        controlling_groups=get_jexl_groups(
            task.control_groups, task, case, BaseUser(), None, context
        ),
    )


def migrate_circulation(models, instance, case):
    circulations = instance.circulations.annotate(
        activation_count=Count("activations")
    ).filter(Q(activation_count=0) | Q(activations__circulation_state__name="RUN"))

    if not circulations.exists():
        # circulation is over
        create_work_item_from_task(models, case, "start-circulation")
        create_work_item_from_task(models, case, "start-decision")

        return

    for circulation in circulations.filter(activation_count__gt=0):
        # create one work item with a child case per running circulation
        activation_document = models.Document.objects.create(
            form=models.Form.objects.get(pk="circulation")
        )
        child_case = models.Case.objects.create(
            workflow=models.Workflow.objects.get(pk="circulation"),
            status=workflow_models.Case.STATUS_RUNNING,
            meta={"migrated": True},
            document=activation_document,
            family=case,
        )

        create_work_item_from_task(
            models,
            case,
            "circulation",
            meta={"circulation-id": circulation.pk},
            child_case=child_case,
        )

        for activation in circulation.activations.all():
            context_and_meta = {"activation-id": activation.pk}
            work_item = create_work_item_from_task(
                models,
                child_case,
                "activation",
                meta=context_and_meta,
                context=context_and_meta,
                deadline=activation.deadline_date,
            )

            if activation.circulation_state.name == "DONE":
                work_item.status = workflow_models.WorkItem.STATUS_SKIPPED
                work_item.closed_at = timezone.now()
                work_item.save()


def migrate(apps, schema_editor):
    if settings.APPLICATION_NAME != "kt_bern":
        log.warn(f"Migration won't be run for application {settings.APPLICATION_NAME}")
        return

    models = namedtuple(
        "models",
        [
            "Publication",
            "Instance",
            "Case",
            "WorkItem",
            "Workflow",
            "Task",
            "Document",
            "Form",
        ],
    )

    models.Publication = apps.get_model("core", "Publication")
    models.Instance = apps.get_model("instance", "Instance")
    models.Case = apps.get_model("caluma_workflow", "Case")
    models.WorkItem = apps.get_model("caluma_workflow", "WorkItem")
    models.Workflow = apps.get_model("caluma_workflow", "Workflow")
    models.Task = apps.get_model("caluma_workflow", "Task")
    models.Document = apps.get_model("caluma_form", "Document")
    models.Form = apps.get_model("caluma_form", "Form")

    _failed_instances = []
    instances = models.Instance.objects.all()

    if not instances.exists():
        return

    sync_work_item_names(models)
    set_ebau_number_deadlines(models)
    mark_all_work_items_unread(models)

    for instance in instances:
        try:
            case = models.Case.objects.get(**{"meta__camac-instance-id": instance.pk})
        except models.Case.DoesNotExist:
            _failed_instances.append(instance.pk)
            log.error(
                f"No Caluma case found for instance {instance.pk} - skipping migration"
            )
            continue

        instance_state = instance.instance_state

        if (
            instance_state.name
            in [
                "audit",
                "correction",
                "circulation_init",
                "circulation",
                "coordination",
            ]
            and not models.Publication.objects.filter(instance=instance.pk).exists()
        ):
            create_work_item_from_task(models, case, "publication")

        if instance_state.name not in ["new", "evaluated", "finished", "archived"]:
            create_work_item_from_task(models, case, "create-manual-workitems")

        if instance_state.name != "subm":
            skip_task(case, "ebau-number")

        if instance_state.name == "audit":
            create_work_item_from_task(models, case, "audit")
            create_work_item_from_task(models, case, "init-circulation")
        elif instance_state.name == "circulation_init":
            create_work_item_from_task(models, case, "init-circulation")
        elif instance_state.name == "circulation":
            migrate_circulation(models, instance, case)
        elif instance_state.name == "coordination":
            create_work_item_from_task(models, case, "decision")
            create_work_item_from_task(models, case, "reopen-circulation")
        elif instance_state.name == "rejected":
            suspend_case(models, case)
        elif instance_state.name in ["evaluated", "finished"]:
            complete_case(models, case)
        elif instance_state.name == "archived":
            cancel_case(models, case)

    if len(_failed_instances):
        failed_ids = ", ".join(map(str, _failed_instances))

        log.warn(f"Failed to migrate the following instances: {failed_ids}")


class Migration(migrations.Migration):
    dependencies = [("instance", "0020_update_ebau_number_deadline")]
    operations = [migrations.RunPython(migrate, migrations.RunPython.noop)]
