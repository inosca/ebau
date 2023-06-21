import json
from datetime import date

import pytest
from caluma.caluma_core.permissions import AllowAny
from caluma.caluma_core.visibilities import Any
from caluma.caluma_workflow.models import WorkItem


@pytest.fixture
def appeal_deadline_factory(answer_factory, be_appeal_settings, document_factory):
    def wrapper(deadline):
        row = document_factory(form_id=be_appeal_settings["ROW_FORM"])

        answer_factory(
            document=row,
            question_id=be_appeal_settings["QUESTIONS"]["AUTHORITY"],
            value=be_appeal_settings["ANSWERS"]["AUTHORITY"]["LEGAL_DEPARTEMENT"],
        )
        answer_factory(
            document=row,
            question_id=be_appeal_settings["QUESTIONS"]["TYPE"],
            value=be_appeal_settings["ANSWERS"]["TYPE"]["DEADLINE"],
        )
        answer_factory(
            document=row,
            question_id=be_appeal_settings["QUESTIONS"]["DATE"],
            date=deadline,
        )

        return row

    return wrapper


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_validate_create_inquiry_context(
    db,
    work_item_factory,
    service,
    be_instance,
    caluma_admin_schema_executor,
    distribution_settings,
):
    work_item = work_item_factory(case=be_instance.case, child_case=None)

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
    work_item_factory,
):
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [Any])
    mocker.patch("caluma.caluma_core.mutation.Mutation.permission_classes", [AllowAny])

    work_item = work_item_factory(case=be_instance.case, child_case=None)

    dates = [date(2023, 4, 20), date(2023, 5, 1)]
    rows = [str(appeal_deadline_factory(deadline).pk) for deadline in dates]

    work_item_to_delete = work_item_factory(
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
        assert created.name["fr"] == "Prendre position sur la plainte"

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
    work_item_factory,
):
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [Any])
    mocker.patch("caluma.caluma_core.mutation.Mutation.permission_classes", [AllowAny])

    row = appeal_deadline_factory(date(2023, 4, 21))

    work_item = work_item_factory(
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
