import pytest
from caluma.caluma_core.relay import extract_global_id
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import complete_work_item, skip_work_item
from caluma.caluma_workflow.models import WorkItem

from camac.caluma.extensions.visibilities import CustomVisibility

from .test_distribution_workflow import _inquiry_factory


@pytest.fixture
def distribution_case_so(
    caluma_admin_user,
    disable_ech0211_settings,
    instance_state_factory,
    mocker,
    so_additional_demand_settings,
    so_distribution_settings,
    so_instance,
):
    mocker.patch("camac.notification.utils.send_mail")

    instance_state_factory(name="material-exam")
    instance_state_factory(name="init-distribution")
    instance_state_factory(name="distribution")

    for task in ["submit", "formal-exam", "material-exam"]:
        skip_work_item(
            work_item=so_instance.case.work_items.get(task_id=task),
            user=caluma_admin_user,
        )

    return so_instance.case


@pytest.fixture
def distribution_child_case_so(distribution_case_so, so_distribution_settings):
    return distribution_case_so.work_items.get(
        task_id=so_distribution_settings["DISTRIBUTION_TASK"]
    ).child_case


@pytest.fixture
def inquiry_factory_so(
    caluma_admin_user,
    distribution_child_case_so,
    service_factory,
    service,
    so_distribution_settings,
):
    def factory(
        to_service=service_factory(), from_service=service, sent=False, direct=False
    ):
        inquiry = _inquiry_factory(
            to_service=to_service,
            from_service=from_service,
            sent=sent,
            user=caluma_admin_user,
            distribution_child_case=distribution_child_case_so,
            distribution_settings=so_distribution_settings,
        )

        if direct:
            save_answer(
                document=inquiry.document,
                question=Question.objects.get(
                    pk=so_distribution_settings["QUESTIONS"]["DIRECT"]
                ),
                value=[so_distribution_settings["ANSWERS"]["DIRECT"]["YES"]],
                user=caluma_admin_user,
            )

        return inquiry

    return factory


def test_direct_inquiry(
    db,
    caluma_admin_user,
    inquiry_factory_so,
    service_factory,
    service,
    so_distribution_settings,
):
    municipality_service = service
    parent_service = service_factory()
    child_service = service_factory(service_parent=parent_service)

    parent_inquiry = inquiry_factory_so(
        to_service=parent_service, from_service=municipality_service, sent=True
    )
    child_inquiry = inquiry_factory_so(
        to_service=child_service, from_service=parent_service, sent=True, direct=True
    )

    save_answer(
        document=child_inquiry.child_case.document,
        question=Question.objects.get(
            pk=so_distribution_settings["QUESTIONS"]["STATUS"]
        ),
        value=so_distribution_settings["ANSWERS"]["STATUS"]["POSITIVE"],
        user=caluma_admin_user,
    )

    complete_work_item(
        work_item=child_inquiry.child_case.work_items.get(
            task_id=so_distribution_settings["INQUIRY_ANSWER_FILL_TASK"]
        ),
        user=caluma_admin_user,
    )

    assert child_inquiry.status == WorkItem.STATUS_COMPLETED

    parent_inquiry.refresh_from_db()
    assert parent_inquiry.status == WorkItem.STATUS_COMPLETED
    assert parent_inquiry.child_case.document.answers.count() == 1
    assert (
        parent_inquiry.child_case.document.answers.get(
            question_id=so_distribution_settings["QUESTIONS"]["STATUS"]
        ).value
        == so_distribution_settings["ANSWERS"]["STATUS"]["DIRECT"]
    )


def test_direct_inquiry_visibility(
    db,
    caluma_admin_schema_executor,
    gql,
    inquiry_factory_so,
    mocker,
    service_factory,
    service,
    settings,
    so_distribution_settings,
    so_instance,
):
    settings.APPLICATION_NAME = "kt_so"
    mocker.patch("caluma.caluma_core.types.Node.visibility_classes", [CustomVisibility])
    mocker.patch(
        "camac.caluma.extensions.visibilities.CustomVisibility._all_visible_instances",
        return_value=[so_instance.pk],
    )

    municipality_service = service
    parent_service = service_factory()
    child_service = service_factory(service_parent=parent_service)

    parent_inquiry = inquiry_factory_so(
        to_service=parent_service, from_service=municipality_service, sent=True
    )
    direct_child_inquiry = inquiry_factory_so(
        to_service=child_service, from_service=parent_service, sent=True, direct=True
    )
    indirect_child_inquiry = inquiry_factory_so(
        to_service=child_service, from_service=parent_service, sent=True
    )

    result = caluma_admin_schema_executor(
        gql("work-items-for-task"),
        variables={"task": so_distribution_settings["INQUIRY_TASK"]},
    )

    assert not result.errors

    ids = [
        extract_global_id(edge["node"]["id"])
        for edge in result.data["allWorkItems"]["edges"]
    ]

    assert str(parent_inquiry.pk) in ids
    assert str(direct_child_inquiry.pk) in ids
    assert str(indirect_child_inquiry.pk) not in ids
