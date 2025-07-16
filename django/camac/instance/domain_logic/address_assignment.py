from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.models import Case, WorkItem
from django.conf import settings
from django.utils.translation import gettext_noop

from camac.caluma.utils import get_answer
from camac.core.utils import create_history_entry
from camac.instance.master_data import MasterData
from camac.user.models import User


class AddressAssignmentLogic:
    @classmethod
    def requires_address_assignment(cls, case: Case):
        exam_document = case.family.work_items.get(
            task_id=settings.ADDRESS_ASSIGNMENT["EXAM_TASK"]
        ).document

        answer_value = get_answer(
            settings.ADDRESS_ASSIGNMENT["REQUIRES_NEW_ADDRESS_QUESTION_SLUG"],
            exam_document,
        )
        return (
            answer_value
            == settings.ADDRESS_ASSIGNMENT["REQUIRES_NEW_ADDRESS_QUESTION_TRUE"]
        )

    @classmethod
    def address_check_was_positive(cls, work_item: WorkItem):
        check_document = work_item.document
        answer_value = get_answer(
            settings.ADDRESS_ASSIGNMENT["ADDRESS_VALID_QUESTION_SLUG"], check_document
        )

        return answer_value == settings.ADDRESS_ASSIGNMENT["ADDRESS_VALID_OPTION_SLUG"]

    @classmethod
    def latest_suggest_address_work_item(cls, case: Case):
        return (
            case.work_items.filter(
                task_id=settings.ADDRESS_ASSIGNMENT["SUGGESTION_TASK"]
            )
            .order_by("-created_at")
            .first()
        )

    @classmethod
    def most_recent_address_suggestions(cls, case: Case):
        latest_suggest_address_work_item = cls.latest_suggest_address_work_item(case)
        return get_answer(
            settings.ADDRESS_ASSIGNMENT["STREET_QUESTION_SLUG"],
            latest_suggest_address_work_item.document,
        )

    @classmethod
    def write_new_address_to_main_form(cls, work_item: WorkItem):
        new_street_value = cls.most_recent_address_suggestions(work_item.case)
        save_answer(
            document=work_item.case.family.document,
            question=Question.objects.get(
                slug=settings.ADDRESS_ASSIGNMENT.get("MAIN_FORM_STREET_QUESTION_SLUG")
            ),
            value=new_street_value,
        )

    @classmethod
    def create_history_entry_for_address_change(cls, work_item: WorkItem, user: User):
        new_street_value = cls.most_recent_address_suggestions(work_item.case)

        master_data = MasterData.from_case_id(work_item.case.pk)

        create_history_entry(
            intance=work_item.case.family.instance,
            user=User.objects.get(username=user.username),
            text=(
                gettext_noop(
                    f"Address suggestion accepted and address updated in form from {master_data.street} to {new_street_value}"
                )
            ),
        )
