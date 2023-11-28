import pytest
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status

from camac.core.models import HistoryActionConfig
from camac.instance.domain_logic import WithdrawalLogic


@pytest.mark.parametrize(
    "instance_state__name,role__name,is_applicant,has_permission",
    [
        ("subm", "Applicant", True, True),
        ("decision", "Applicant", True, False),  # wrong instance state
        ("subm", "Municipality", True, False),  # wrong role
        ("subm", "Applicant", False, False),  # not an applicant
    ],
)
def test_has_permission(
    db,
    admin_user,
    applicant_factory,
    so_instance,
    group,
    has_permission,
    is_applicant,
):
    if is_applicant:
        applicant_factory(instance=so_instance, invitee=admin_user)

    assert (
        WithdrawalLogic.has_permission(so_instance, admin_user, group) == has_permission
    )


def test_has_permission_module_disabled(
    db,
    so_instance,
    admin_user,
    group,
    disable_withdrawal_settings,
):
    assert not WithdrawalLogic.has_permission(so_instance, admin_user, group)


@pytest.mark.parametrize("role__name", ["applicant"])
@pytest.mark.parametrize(
    "instance_state__name,skipped_work_items",
    [
        ("subm", ["submit"]),
        ("material-exam", ["submit", "formal-exam"]),
        ("init-distribution", ["submit", "formal-exam", "material-exam"]),
        ("distribution", ["submit", "formal-exam", "material-exam"]),
    ],
)
def test_withdraw_instance(
    db,
    so_instance,
    admin_client,
    admin_user,
    applicant_factory,
    so_withdrawal_settings,
    caluma_admin_user,
    instance_state_factory,
    so_decision_settings,
    notification_template,
    so_distribution_settings,
    set_application_so,
    form_question_factory,
    skipped_work_items,
    mailoutbox,
):
    so_instance.involved_applicants.all().delete()
    applicant_factory(instance=so_instance, invitee=admin_user)
    instance_state_factory(name=so_withdrawal_settings["INSTANCE_STATE"])

    # needed because completing distrubution-complete changes the instance state
    # to decision
    instance_state_factory(name=so_decision_settings["INSTANCE_STATE"])

    form_question_factory(
        form_id="entscheid",
        question__slug=so_decision_settings["QUESTIONS"]["DECISION"],
    )

    so_withdrawal_settings["NOTIFICATIONS"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["applicant"],
        }
    ]

    for task_id in skipped_work_items:
        skip_work_item(
            so_instance.case.work_items.get(
                task_id=task_id,
                status=WorkItem.STATUS_READY,
            ),
            user=caluma_admin_user,
        )

    url = reverse("instance-withdraw", args=[so_instance.pk])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    so_instance.refresh_from_db()

    assert so_instance.instance_state.name == so_withdrawal_settings["INSTANCE_STATE"]

    decision = so_instance.case.work_items.get(task_id=so_decision_settings["TASK"])
    assert decision.status == WorkItem.STATUS_READY
    assert (
        decision.document.answers.get(
            question_id=so_decision_settings["QUESTIONS"]["DECISION"]
        ).value
        == so_decision_settings["ANSWERS"]["DECISION"]["WITHDRAWAL"]
    )

    assert (
        so_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
        == "Dossier zurückgezogen"
    )

    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject
