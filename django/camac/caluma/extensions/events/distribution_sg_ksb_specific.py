from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_resume_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.event_utils import filter_by_canton, filter_by_task, setting

# This property is explicitly written in camelCase in order to be easily
# accessible in JEXL expressions.
# While the JEXL evaluation with dasherized properties (e.g.
# `info.workItem.meta["is-first-week"]`) actually works, the validator in the
# form-builder fails.
# With camelized properties (e.g. `info.workItem.meta.isFirstWeek`) we don't
# have any issues and it looks a bit cleaner.
META_FIRST_WEEK_KEY = "isFirstWeek"


@on(post_resume_work_item, raise_exception=True)
@filter_by_canton("kt_sg")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
def mark_inquiry_as_first_week(_, work_item: WorkItem, *args, **kwargs):
    """Mark inquiries as first week if they were marked as such.

    This is needed in order to conditionally show a different inquiry answer
    form if the inquiry is a first week inquiry. An inquiry is marked as first
    week if the inquiry type question was answered with "first-week".

    This is part of the custom distinction between the first week distribution
    round ("Erste Woche") and the regular statement round ("Stellungnahmen")
    specifically for the KSB of Kt. SG.
    """

    is_first_week = work_item.document.answers.filter(
        question_id=settings.DISTRIBUTION["QUESTIONS"]["TYPE"],
        value=settings.DISTRIBUTION["ANSWERS"]["TYPE"]["FIRST_WEEK"],
    ).exists()

    if not is_first_week:
        # If the type is not of "first-week", we don't mark it
        return

    work_item.meta[META_FIRST_WEEK_KEY] = True
    work_item.save(update_fields=["meta"])
