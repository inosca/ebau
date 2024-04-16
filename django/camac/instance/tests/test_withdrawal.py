from datetime import date

import pytest
from caluma.caluma_form.api import save_answer
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.api import skip_work_item
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status

from camac.core.models import HistoryActionConfig
from camac.instance.domain_logic import WithdrawalLogic


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


@pytest.mark.parametrize(
    "instance_state__name,role__name,is_applicant,is_paper,has_permission",
    [
        ("subm", "Applicant", True, False, True),
        ("subm", "Municipality", False, True, True),
        ("subm", "Municipality", False, False, False),  # not paper instance
        ("decision", "Applicant", True, False, False),  # wrong instance state
        ("subm", "Support", True, False, False),  # wrong role
        ("subm", "Applicant", False, False, False),  # not an applicant
    ],
)
def test_has_permission(
    db,
    admin_user,
    applicant_factory,
    caluma_admin_user,
    group,
    has_permission,
    is_applicant,
    is_paper,
    so_instance,
):
    if is_applicant:
        applicant_factory(instance=so_instance, invitee=admin_user)

    if is_paper:
        save_answer(
            document=so_instance.case.document,
            question=Question.objects.get(pk="is-paper"),
            value="is-paper-yes",
            user=caluma_admin_user,
        )

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


@pytest.mark.freeze("2024-04-15")
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
