from caluma.caluma_core.events import filter_events, on
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from django.conf import settings
from django.db import transaction
from django.utils.translation import gettext

from camac.caluma.extensions.events.general import get_instance
from camac.core.utils import create_history_entry
from camac.instance.master_data import MasterData
from camac.user.models import User


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: (
        settings.ADDRESS_ASSIGNMENT.get("ENABLED", False)
        and work_item.task.slug == settings.ADDRESS_ASSIGNMENT.get("SUGGESTION_TASK")
    )
)
def prefill_street_answer(sender, work_item, user, context=None, **kwargs):
    master_data = MasterData.from_case_id(work_item.case.pk)
    save_answer(
        document=work_item.document,
        question=Question.objects.get(
            slug=settings.ADDRESS_ASSIGNMENT["STREET_QUESTION_SLUG"]
        ),
        value=master_data.street,
        user=user,
    )


@on(post_complete_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: (
        settings.ADDRESS_ASSIGNMENT.get("ENABLED", False)
        and work_item.task.slug == settings.ADDRESS_ASSIGNMENT.get("CONFIRM_TASK")
    )
)
def address_assignment_write_street_to_main_form(
    sender, work_item, user, context=None, **kwargs
):
    """
    Write back the new street to main form if check was positive.

    If the checking service is happy with the suggested address we write it back to the main form
    and create a history entry.
    """
    master_data = MasterData.from_case_id(work_item.case.pk)
    answer_map = work_item.document.flat_answer_map()
    previous_suggest_work_item = (
        work_item.case.work_items.filter(
            task_id=settings.ADDRESS_ASSIGNMENT["SUGGESTION_TASK"]
        )
        .order_by("-created_at")
        .first()
    )
    new_street_value = previous_suggest_work_item.document.flat_answer_map().get(
        settings.ADDRESS_ASSIGNMENT["STREET_QUESTION_SLUG"]
    )
    old_street_value = master_data.street

    if (
        answer_map.get(settings.ADDRESS_ASSIGNMENT["ADDRESS_VALID_QUESTION_SLUG"])
        == settings.ADDRESS_ASSIGNMENT["ADDRESS_VALID_OPTION_SLUG"]
    ):
        save_answer(
            document=work_item.case.family.document,
            question=Question.objects.get(
                slug=settings.ADDRESS_ASSIGNMENT.get("MAIN_FORM_STREET_QUESTION_SLUG")
            ),
            value=new_street_value,
        )
        create_history_entry(
            instance=get_instance(work_item),
            user=User.objects.get(username=user.username),
            text=(
                gettext(
                    f"Address suggestion accepted and address updated in form from {old_street_value} to {new_street_value}"
                )
            ),
        )
