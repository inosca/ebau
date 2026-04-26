from datetime import date

import pytest
from caluma.caluma_workflow.api import suspend_case
from caluma.caluma_workflow.models import Case, Task, WorkItem
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status
from rest_framework.exceptions import ValidationError

from camac.ech0211.models import Message
from camac.instance.domain_logic import RejectionLogic
from camac.instance.models import HistoryActionConfig


@pytest.mark.parametrize(
    "instance_state__name,is_authority,has_permission",
    [
        ("rejected", True, True),
        ("circulation_init", True, True),
        ("circulation_init", False, False),  # not authority
        ("subm", True, False),  # wrong instance state
    ],
)
def test_has_permission(
    db,
    be_instance,
    group,
    group_factory,
    is_authority,
    has_permission,
):
    if not is_authority:
        group = group_factory()

    assert RejectionLogic.has_permission(be_instance, group) == has_permission


# TODO:  Update test after removing nfd work items
@pytest.mark.parametrize(
    "reason,module_settings,message",
    [
        (
            "inquiry",
            None,
            "Das Dossier kann nicht zurückgewiesen werden solange noch eine Zirkulation läuft.",
        ),
        (
            "claim",
            lf("additional_demand_settings"),
            "Das Dossier kann nicht zurückgewiesen werden solange noch Nachforderungen offen sind.",
        ),
    ],
)
def test_validate(
    db,
    be_instance,
    active_inquiry_factory,
    caluma_document_factory,
    caluma_answer_factory,
    caluma_work_item_factory,
    settings,
    reason,
    module_settings,
    message,
):
    if reason == "inquiry":
        active_inquiry_factory(be_instance)

    elif reason == "claim":
        task_obj, created = Task.objects.get_or_create(
            slug=module_settings["TASK"],
            defaults={"name": "Nachforderung", "type": Task.TYPE_SIMPLE},
        )
        caluma_work_item_factory(
            case=be_instance.case,
            task=task_obj,
            status=WorkItem.STATUS_READY,
        )

    with pytest.raises(ValidationError) as e:
        assert RejectionLogic.validate_for_rejection(be_instance)

    assert message in e.value.detail


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize("allow_revert", [True, False])
def test_reject_instance(
    db,
    be_instance,
    be_ech0211_settings,
    admin_client,
    instance_state_factory,
    rejection_settings,
    notification_template,
    mailoutbox,
    allow_revert,
    caluma_work_item_factory,
    deadlines_settings,
    instance_deadline_factory,
    mocker,
):
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )
    deadlines_settings.enabled = True
    instance_state_factory(name=rejection_settings["INSTANCE_STATE"])

    deadline = instance_deadline_factory(
        instance=be_instance.case.family.instance,
        service=be_instance.responsible_service(filter="municipality"),
        start_date=date(2025, 1, 1),
        process_deadline_date=None,
    )
    assert deadline.process_deadline_date is None

    work_item = caluma_work_item_factory(
        case=be_instance.case,
        status=WorkItem.STATUS_READY,
        child_case=None,
    )

    rejection_settings["ALLOW_REVERT"] = allow_revert
    rejection_settings["ALLOWED_INSTANCE_STATES"] = [be_instance.instance_state.name]
    rejection_settings["NOTIFICATIONS"] = {
        "REJECTED": [
            {
                "recipient_types": ["applicant"],
                "template_slug": notification_template.slug,
            }
        ]
    }
    rejection_settings["WORK_ITEM"] = {"TASK": work_item.task_id}

    response = admin_client.post(
        reverse("instance-rejection", args=[be_instance.pk]),
        data={
            "data": {
                "id": be_instance.pk,
                "type": "instance-rejections",
                "attributes": {"rejection-feedback": "My rejection feedback"},
            }
        },
    )

    assert response.status_code == status.HTTP_200_OK

    be_instance.refresh_from_db()
    work_item.refresh_from_db()

    if allow_revert:
        assert be_instance.case.status == Case.STATUS_SUSPENDED
    else:
        assert be_instance.case.status == Case.STATUS_CANCELED

    assert work_item.status == WorkItem.STATUS_COMPLETED
    assert be_instance.instance_state.name == rejection_settings["INSTANCE_STATE"]
    history_entry = be_instance.history.filter(
        history_type=HistoryActionConfig.HISTORY_TYPE_STATUS
    ).latest("created_at")
    assert history_entry.get_trans_attr("title") == "Dossier zurückgewiesen"
    deadline.refresh_from_db()
    assert deadline.process_deadline_date == history_entry.created_at.date()
    assert Message.objects.count() == 1
    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject


@pytest.mark.parametrize(
    "role__name,instance_state__name", [("Municipality", "rejected")]
)
def test_revert_instance_rejection(
    db,
    be_instance,
    be_ech0211_settings,
    admin_client,
    caluma_admin_user,
    rejection_settings,
    notification_template,
    mailoutbox,
    deadlines_settings,
    instance_deadline_factory,
    mocker,
):
    mocker.patch(
        "camac.deadlines.models.InstanceDeadline.trigger_side_effect",
        return_value=False,
    )
    deadlines_settings.enabled = True
    rejection_settings["NOTIFICATIONS"] = {
        "REVERTED": [
            {
                "recipient_types": ["applicant"],
                "template_slug": notification_template.slug,
            }
        ]
    }

    deadline = instance_deadline_factory(
        instance=be_instance.case.family.instance,
        service=be_instance.responsible_service(filter="municipality"),
        start_date=date(2025, 1, 1),
    )
    assert deadline.process_deadline_date is not None

    suspend_case(be_instance.case, caluma_admin_user)

    response = admin_client.post(reverse("instance-rejection", args=[be_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    previous_instance_state = be_instance.previous_instance_state.name

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == previous_instance_state
    assert be_instance.case.status == Case.STATUS_RUNNING
    assert (
        be_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
        == "Rückweisung aufgehoben"
    )
    deadline.refresh_from_db()
    assert deadline.process_deadline_date is None
    assert Message.objects.count() == 1
    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_save_rejection_feedback(
    db,
    be_instance,
    admin_client,
    rejection_settings,
):
    rejection_settings["ALLOWED_INSTANCE_STATES"] = [be_instance.instance_state.name]

    before_instance_state = be_instance.instance_state.name
    rejection_feedback = "My rejection feedback"

    assert be_instance.rejection_feedback is None

    response = admin_client.patch(
        reverse("instance-rejection", args=[be_instance.pk]),
        data={
            "data": {
                "id": be_instance.pk,
                "type": "instance-rejections",
                "attributes": {"rejection-feedback": rejection_feedback},
            }
        },
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == before_instance_state
    assert be_instance.case.status == Case.STATUS_RUNNING
    assert be_instance.rejection_feedback == rejection_feedback
