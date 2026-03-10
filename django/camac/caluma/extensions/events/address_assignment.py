from caluma.caluma_core.events import filter_events, on
from caluma.caluma_workflow.events import post_complete_work_item, post_create_work_item
from django.conf import settings
from django.db import transaction

from camac.instance import domain_logic


@on(post_create_work_item, raise_exception=True)
@transaction.atomic
@filter_events(
    lambda work_item: (
        settings.ADDRESS_ASSIGNMENT.get("ENABLED", False)
        and work_item.task.slug == settings.ADDRESS_ASSIGNMENT.get("SUGGESTION_TASK")
    )
)
def prefill_street_answer(sender, work_item, user, context=None, **kwargs):
    domain_logic.AddressAssignmentLogic.prefill_street_answer(work_item, user)


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
    if domain_logic.AddressAssignmentLogic.address_check_was_positive(work_item):
        domain_logic.AddressAssignmentLogic.write_new_address_to_main_form(work_item)
        domain_logic.AddressAssignmentLogic.create_history_entry_for_address_change(
            work_item, user
        )
