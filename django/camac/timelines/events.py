from caluma.caluma_core.events import on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.events import (
    post_cancel_work_item,
    post_complete_work_item,
    post_create_work_item,
)
from django.conf import settings
from django.db import transaction

from camac.caluma.extensions.events.additional_demand import (
    get_additional_demand_settings,
)
from camac.caluma.utils import filter_events
from camac.timelines.models import FormTimeline


def filter_additional_demand_event(settings_keys):
    """Check for additional demand settings key.

    If the timelines module is not enabled, ignore all these events.
    """
    return filter_events(
        lambda work_item: (
            settings.TIMELINES.enabled
            and work_item.task_id in get_additional_demand_settings(settings_keys)
        )
    )


@on(post_complete_work_item, raise_exception=True)
@filter_additional_demand_event("FILL_TASK")
@transaction.atomic
def post_complete_fill_additional_demand_form_timelines(
    sender, work_item, user, context=None, **kwargs
):
    """Close additional demand formtimeline when the applicant has answered."""
    additional_demand = work_item.case.parent_work_item
    if additional_demand:
        FormTimeline.objects.close_additional_demand(additional_demand)


@on(post_complete_work_item, raise_exception=True)
@filter_additional_demand_event(["SEND_TASK", "CHECK_TASK"])
@transaction.atomic
def post_complete_send_check_additional_demand_allow_changes(
    sender, work_item, user, context=None, **kwargs
):
    """Set meta flag to allow changes on the additional demand form.

    When the extra checkbox to allow form changes has been checked, store this
    information in the additional demand work item's meta data.
    """
    allow_changes_answer = work_item.document.answers.filter(
        question_id="additional-demand-allow-changes"
    ).first()
    allow_changes = "additional-demand-allow-changes" in (
        allow_changes_answer.value if allow_changes_answer else []
    )
    additional_demand = work_item.case.parent_work_item

    if allow_changes and additional_demand:
        additional_demand.meta["allow-form-changes"] = True
        additional_demand.save(update_fields=["meta"])

        FormTimeline.objects.open_additional_demand(additional_demand)


@on(post_cancel_work_item, raise_exception=True)
@filter_additional_demand_event("TASK")
@transaction.atomic
def post_cancel_additional_demand_allow_changes(
    sender, work_item, user, context=None, **kwargs
):
    """Close the formtimeline when the additional demand is cancelled."""
    FormTimeline.objects.close_additional_demand(work_item)


@on(post_create_work_item, raise_exception=True)
@filter_additional_demand_event("FILL_TASK")
@transaction.atomic
def post_create_fill_additional_demand_formtimeline(
    sender, work_item, user, context=None, **kwargs
):
    """Fill the formtimeline case relation when the fill task is created."""
    instance = work_item.case.family.instance
    form_timeline_question = Question.objects.get(slug="additional-demand-formtimeline")
    additional_demand = work_item.case.parent_work_item
    allow_form_changes = (
        additional_demand.meta.get("allow-form-changes") if additional_demand else False
    )

    if allow_form_changes:
        form_timeline = (
            FormTimeline.objects.get_queryset()
            .for_instance(instance)
            .only_open()
            .filter(
                timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND,
            )
            .first()
        )
        if form_timeline:
            save_answer(
                document=work_item.document,
                question=form_timeline_question,
                value=str(form_timeline.pk),
            )
