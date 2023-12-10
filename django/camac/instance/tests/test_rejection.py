import pytest
from caluma.caluma_workflow.api import suspend_case
from caluma.caluma_workflow.models import Case, WorkItem
from django.urls import reverse
from pytest_lazyfixture import lazy_fixture
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
            lazy_fixture("additional_demand_settings"),
            "Das Dossier kann nicht zurückgewiesen werden solange noch Nachforderungen offen sind.",
        ),
        (
            "claim_legacy",
            lazy_fixture("disable_additional_demand_settings"),
            "Das Dossier kann nicht zurückgewiesen werden solange noch Nachforderungen offen sind.",
        ),
    ],
)
def test_validate(
    db,
    be_instance,
    active_inquiry_factory,
    document_factory,
    answer_factory,
    work_item_factory,
    settings,
    reason,
    module_settings,
    message,
):
    if reason == "inquiry":
        active_inquiry_factory(be_instance)
    elif reason == "claim":
        work_item_factory(
            case=be_instance.case,
            task__slug=module_settings["TASK"],
            status=WorkItem.STATUS_READY,
        )
    elif reason == "claim_legacy":
        settings.APPLICATION_NAME = "kt_bern"
        document = document_factory(form_id="nfd")

        work_item_factory(case=be_instance.case, document=document)

        answer_factory(
            document=document_factory(form__slug="nfd-tabelle", family=document),
            question__slug="nfd-tabelle-status",
            value="nfd-tabelle-status-in-bearbeitung",
        )

    with pytest.raises(ValidationError) as e:
        assert RejectionLogic.validate_for_rejection(be_instance)

    assert message in e.value.detail


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_reject_instance(
    db,
    be_instance,
    admin_client,
    instance_state_factory,
    rejection_settings,
    notification_template,
    mailoutbox,
    enable_ech,
):
    instance_state_factory(name=rejection_settings["INSTANCE_STATE"])

    rejection_settings["ALLOWED_INSTANCE_STATES"] = [be_instance.instance_state.name]
    rejection_settings["NOTIFICATIONS"] = {
        "REJECTED": [
            {
                "recipient_types": ["applicant"],
                "template_slug": notification_template.slug,
            }
        ]
    }

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

    assert be_instance.instance_state.name == rejection_settings["INSTANCE_STATE"]
    assert be_instance.case.status == Case.STATUS_SUSPENDED
    assert (
        be_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
        == "Dossier zurückgewiesen"
    )
    assert Message.objects.count() == 1
    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject


@pytest.mark.parametrize(
    "role__name,instance_state__name", [("Municipality", "rejected")]
)
def test_revert_instance_rejection(
    db,
    be_instance,
    admin_client,
    caluma_admin_user,
    rejection_settings,
    notification_template,
    mailoutbox,
    enable_ech,
):
    rejection_settings["NOTIFICATIONS"] = {
        "REVERTED": [
            {
                "recipient_types": ["applicant"],
                "template_slug": notification_template.slug,
            }
        ]
    }

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
