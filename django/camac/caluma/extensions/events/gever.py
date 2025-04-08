from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.models import Document
from caluma.caluma_workflow.events import (
    post_resume_work_item,
)
from caluma.caluma_workflow.models import Task, WorkItem
from django.db import transaction

from camac.caluma.api import CalumaApi


@on(post_resume_work_item, raise_exception=True)
@filter_events(lambda work_item: work_item.task_id == "inquiry")
@transaction.atomic
def post_resume_inquiry_for_gever(sender, work_item, user, context=None, **kwargs):
    case = work_item.case.family

    if case.work_items.filter(
        task_id="gever",
        status=WorkItem.STATUS_READY,
    ).exists():
        return  # "gever" work-item already exists

    task = Task.objects.get(pk="gever")

    gever_work_item = WorkItem.objects.create(
        task=task,
        name=task.name,
        addressed_groups=["20032"],
        case=case,
        status=WorkItem.STATUS_READY,
        document=Document.objects.create_document_for_task(task, None),
    )

    # fill work-item with instance data
    instance = case.instance
    rows = CalumaApi().get_table_answer("parzelle", instance)
    if rows:
        numbers = [row.answers.get(question_id="nummer-parzelle").value for row in rows]
        parcels = ", ".join([str(n) for n in numbers if n is not None])

        row = rows.first()
        x = row.answers.get(question_id="lagekoordinaten-ost").value
        y = row.answers.get(question_id="lagekoordinaten-nord").value

        # assign values to document answers
        document = gever_work_item.document
        CalumaApi().update_or_create_answer(
            document, "agr-titel", str(instance.pk), None
        )
        CalumaApi().update_or_create_answer(document, "agr-parzellen", parcels, None)
        CalumaApi().update_or_create_answer(document, "agr-koordinate-ost", x, None)
        CalumaApi().update_or_create_answer(document, "agr-koordinate-nord", y, None)

    return
