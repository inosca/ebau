import pytest
from caluma.caluma_workflow.models import WorkItem

from camac.applicants.models import ROLE_CHOICES
from camac.permissions.api import ACLUserInfo
from camac.permissions.conditions import (
    HasApplicantRole,
    IsPaper,
    IsServiceGroup,
    PermissionContext,
    RequireWorkItem,
)
from camac.tests.form_utils import FormUtils


@pytest.fixture
def userinfo(user, service, role):
    return ACLUserInfo(user=user, service=service, token=None, role=role)


@pytest.mark.parametrize("is_paper", [True, False])
def test_condition_is_paper(db, is_paper, so_instance, userinfo, form_utils: FormUtils):
    if is_paper:
        form_utils.add_answer(so_instance.case.document, "is-paper", "is-paper-yes")

    assert IsPaper().apply(userinfo, PermissionContext(so_instance)) == is_paper


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
    db,
    expected_result,
    has_work_item,
    so_instance,
    status,
    userinfo,
    caluma_work_item_factory,
):
    task_id = "test-work-item"

    if has_work_item:
        caluma_work_item_factory(
            case=so_instance.case, task_id=task_id, status=WorkItem.STATUS_READY
        )

    assert (
        RequireWorkItem(task_id, status).apply(userinfo, PermissionContext(so_instance))
        == expected_result
    )


def test_condition_require_work_item_addressed_to_current_service(
    db,
    so_instance,
    userinfo,
    caluma_work_item_factory,
):
    caluma_work_item_factory(
        case=so_instance.case,
        task_id="addressed-work-item",
        addressed_groups=[str(userinfo.service.pk)],
    )
    caluma_work_item_factory(
        case=so_instance.case,
        task_id="not-addressed-work-item",
        addressed_groups=["some-other-service-pk"],
    )

    assert (
        RequireWorkItem("addressed-work-item", addressed_to_current_service=True).apply(
            userinfo, PermissionContext(so_instance)
        )
        is True
    )
    assert (
        RequireWorkItem("addressed-work-item").apply(
            userinfo, PermissionContext(so_instance)
        )
        is True
    )
    assert (
        RequireWorkItem(
            "not-addressed-work-item", addressed_to_current_service=True
        ).apply(userinfo, PermissionContext(so_instance))
        is False
    )
    assert (
        RequireWorkItem("not-addressed-work-item").apply(
            userinfo, PermissionContext(so_instance)
        )
        is True
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

    assert (
        HasApplicantRole(roles).apply(userinfo, PermissionContext(so_instance))
        == expected_result
    )


@pytest.mark.parametrize(
    "has_service,service_group__name,expected_result",
    [
        (True, "foo", True),
        (True, "bar", True),
        (True, "baz", False),
        (False, "foo", False),
    ],
)
def test_is_service_group(db, expected_result, has_service, userinfo):
    if not has_service:
        userinfo.service = None

    assert IsServiceGroup(["foo", "bar"]).apply(userinfo, None) == expected_result
