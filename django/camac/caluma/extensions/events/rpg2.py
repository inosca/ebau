from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.events import post_resume_work_item
from caluma.caluma_workflow.models import Task, WorkItem
from django.conf import settings
from django.db import transaction

from camac.caluma.utils import is_addressed_to_service_slug
from camac.user.models import Service
from camac.utils import get_unversioned_slug


def is_rpg2_service_addressed(work_item):
    """Check that the addressed_groups of the work item contain the rpg2 services."""
    return is_addressed_to_service_slug(work_item, settings.RPG2.service_slugs)


def is_rpg2_relevant_form(work_item):
    """Check that the case's main form is in the configured RPG2 allowed_forms list."""
    forms = settings.RPG2.allowed_forms
    # allowed_forms setting needs to be configured, work item should not be created for non-configured forms.
    if not forms:
        return False
    return get_unversioned_slug(work_item.case.family.document.form_id) in forms


@on(post_resume_work_item, raise_exception=True)
@filter_events(lambda: settings.RPG2.enabled)
@filter_events(
    lambda work_item: work_item.task_id == settings.DISTRIBUTION["INQUIRY_TASK"]
)
@transaction.atomic
def post_resume_inquiry_for_rpg2(
    sender, work_item, user, context=None, **kwargs
):  # pragma: no cover
    # TODO: Add tests per canton when enabling

    if not is_rpg2_service_addressed(work_item):
        return

    if not is_rpg2_relevant_form(work_item):
        return

    # get the main case from the distribution child case
    case = work_item.case.family

    if case.work_items.filter(task_id=settings.RPG2.task).exists():
        return  # "rpg2" work-item already exists

    # Assume task exists (created per canton) when module is enabled.
    task = Task.objects.get(pk=settings.RPG2.task)
    # The rpg2 work_item is addressed to all cantonal services configured.
    group_pks = [
        str(pk)
        for pk in Service.objects.filter(
            slug__in=settings.RPG2.service_slugs,
        ).values_list("pk", flat=True)
    ]

    WorkItem.objects.create(
        task=task,
        name=task.name,
        addressed_groups=group_pks,
        case=case,
        status=WorkItem.STATUS_READY,
        document=Document.objects.create_document_for_task(task, None),
    )
