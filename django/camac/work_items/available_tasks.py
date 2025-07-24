import locale
from typing import TypedDict

from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.db.models import (
    F,
    Func,
    OuterRef,
    QuerySet,
    Subquery,
    UUIDField,
)
from django.db.models.fields.json import KeyTextTransform
from django.db.models.functions import Cast

from camac.user.models import Group
from camac.user.permissions import get_role_name
from camac.work_items.models import WorkItemListFilterPreset, WorkItemTemplate


class WorkItemListTaskOption(TypedDict):
    id: str
    label: str
    count: int


def get_task_options(
    group: Group,
    work_items: QuerySet[WorkItem],
    preset: WorkItemListFilterPreset | None,
) -> list[WorkItemListTaskOption]:
    """Get available task options from configuration (default, per role and per service group).

    The count of available work items for each returned option will be
    calculated in a subquery but will be omitted if
    `available_tasks_include_count` is not enabled.
    """

    role = get_role_name(group)
    service_group = group.service.service_group.name

    task_slugs = [
        *settings.WORK_ITEM_LIST.available_tasks_default,
        *settings.WORK_ITEM_LIST.available_tasks_for_role.get(role, []),
        *settings.WORK_ITEM_LIST.available_tasks_for_service_group.get(
            service_group, []
        ),
    ]

    tasks = Task.objects.filter(pk__in=task_slugs).only("pk", "name")

    if settings.WORK_ITEM_LIST.available_tasks_include_count:
        tasks = tasks.annotate(
            count=Subquery(
                work_items.filter(task_id=OuterRef("pk"))
                .annotate(count=Func(F("id"), function="Count"))
                .values("count")
            )
        )

    if preset and preset.prefilter_tasks:
        tasks = tasks.filter(pk__in=preset.tasks.all())

    return [
        {
            "id": task.pk,
            "label": str(task.name),
            "count": getattr(task, "count", None),
        }
        for task in tasks
    ]


def get_template_options(
    group: Group,
    work_items: QuerySet[WorkItem],
    preset: WorkItemListFilterPreset | None,
) -> list[WorkItemListTaskOption]:
    """Get available task options from work item templates.

    The count of available work items for each returned option will be
    calculated in a subquery but will be omitted if
    `available_tasks_include_count` is not enabled.

    This will only return data if `available_tasks_include_templates` is enabled
    in the module settings.
    """

    if not settings.WORK_ITEM_LIST.available_tasks_include_templates:
        return []

    templates = WorkItemTemplate.objects.for_service(group.service).only("pk", "name")

    if settings.WORK_ITEM_LIST.available_tasks_include_count:
        templates = templates.annotate(
            count=Subquery(
                work_items.annotate(
                    template_id=Cast(
                        KeyTextTransform("template-id", "meta"),
                        output_field=UUIDField(),
                    ),
                )
                .filter(template_id=OuterRef("pk"))
                .annotate(count=Func(F("id"), function="Count"))
                .values("count")
            )
        )

    if preset and preset.prefilter_work_item_templates:
        templates = templates.filter(pk__in=preset.work_item_templates.all())

    return [
        {
            "id": template.pk,
            "label": str(template.name),
            "count": getattr(template, "count", None),
        }
        for template in templates
    ]


def get_options(
    group: Group,
    work_items: QuerySet[WorkItem],
    preset_id=None,
) -> list[WorkItemListTaskOption]:
    """Get all options for the task filter of the work item list."""

    preset = (
        WorkItemListFilterPreset.objects.prefetch_related(
            "tasks", "work_item_templates"
        ).get(pk=preset_id)
        if preset_id
        else None
    )

    return sorted(
        [
            *get_task_options(group, work_items, preset),
            *get_template_options(group, work_items, preset),
        ],
        key=lambda option: locale.strxfrm(option["label"]),
    )
