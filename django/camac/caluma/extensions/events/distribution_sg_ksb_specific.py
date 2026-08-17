from caluma.caluma_core.events import on
from caluma.caluma_workflow.events import post_create_work_item, post_resume_work_item
from caluma.caluma_workflow.models import WorkItem
from django.conf import settings

from camac.caluma.event_utils import filter_by_canton, filter_by_task, setting
from camac.user.models import Service

# Those properties are explicitly written in camelCase in order to be easily
# accessible in JEXL expressions.
# While the JEXL evaluation with dasherized properties (e.g.
# `info.workItem.meta["created-by-ksb"]`) actually works, the validator in the
# form-builder fails.
# With camelized properties (e.g. `info.workItem.meta.createdByKsb`) we don't
# have any issues and it looks a bit cleaner.
META_CREATED_BY_KSB_KEY = "createdByKsb"
META_FIRST_WEEK_KEY = "isFirstWeek"


@on(post_create_work_item, raise_exception=True)
@filter_by_canton("kt_sg")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
def mark_inquiry_as_created_by_ksb(_, work_item: WorkItem, *args, **kwargs):
    """Mark inquiries created by the KSB as such.

    This is needed in order to conditionally show a question in the inquiry
    request form which should only be visible if the KSB created that inquiry.

    This is part of the custom distinction between the first week distribution
    round ("Erste Woche") and the regular statement round ("Stellungnahmen")
    specifically for the KSB of Kt. SG.
    """

    is_created_by_ksb = Service.objects.filter(
        pk=work_item.controlling_groups[0],
        slug="coordination",
    ).exists()

    if not is_created_by_ksb:
        # Don't do anything if the inquiry is not created by the KSB
        return

    work_item.meta[META_CREATED_BY_KSB_KEY] = True
    work_item.save(update_fields=["meta"])


@on(post_resume_work_item, raise_exception=True)
@filter_by_canton("kt_sg")
@filter_by_task(setting("DISTRIBUTION", "INQUIRY_TASK"))
def mark_inquiry_as_first_week(_, work_item: WorkItem, *args, **kwargs):
    """Mark inquiries as first week if the KSB marked it as such.

    This is needed in order to conditionally show a different inquiry answer
    form if the inquiry is a first week inquiry. An inquiry is marked as first
    week if the KSB answered the inquiry type question with "first-week".

    This is part of the custom distinction between the first week distribution
    round ("Erste Woche") and the regular statement round ("Stellungnahmen")
    specifically for the KSB of Kt. SG.
    """

    if not work_item.meta.get(META_CREATED_BY_KSB_KEY):
        # If it's not an inquiry created by the KSB we don't even have to check
        # the inquiry type as this question was never shown.
        return

    is_first_week = work_item.document.answers.filter(
        question_id=settings.DISTRIBUTION["QUESTIONS"]["TYPE"],
        value=settings.DISTRIBUTION["ANSWERS"]["TYPE"]["FIRST_WEEK"],
    ).exists()

    if not is_first_week:
        # If the type is not of "first-week", we don't mark it
        return

    work_item.meta[META_FIRST_WEEK_KEY] = True
    work_item.save(update_fields=["meta"])
