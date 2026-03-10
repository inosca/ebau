import pytest
from caluma.caluma_workflow.models import Workflow, WorkItem
from django.utils import timezone

from camac.applicants.models import ROLE_CHOICES, ApplicantConfirmationRound
from camac.permissions.conditions import (
    HasAdditionalDemandWithFormEdit,
    HasApplicantConfirmationRound,
    HasApplicantRole,
    IsCreatedByService,
    IsModification,
    IsPaper,
    IsServiceGroup,
    IsWorkflow,
    PermissionContext,
    RequireWorkItem,
)
from camac.tests.form_utils import FormUtils
from camac.timelines.models import FormTimeline


@pytest.mark.parametrize("is_paper", [True, False])
def test_condition_is_paper(db, is_paper, so_instance, userinfo, form_utils: FormUtils):
    if is_paper:
        form_utils.set_is_paper(so_instance.case.document, True)

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


@pytest.mark.parametrize(
    ("timeline_open", "timeline_type", "expected_result"),
    [
        (False, FormTimeline.Type.CORRECTION, False),
        (True, FormTimeline.Type.CORRECTION, False),
        (False, FormTimeline.Type.ADDITIONAL_DEMAND, False),
        # open timeline of type additional demand should evaluate to True
        (True, FormTimeline.Type.ADDITIONAL_DEMAND, True),
    ],
)
def test_has_additional_demand_with_form_edit(
    db,
    form_timeline_factory,
    instance_factory,
    instance,
    timeline_open,
    timeline_type,
    expected_result,
    userinfo,
):
    # timeline for other instance should be irrelevant
    form_timeline_factory(
        instance=instance_factory(),
        start_date=timezone.now(),
        end_date=None,
        timeline_type=FormTimeline.Type.ADDITIONAL_DEMAND,
    )

    end_date = (
        timezone.now() + timezone.timedelta(days=1) if not timeline_open else None
    )
    form_timeline_factory(
        instance=instance,
        start_date=timezone.now(),
        end_date=end_date,
        timeline_type=timeline_type,
    )

    assert (
        HasAdditionalDemandWithFormEdit().apply(userinfo, PermissionContext(instance))
        == expected_result
    )


def test_has_applicant_confirmation_round(
    db,
    applicant_confirmation_round_factory,
    caluma_case_factory,
    instance_factory,
    userinfo,
):
    main_instance = instance_factory(case=caluma_case_factory())
    main_document = main_instance.case.document

    other_instance = instance_factory(case=caluma_case_factory())
    other_document = other_instance.case.document

    applicant_confirmation_round_factory(
        document=main_document,
        status=ApplicantConfirmationRound.Status.COMPLETED,
    )
    applicant_confirmation_round_factory(
        document=other_document,
        status=ApplicantConfirmationRound.Status.INVALIDATED,
    )

    invalidated = HasApplicantConfirmationRound(
        [ApplicantConfirmationRound.Status.INVALIDATED]
    )
    active = HasApplicantConfirmationRound(
        [
            ApplicantConfirmationRound.Status.COMPLETED,
            ApplicantConfirmationRound.Status.RUNNING,
        ]
    )

    assert not invalidated.apply(userinfo, PermissionContext(main_instance))
    assert invalidated.apply(userinfo, PermissionContext(other_instance))
    assert active.apply(userinfo, PermissionContext(main_instance))
    assert not active.apply(userinfo, PermissionContext(other_instance))


@pytest.mark.parametrize("is_modification", [True, False])
def test_condition_is_modification(
    db, is_modification, be_instance, userinfo, form_utils: FormUtils
):
    if is_modification:
        form_utils.add_answer(
            be_instance.case.document, "projektaenderung", "projektaenderung-ja"
        )

    assert (
        IsModification().apply(userinfo, PermissionContext(be_instance))
        == is_modification
    )


@pytest.mark.parametrize(
    "workflow,expected_result",
    [
        ("building-permit", True),
        ("preliminary-clarification", True),
        ("internal", False),
        ("migrated", False),
    ],
)
def test_condition_is_workflow(db, workflow, expected_result, be_instance, userinfo):
    be_instance.case.workflow = Workflow.objects.get(pk=workflow)
    be_instance.case.save()

    assert (
        IsWorkflow(["building-permit", "preliminary-clarification"]).apply(
            userinfo, PermissionContext(be_instance)
        )
        == expected_result
    )


@pytest.mark.parametrize("is_created_by_service", [True, False])
def test_condition_is_created_by_service(
    db,
    is_created_by_service,
    be_instance,
    userinfo,
    form_utils: FormUtils,
    group_factory,
):
    if not is_created_by_service:
        be_instance.group = group_factory()
        be_instance.save()

    assert (
        IsCreatedByService().apply(userinfo, PermissionContext(be_instance))
        == is_created_by_service
    )
