import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.applicants.models import ROLE_CHOICES
from camac.permissions.api import ACLUserInfo
from camac.permissions.conditions import HasApplicantRole, IsPaper, RequireWorkItem


@pytest.fixture
def userinfo(user, service, role):
    return ACLUserInfo(user=user, service=service, token=None, role=role)


@pytest.mark.parametrize("is_paper", [True, False])
def test_condition_is_paper(db, is_paper, so_instance, userinfo, utils):
    if is_paper:
        utils.add_answer(so_instance.case.document, "is-paper", "is-paper-yes")

    assert IsPaper().apply(userinfo, so_instance) == is_paper


@pytest.mark.parametrize(
    "has_work_item,status,expected_result",
    [
        (True, None, True),
        (False, None, False),
        (True, WorkItem.STATUS_COMPLETED, False),
        (True, WorkItem.STATUS_READY, True),
    ],
)
def test_condition_require_work_item(
    db, expected_result, has_work_item, so_instance, status, userinfo, work_item_factory
):
    task_id = "test-work-item"

    if has_work_item:
        work_item_factory(
            case=so_instance.case, task_id=task_id, status=WorkItem.STATUS_READY
        )

    assert (
        RequireWorkItem(task_id, status).apply(userinfo, so_instance) == expected_result
    )


@pytest.mark.parametrize(
    "applicant_role,roles,expected_result",
    [
        (
            ROLE_CHOICES.ADMIN.value,
            [ROLE_CHOICES.ADMIN.value, ROLE_CHOICES.EDITOR.value],
            True,
        ),
        (
            ROLE_CHOICES.READ_ONLY.value,
            [ROLE_CHOICES.ADMIN.value, ROLE_CHOICES.EDITOR.value],
            False,
        ),
    ],
)
def test_has_applicant_role(
    db,
    applicant_factory,
    applicant_role,
    expected_result,
    roles,
    so_instance,
    user,
    userinfo,
):
    so_instance.involved_applicants.all().delete()

    applicant_factory(instance=so_instance, invitee=user, role=applicant_role)

    assert HasApplicantRole(roles).apply(userinfo, so_instance) == expected_result
