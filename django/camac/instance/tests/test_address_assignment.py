from caluma.caluma_form.models import Question

from camac.instance.domain_logic import AddressAssignmentLogic
from camac.permissions.config.kt_gr import PermissionEventHandlerGR
from camac.user.models import ServiceRelation


def test_requires_address_assignment(
    db,
    gr_instance,
    caluma_work_item_factory,
    caluma_answer_factory,
    gr_address_assignment_settings,
    caluma_document_factory,
    set_application_gr,
):
    gr_address_assignment_settings["ENABLED"] = True
    exam_work_item = caluma_work_item_factory(
        case=gr_instance.case,
        task_id=gr_address_assignment_settings["EXAM_TASK"],
        document=caluma_document_factory(),
    )
    caluma_answer_factory(
        question__slug=gr_address_assignment_settings[
            "REQUIRES_NEW_ADDRESS_QUESTION_SLUG"
        ],
        value=gr_address_assignment_settings["REQUIRES_NEW_ADDRESS_QUESTION_TRUE"],
        document=exam_work_item.document,
    )

    assert AddressAssignmentLogic.requires_address_assignment(gr_instance.case)


def test_address_check_was_positive(
    db,
    gr_instance,
    caluma_work_item_factory,
    caluma_answer_factory,
    gr_address_assignment_settings,
    caluma_document_factory,
):
    check_item = caluma_work_item_factory(
        case=gr_instance.case,
        document=caluma_document_factory(),
    )
    caluma_answer_factory(
        question_id=gr_address_assignment_settings["ADDRESS_VALID_QUESTION_SLUG"],
        value=gr_address_assignment_settings["ADDRESS_VALID_OPTION_SLUG"],
        document=check_item.document,
    )
    assert AddressAssignmentLogic.address_check_was_positive(check_item)


def test_latest_suggest_address_work_item(
    db,
    gr_instance,
    caluma_work_item_factory,
    caluma_answer_factory,
    gr_address_assignment_settings,
    caluma_document_factory,
):
    caluma_work_item_factory(
        task_id=gr_address_assignment_settings["SUGGESTION_TASK"], case=gr_instance.case
    )
    newer = caluma_work_item_factory(
        task_id=gr_address_assignment_settings["SUGGESTION_TASK"], case=gr_instance.case
    )

    assert (
        AddressAssignmentLogic.latest_suggest_address_work_item(gr_instance.case).pk
        == newer.pk
    )


def test_most_recent_address_suggestions(
    db,
    gr_instance,
    caluma_work_item_factory,
    caluma_answer_factory,
    gr_address_assignment_settings,
    caluma_document_factory,
):
    work_item = caluma_work_item_factory(
        task_id=gr_address_assignment_settings["SUGGESTION_TASK"], case=gr_instance.case
    )
    caluma_answer_factory(
        question_id=gr_address_assignment_settings["STREET_QUESTION_SLUG"],
        value="some-value",
        document=work_item.document,
    )

    assert (
        AddressAssignmentLogic.most_recent_address_suggestions(gr_instance.case)
        == "some-value"
    )


def test_write_new_address_to_main_form(
    db,
    gr_instance,
    caluma_work_item_factory,
    caluma_answer_factory,
    gr_address_assignment_settings,
    caluma_document_factory,
):
    work_item = caluma_work_item_factory(
        task_id=gr_address_assignment_settings["SUGGESTION_TASK"], case=gr_instance.case
    )
    caluma_answer_factory(
        question_id=gr_address_assignment_settings["STREET_QUESTION_SLUG"],
        value="new street",
        document=work_item.document,
    )
    caluma_answer_factory(
        question__slug=gr_address_assignment_settings["MAIN_FORM_STREET_QUESTION_SLUG"],
        question__type=Question.TYPE_TEXT,
        value="old street",
        document=gr_instance.case.document,
    )
    AddressAssignmentLogic.write_new_address_to_main_form(work_item)

    assert (
        gr_instance.case.document.answers.get(
            question_id=gr_address_assignment_settings["MAIN_FORM_STREET_QUESTION_SLUG"]
        ).value
        == "new street"
    )


def test_create_history_entry_for_address_change(
    db,
    gr_instance,
    gr_address_assignment_settings,
    caluma_work_item_factory,
    mocker,
    admin_user,
):
    create_history_entry_mock = mocker.patch(
        "camac.instance.domain_logic.address_assignment.create_history_entry"
    )
    mocker.patch(
        "camac.instance.domain_logic.AddressAssignmentLogic.most_recent_address_suggestions"
    )

    work_item = caluma_work_item_factory(case=gr_instance.case)

    AddressAssignmentLogic.create_history_entry_for_address_change(
        work_item, admin_user
    )

    create_history_entry_mock.assert_called_once()


def test_formal_exam_completed_signal(
    db, mocker, service_factory, caluma_work_item_factory, gr_instance
):
    mocker.patch(
        "camac.instance.domain_logic.AddressAssignmentLogic.requires_address_assignment",
        return_value=True,
    )

    service_factory(slug="gvg")
    geometer = service_factory()

    ServiceRelation.objects.create(
        provider=geometer,
        receiver=gr_instance.responsible_service(),
        function=ServiceRelation.FUNCTION_GEOMETER,
    )
    work_item = caluma_work_item_factory(case=gr_instance.case)

    handler = PermissionEventHandlerGR(None)
    mock_manager = mocker.MagicMock()
    mocker.patch.object(handler, "manager", new=mock_manager)
    handler.formal_exam_completed(gr_instance, work_item)
