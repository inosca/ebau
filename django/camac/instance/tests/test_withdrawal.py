from datetime import date

import pytest
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status

from camac.core.models import HistoryActionConfig


@pytest.fixture
def publications(so_instance, so_publication_settings, utils, work_item_factory):
    work_items = []

    for start, end in [
        (date(2024, 4, 1), date(2024, 4, 10)),  # past
        (date(2024, 4, 10), date(2024, 4, 20)),  # active
        (date(2024, 4, 20), date(2024, 4, 30)),  # future
    ]:
        work_item = work_item_factory(
            task_id=so_publication_settings["FILL_TASKS"][0],
            status=WorkItem.STATUS_COMPLETED,
            case=so_instance.case,
            meta={"is-published": True},
        )

        utils.add_answer(
            work_item.document,
            so_publication_settings["RANGE_QUESTIONS"][0][0],
            start,
        )
        utils.add_answer(
            work_item.document,
            so_publication_settings["RANGE_QUESTIONS"][0][1],
            end,
        )

        work_items.append(work_item)

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
    form_question_factory,
    skipped_work_items,
    mailoutbox,
    has_publications,
    request,
    so_ech0211_settings,
    grant_all_permissions,
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

    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject

    if has_publications:
        past_publication.refresh_from_db()
        active_publication.refresh_from_db()
        future_publication.refresh_from_db()

        assert past_publication.meta["is-published"]
        assert not active_publication.meta["is-published"]
        assert not future_publication.meta["is-published"]
