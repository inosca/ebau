from unittest.mock import Mock, patch

from caluma.caluma_form import (
    factories as caluma_form_factories,
    models as caluma_form_models,
)

from camac.caluma.extensions.events import address_assignment
from camac.tests.utils import Utils


def test_prefill_street_answer(
    db,
    set_application_gr,
    caluma_work_item_factory,
    caluma_admin_user,
    gr_address_assignment_settings,
    gr_instance,
    utils,
    mocker,
):
    gr_address_assignment_settings["ENABLED"] = True
    with patch(
        "camac.instance.master_data.MasterData.from_case_id",
        return_value=Mock(street="Teststreet 420"),
    ):
        work_item = caluma_work_item_factory(
            case=gr_instance.case,
            task_id=gr_address_assignment_settings["SUGGESTION_TASK"],
        )

        address_assignment.prefill_street_answer(
            sender=None, work_item=work_item, user=caluma_admin_user
        )

        street_prefilled = work_item.document.answers.get(
            question__slug=gr_address_assignment_settings["STREET_QUESTION_SLUG"]
        )
        assert street_prefilled.value == "Teststreet 420"


def test_address_assignment_write_street_to_main_form(
    db,
    gr_instance,
    utils: Utils,
    caluma_work_item_factory,
    gr_address_assignment_settings,
    caluma_admin_user,
):
    gr_address_assignment_settings["ENABLED"] = True
    suggestion_work_item = caluma_work_item_factory(
        case=gr_instance.case, task_id=gr_address_assignment_settings["SUGGESTION_TASK"]
    )
    utils.add_answer(
        suggestion_work_item.document,
        gr_address_assignment_settings["STREET_QUESTION_SLUG"],
        "New street",
    )
    confirm_task_work_item = caluma_work_item_factory(
        case=gr_instance.case, task_id=gr_address_assignment_settings["CONFIRM_TASK"]
    )
    utils.add_answer(
        confirm_task_work_item.document,
        gr_address_assignment_settings["ADDRESS_VALID_QUESTION_SLUG"],
        gr_address_assignment_settings["ADDRESS_VALID_OPTION_SLUG"],
    )
    valid_question = caluma_form_factories.QuestionFactory(
        slug=gr_address_assignment_settings["MAIN_FORM_STREET_QUESTION_SLUG"],
        type=caluma_form_models.Question.TYPE_TEXT,
    )
    caluma_form_factories.FormQuestionFactory(
        form=confirm_task_work_item.document.form, question=valid_question
    )
    address_assignment.address_assignment_write_street_to_main_form(
        sender=None, work_item=confirm_task_work_item, user=caluma_admin_user
    )

    assert (
        gr_instance.case.document.answers.get(
            question_id=gr_address_assignment_settings["MAIN_FORM_STREET_QUESTION_SLUG"]
        ).value
        == "New street"
    )
