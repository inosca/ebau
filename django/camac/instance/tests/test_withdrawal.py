from datetime import date

import pytest
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status

from camac.core.models import HistoryActionConfig
from camac.ech0211.models import Message
from camac.permissions import api as permissions_api


@pytest.fixture
def publications(so_instance, so_publication_settings, create_caluma_publication):
    work_items = []

    for start, end in [
        (date(2024, 4, 1), date(2024, 4, 10)),  # past
        (date(2024, 4, 10), date(2024, 4, 20)),  # active
        (date(2024, 4, 20), date(2024, 4, 30)),  # future
    ]:
        work_items.append(
            create_caluma_publication(
                so_instance,
                start,
                end,
                module_settings=so_publication_settings,
            )
        )

    return work_items


@pytest.mark.freeze_time("2024-04-15", tick=True)
@pytest.mark.parametrize("role__name", ["applicant"])
@pytest.mark.parametrize(
    "instance_state__name,has_publications,skipped_work_items",
    [
        ("subm", False, ["submit"]),
        ("material-exam", False, ["submit", "formal-exam"]),
        ("init-distribution", False, ["submit", "formal-exam", "material-exam"]),
        ("distribution", True, ["submit", "formal-exam", "material-exam"]),
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
    caluma_form_question_factory,
    skipped_work_items,
    mailoutbox,
    has_publications,
    request,
    so_ech0211_settings,
    grant_all_permissions,
    instance_service_factory,
):
    so_instance.involved_applicants.all().delete()
    applicant_factory(instance=so_instance, invitee=admin_user)
    instance_state_factory(name=so_withdrawal_settings["INSTANCE_STATE"])
    instance_service_factory(
        instance=so_instance, service__service_group__name="municipality", active=1
    )

    # needed because completing distrubution-complete changes the instance state
    # to decision
    instance_state_factory(name=so_decision_settings["INSTANCE_STATE"])

    caluma_form_question_factory(
        form_id="entscheid",
        question__slug=so_decision_settings["QUESTIONS"]["DECISION"],
        question__type=Question.TYPE_TEXT,
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

    if has_publications:
        (
            past_publication,
            active_publication,
            future_publication,
        ) = request.getfixturevalue("publications")

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

    # check that two eCH messages were sent:
    # status notification (decision) and withdrawal
    assert Message.objects.count() == 2

    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject

    if has_publications:
        past_publication.refresh_from_db()
        active_publication.refresh_from_db()
        future_publication.refresh_from_db()

        assert past_publication.meta["is-published"] is True
        assert active_publication.meta["is-published"] is False
        assert future_publication.meta["is-published"] is False


@pytest.mark.freeze_time("2024-04-15", tick=True)
@pytest.mark.parametrize("role__name,instance_state__name", [("applicant", "subm")])
def test_withdraw_instance_light(
    db,
    admin_client,
    admin_user,
    applicant_factory,
    set_application_ag,
    ag_instance,
    ag_withdrawal_settings,
    ag_access_levels,
    ag_permissions_settings,
    caluma_work_item_factory,
    instance_service_factory,
    notification_template_factory,
    mailoutbox,
):
    ag_instance.involved_applicants.all().delete()
    applicant_factory(instance=ag_instance, invitee=admin_user)
    instance_service_factory(
        instance=ag_instance, service__service_group__name="municipality", active=1
    )
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.USER.value,
        access_level="applicant",
        user=admin_user,
    )

    caluma_work_item_factory(
        case=ag_instance.case,
        task_id=ag_withdrawal_settings["REQUEST_TASK"],
        status=WorkItem.STATUS_READY,
        child_case=None,
    )

    notification_subject = "Withdrawal Notification"
    for notification in ag_withdrawal_settings["NOTIFICATIONS"]:
        notification_template_factory(
            slug=notification["template_slug"],
            subject=notification_subject,
            body="This is a withdrawal notification.",
        )

    instance_state = ag_instance.instance_state.name

    url = reverse("instance-withdraw", args=[ag_instance.pk])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT

    ag_instance.refresh_from_db()

    assert ag_instance.instance_state.name == instance_state

    assert (
        ag_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
        == "Rückzug beantragt"
    )

    assert Message.objects.count() == 0

    assert len(mailoutbox) == 2
    assert notification_subject in mailoutbox[0].subject
    assert notification_subject in mailoutbox[1].subject

    assert ag_instance.case.meta.get("withdrawal-requested") is True


@pytest.mark.freeze_time("2024-04-15", tick=True)
@pytest.mark.parametrize("role__name,instance_state__name", [("applicant", "subm")])
def test_withdraw_instance_light_completed(
    db,
    admin_client,
    admin_user,
    applicant_factory,
    set_application_ag,
    ag_instance,
    ag_withdrawal_settings,
    ag_access_levels,
    ag_permissions_settings,
    caluma_work_item_factory,
):
    applicant_factory(instance=ag_instance, invitee=admin_user)
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.USER.value,
        access_level="applicant",
        user=admin_user,
    )

    caluma_work_item_factory(
        case=ag_instance.case,
        task_id=ag_withdrawal_settings["REQUEST_TASK"],
        status=WorkItem.STATUS_COMPLETED,
        child_case=None,
    )

    url = reverse("instance-withdraw", args=[ag_instance.pk])
    response = admin_client.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[0]["detail"] == "Rückzug nicht möglich."
