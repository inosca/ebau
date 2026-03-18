import json
import re
from contextlib import nullcontext
from datetime import date

import pytest
from caluma.caluma_core.permissions import AllowAny
from caluma.caluma_core.visibilities import Any
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.api import CalumaApi


@pytest.fixture
def appeal_deadline_factory(
    caluma_answer_factory, be_appeal_settings, caluma_document_factory
):
    def wrapper(deadline):
        row = caluma_document_factory(form_id=be_appeal_settings["ROW_FORM"])

        caluma_answer_factory(
            document=row,
            question_id=be_appeal_settings["QUESTIONS"]["AUTHORITY"],
            value=be_appeal_settings["ANSWERS"]["AUTHORITY"]["LEGAL_DEPARTEMENT"],
        )
        caluma_answer_factory(
            document=row,
            question_id=be_appeal_settings["QUESTIONS"]["TYPE"],
            value=be_appeal_settings["ANSWERS"]["TYPE"]["DEADLINE"],
        )
        caluma_answer_factory(
            document=row,
            question_id=be_appeal_settings["QUESTIONS"]["DATE"],
            date=deadline,
        )

        return row

    return wrapper


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_validate_create_inquiry_context(
    db,
    caluma_work_item_factory,
    service,
    be_instance,
    caluma_admin_schema_executor,
    distribution_settings,
):
    work_item = caluma_work_item_factory(
        case=be_instance.case,
        child_case=None,
        addressed_groups=[str(service.pk)],
    )

    distribution_settings["INQUIRY_CREATE_TASK"] = work_item.task_id

    result = caluma_admin_schema_executor(
        """
        mutation($input: CompleteWorkItemInput!) {
            completeWorkItem(input: $input) {
                clientMutationId
            }
        }
        """,
        variables={
            "input": {
                "id": str(work_item.id),
                "context": json.dumps({"addressed_groups": [str(service.pk)]}),
            }
        },
    )

    assert result.errors
    assert "Services can't create inquiries for themselves!" in result.errors[0].message


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_appeal_work_item(
    db,
    appeal_deadline_factory,
    application_settings,
    be_appeal_settings,
    be_instance,
    caluma_admin_schema_executor,
    gql,
    mocker,
    service,
    caluma_work_item_factory,
    notification_template_factory,
):
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [Any])
    mocker.patch("caluma.caluma_core.mutation.Mutation.permission_classes", [AllowAny])
    notification_template_factory(slug="create-manual-work-item")

    work_item = caluma_work_item_factory(
        case=be_instance.case, child_case=None, document__form_id="appeal"
    )

    dates = [date(2023, 4, 20), date(2023, 5, 1)]
    rows = [str(appeal_deadline_factory(deadline).pk) for deadline in dates]

    work_item_to_delete = caluma_work_item_factory(
        case=be_instance.case,
        task_id=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
        meta={
            "is-appeal-statement-deadline": True,
            "appeal-row-id": "6b8f3186-8330-4720-8385-2891be249594",
        },
    )

    result = caluma_admin_schema_executor(
        gql("save-document-table-answer"),
        variables={
            "input": {
                "question": be_appeal_settings["QUESTIONS"]["TABLE"],
                "document": str(work_item.document.pk),
                "value": rows,
            }
        },
    )

    assert not result.errors

    for deadline, row_id in zip(dates, rows):
        created = work_item.case.work_items.filter(
            task_id=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
            deadline__date=deadline,
        ).first()

        assert created.status == WorkItem.STATUS_READY
        assert created.deadline.date().isoformat() == deadline.isoformat()
        assert created.addressed_groups == [str(service.pk)]
        assert created.meta == {
            # from event handler
            "not-viewed": True,
            "notify-completed": False,
            "notify-deadline": True,
            # from validation layer
            "is-appeal-statement-deadline": True,
            "appeal-row-id": row_id,
        }

        assert created.name["de"] == "Stellungnahme zu Beschwerde abgeben"
        assert created.name["fr"] == "Prendre position sur le recours"

    with pytest.raises(WorkItem.DoesNotExist):
        work_item_to_delete.refresh_from_db()


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_appeal_work_item_update(
    db,
    appeal_deadline_factory,
    application_settings,
    be_appeal_settings,
    be_instance,
    caluma_admin_schema_executor,
    gql,
    mocker,
    caluma_work_item_factory,
):
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [Any])
    mocker.patch("caluma.caluma_core.mutation.Mutation.permission_classes", [AllowAny])

    row = appeal_deadline_factory(date(2023, 4, 21))

    work_item = caluma_work_item_factory(
        case=be_instance.case,
        task_id=application_settings["CALUMA"]["MANUAL_WORK_ITEM_TASK"],
        meta={"is-appeal-statement-deadline": True, "appeal-row-id": str(row.pk)},
    )

    result = caluma_admin_schema_executor(
        gql("save-document-date-answer"),
        variables={
            "input": {
                "question": be_appeal_settings["QUESTIONS"]["DATE"],
                "document": str(row.pk),
                "value": "2025-01-01",
            }
        },
    )

    assert not result.errors

    work_item.refresh_from_db()

    assert work_item.deadline.date().isoformat() == "2025-01-01"


@pytest.mark.parametrize(
    "q_type, value, skip_on_error, expect_error",
    [
        ("choice", "foo", True, False),
        ("choice", "foo", False, True),
        ("text", "foo", False, False),
        ("text", "foo", True, False),
    ],
)
def test_update_or_create_answer(
    db,
    be_instance,
    caluma_form_question_factory,
    q_type,
    value,
    skip_on_error,
    expect_error,
):
    question = caluma_form_question_factory(
        question__type=q_type, form=be_instance.case.document.form
    ).question

    if expect_error:
        expectation = pytest.raises(Exception)
    else:
        # expect no raise
        expectation = nullcontext()

    with expectation:
        CalumaApi().update_or_create_answer(
            be_instance.case.document,
            question.slug,
            value="hello",
            user=None,
            skip_on_error=skip_on_error,
        )


@pytest.mark.parametrize(
    "meta_before, meta_after, expect_error",
    [
        # some generic checks
        ({}, {}, False),
        ({"foo": "Bar"}, {"foo": "Bar"}, False),
        ({"foo": None}, {"foo": "Bar"}, False),
        ({"foo": "Bar"}, {"foo": None}, True),
        ({"foo": "Bar"}, {}, True),
        # configured exceptions to the rule and explicit checks as
        # reported as incidents
        ({"paper-submit-date": "2026-03-09"}, {}, False),
        ({"camac-dossier-number": "2026-9999"}, {}, True),
    ],
)
def test_case_metainfo_data_loss(
    db,
    admin_user,
    be_instance,
    meta_before,
    meta_after,
    expect_error,
    caluma_admin_schema_executor,
    mocker,
):

    # Don't care about visibility & permissions here
    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility._visible_instances_qs",
        return_value=type(be_instance).objects.all(),
    )

    case = be_instance.case
    case.meta = meta_before
    case.save()

    result = caluma_admin_schema_executor(
        """
        mutation SaveCase($input: SaveCaseInput!) {
            saveCase(input: $input) {
                clientMutationId
            }
        }
        """,
        variables={
            "input": {
                "id": str(case.pk),
                "meta": json.dumps(meta_after),
                "workflow": case.workflow_id,
            }
        },
    )

    if expect_error:
        assert result.errors
        assert re.match(r".*Cannot reset [^\s]+ from Case.meta.*", str(result.errors))
    else:
        assert not result.errors


@pytest.mark.parametrize(
    "meta_before, meta_after, expect_error",
    [
        # some generic checks
        ({}, {}, False),
        ({"foo": "Bar"}, {"foo": "Bar"}, False),
        ({"foo": None}, {"foo": "Bar"}, False),
        ({"foo": "Bar"}, {"foo": None}, True),
        ({"foo": "Bar"}, {}, True),
        # configured exceptions to the rule and explicit checks as
        # reported as incidents
        (
            # allowed to be reset, but only on case
            {"paper-submit-date": "2026-03-09"},
            {},
            True,
        ),
        (
            # resetting dossier number must not be allowed, even accidentally
            {"camac-dossier-number": "2026-9999"},
            {"paper-submit-date": "09.03.2023"},
            True,
        ),
        (
            {"notify-deadline": True},
            {},
            False,
        ),
        (
            {"not-viewed": True},
            {"not-viewed": None},
            False,
        ),
    ],
)
def test_workitem_metainfo_data_loss(
    db,
    request,
    be_instance,
    meta_before,
    meta_after,
    expect_error,
    caluma_admin_schema_executor,
    mocker,
):
    # Don't care about visibility & permissions here
    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility._visible_instances_qs",
        return_value=type(be_instance).objects.all(),
    )
    mocker.patch(
        "camac.caluma.extensions.permissions.CustomPermission.has_object_permission",
        return_value=True,
    )
    mocker.patch(
        "camac.caluma.extensions.permissions.CustomPermission.has_permission",
        return_value=True,
    )

    workitem = be_instance.case.work_items.first()
    workitem.meta.update(meta_before)
    workitem.save()

    result = caluma_admin_schema_executor(
        """
        mutation SaveWorkItem($input: SaveWorkItemInput!) {
            saveWorkItem (input: $input) {
                clientMutationId
            }
        }
        """,
        variables={
            "input": {
                "workItem": str(workitem.pk),
                "meta": json.dumps(meta_after),
            }
        },
    )

    if expect_error:
        assert result.errors
        assert re.match(
            r".*Cannot reset [^\s]+ from WorkItem.meta.*", str(result.errors)
        )
    else:
        assert not result.errors


@pytest.mark.parametrize(
    "meta_after, expect_error",
    [
        ({"submit-date": "2026-03-09", "paper-submit-date": "2026-03-09"}, False),
        ({"submit-date": "2026-03-09", "paper-submit-date": "09.03.2026"}, True),
        ({"submit-date": "2026-03-09", "paper-submit-date": "blah"}, True),
        ({"submit-date": "2026-03-09", "paper-submit-date": None}, False),
    ],
)
def test_case_metainfo_paper_submit_date(
    db,
    admin_user,
    be_instance,
    meta_after,
    expect_error,
    caluma_admin_schema_executor,
    mocker,
):

    # Don't care about visibility & permissions here
    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility._visible_instances_qs",
        return_value=type(be_instance).objects.all(),
    )

    case = be_instance.case

    result = caluma_admin_schema_executor(
        """
        mutation SaveCase($input: SaveCaseInput!) {
            saveCase(input: $input) {
                clientMutationId
            }
        }
        """,
        variables={
            "input": {
                "id": str(case.pk),
                "meta": json.dumps(meta_after),
                "workflow": case.workflow_id,
            }
        },
    )

    if expect_error:
        assert result.errors
        assert "Invalid paper submit date" in str(result.errors)

    else:
        assert not result.errors
