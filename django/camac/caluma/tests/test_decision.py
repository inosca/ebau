import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_form.factories import FormFactory
from caluma.caluma_form.models import Question
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import Workflow, WorkItem
from django.core.management import call_command

from camac.core.models import HistoryActionConfig
from camac.instance.domain_logic import DecisionLogic
from camac.instance.models import HistoryEntryT, Instance, InstanceState
from camac.instance.utils import copy_instance


@pytest.fixture
def construction_control(instance_service_factory, be_instance, service_factory):
    instance_service_factory(
        instance=be_instance,
        service=service_factory(
            trans__name="Leitbehörde Bern",
            trans__language="de",
            service_group__name="municipality",
        ),
        active=1,
    )

    return service_factory(
        trans__name="Baukontrolle Bern",
        trans__language="de",
        service_group__name="construction-control",
    )


@pytest.mark.parametrize(
    "decision,expected_instance_state,expected_text",
    [
        (
            "APPROVED",
            "construction-acceptance",
            "Bauentscheid verfügt",
        ),
        (
            "REJECTED",
            "finished",
            "Bauentscheid verfügt",
        ),
    ],
)
def test_complete_decision(
    db,
    gr_instance,
    caluma_admin_user,
    mailoutbox,
    notification_template,
    work_item_factory,
    document_factory,
    question_factory,
    instance_state_factory,
    decision,
    decision_settings,
    expected_instance_state,
    expected_text,
    settings,
    gr_decision_settings,
    gr_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_gr"
    instance_state_factory(name=expected_instance_state)

    settings.APPLICATION["NOTIFICATIONS"] = {}

    gr_instance.case.workflow = Workflow.objects.get(pk="building-permit")
    gr_instance.case.save()

    work_item = work_item_factory(
        case=gr_instance.case,
        task_id=decision_settings["TASK"],
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form_id="decision"),
    )
    decision_question = question_factory(
        slug=decision_settings["QUESTIONS"]["DECISION"],
        label="Entscheid",
        type=Question.TYPE_TEXT,
    )

    work_item.document.answers.create(
        question=decision_question,
        value=decision_settings["ANSWERS"]["DECISION"][decision],
    )

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    gr_instance.refresh_from_db()

    assert gr_instance.instance_state.name == expected_instance_state
    assert HistoryEntryT.objects.filter(
        history_entry__instance=gr_instance, title=expected_text, language="de"
    ).exists()


@pytest.mark.parametrize(
    "workflow,decision,decision_type,expected_instance_state,expected_text",
    [
        (
            "building-permit",
            "APPROVED",
            "BUILDING_PERMIT",
            "sb1",
            "Bauentscheid verfügt",
        ),
        (
            "building-permit",
            "REJECTED",
            "BUILDING_PERMIT",
            "finished",
            "Bauentscheid verfügt",
        ),
        (
            "building-permit",
            "REJECTED",
            "CONSTRUCTION_TEE_WITH_RESTORATION",
            "sb1",
            "Bauentscheid verfügt",
        ),
        (
            "migrated",
            "APPROVED",
            "BUILDING_PERMIT",
            "finished",
            "Beurteilung abgeschlossen",
        ),
        (
            "preliminary-clarification",
            "POSITIVE",
            "BUILDING_PERMIT",
            "evaluated",
            "Beurteilung abgeschlossen",
        ),
        (
            "internal",
            "APPROVED",
            "BUILDING_PERMIT",
            "finished_internal",
            "Beurteilung abgeschlossen",
        ),
    ],
)
def test_complete_decision_be(
    db,
    be_instance,
    caluma_admin_user,
    application_settings,
    mailoutbox,
    notification_template,
    work_item_factory,
    instance_state_factory,
    workflow,
    decision,
    decision_type,
    expected_instance_state,
    expected_text,
    multilang,
    use_instance_service,
    decision_factory,
    construction_control,
    settings,
    be_decision_settings,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    application_settings["NOTIFICATIONS"] = {
        "DECISION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            }
        ],
        "DECISION_PRELIMINARY_CLARIFICATION": [
            {
                "template_slug": notification_template.slug,
                "recipient_types": ["applicant"],
            }
        ],
    }

    instance_state_factory(name=expected_instance_state)

    be_instance.case.workflow = Workflow.objects.get(pk=workflow)
    be_instance.case.save()

    work_item = decision_factory(
        decision=be_decision_settings["ANSWERS"]["DECISION"][decision],
        decision_type=be_decision_settings["ANSWERS"]["APPROVAL_TYPE"][decision_type],
    )

    if workflow == "internal":
        ebau_number_work_item = work_item_factory(case=be_instance.case)
        application_settings["CALUMA"]["EBAU_NUMBER_TASK"] = (
            ebau_number_work_item.task_id
        )

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    be_instance.refresh_from_db()

    assert be_instance.instance_state.name == expected_instance_state
    assert len(mailoutbox) == 1
    assert HistoryEntryT.objects.filter(
        history_entry__instance=be_instance, title=expected_text, language="de"
    ).exists()

    if expected_instance_state == "sb1":
        assert be_instance.responsible_service() == construction_control

    if workflow == "internal":
        ebau_number_work_item.refresh_from_db()
        assert ebau_number_work_item.status == WorkItem.STATUS_SKIPPED


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "previous_instance_state,expected_instance_state,decision,expect_copy",
    [
        ("sb1", "sb1", "CONFIRMED", False),
        ("sb1", "finished", "CHANGED", False),
        ("sb1", "finished", "REJECTED", True),
        ("finished", "finished", "CONFIRMED", False),
        ("finished", "sb1", "CHANGED", False),
        ("finished", "finished", "REJECTED", True),
    ],
)
def test_complete_decision_appeal(
    db,
    admin_user,
    be_appeal_settings,
    be_instance,
    caluma_admin_user,
    construction_control,
    decision_factory,
    decision,
    expect_copy,
    expected_instance_state,
    instance_state_factory,
    mailoutbox,
    notification_template,
    previous_instance_state,
    settings,
    application_settings,
    be_decision_settings,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_ebau_number_form.json")
    )

    be_appeal_settings["NOTIFICATIONS"]["APPEAL_DECISION"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["leitbehoerde"],
        }
    ]

    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    instance_state_factory(name="circulation_init")

    if expected_instance_state != previous_instance_state:
        instance_state_factory(name=expected_instance_state)

    be_instance.previous_instance_state = instance_state_factory(
        name=previous_instance_state
    )
    be_instance.save()

    be_instance.case.workflow = Workflow.objects.get(pk="building-permit")
    be_instance.case.meta.update({"has-appeal": True})
    be_instance.case.save()

    instance = copy_instance(
        instance=be_instance,
        group=admin_user.groups.first(),
        user=admin_user,
        caluma_user=caluma_admin_user,
        new_meta={"ebau-number": "2023-123", "is-appeal": True},
    )

    work_item = decision_factory(
        instance, be_appeal_settings["ANSWERS"]["DECISION"][decision]
    )

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    instance.refresh_from_db()

    assert instance.instance_state.name == expected_instance_state

    assert len(mailoutbox) == 1
    assert notification_template.subject in mailoutbox[0].subject

    if expect_copy:
        new_instance = Instance.objects.get(
            case__document__source=instance.case.document
        )

        assert new_instance.case.meta["is-rejected-appeal"]
        assert (
            new_instance.case.meta["ebau-number"] == instance.case.meta["ebau-number"]
        )
        assert new_instance.instance_state.name == "circulation_init"


@pytest.mark.parametrize(
    "instance_state__name,decision,bauabschlag,expected",
    [
        ("decision", "APPROVED", None, True),
        ("decision", "PARTIALLY_APPROVED", "MIT_WIEDERHERSTELLUNG", True),
        ("decision", "PARTIALLY_APPROVED", "OHNE_WIEDERHERSTELLUNG", True),
        ("decision", "REJECTED", "MIT_WIEDERHERSTELLUNG", True),
        ("decision", "REJECTED", "OHNE_WIEDERHERSTELLUNG", False),
        ("decision", "WITHDRAWAL", None, False),
        # If instance state is withdrawn, never continue
        ("withdrawal", "WITHDRAWAL", None, False),
        ("withdrawal", "APPROVED", None, False),
    ],
)
def test_should_continue_after_decision_so(
    db,
    document_factory,
    question_factory,
    so_decision_settings,
    task_factory,
    work_item_factory,
    decision,
    bauabschlag,
    expected,
    instance,
):
    work_item = work_item_factory(
        task=task_factory(slug=so_decision_settings["TASK"]),
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form=FormFactory(slug="decision")),
    )

    work_item.document.answers.create(
        question=question_factory(slug=so_decision_settings["QUESTIONS"]["DECISION"]),
        value=so_decision_settings["ANSWERS"]["DECISION"][decision],
    )

    if bauabschlag:
        work_item.document.answers.create(
            question=question_factory(
                slug=so_decision_settings["QUESTIONS"]["BAUABSCHLAG"]
            ),
            value=so_decision_settings["ANSWERS"]["BAUABSCHLAG"][bauabschlag],
        )

    DecisionLogic.should_continue_after_decision_so(instance, work_item) == expected


@pytest.mark.parametrize("instance_state__name", ["withdrawal"])
def test_complete_decision_withdrawn(
    db,
    caluma_admin_user,
    document_factory,
    instance_state_factory,
    question_factory,
    so_decision_settings,
    so_instance,
    withdrawal_settings,
    work_item_factory,
    disable_ech0211_settings,
):
    instance_state_factory(name=withdrawal_settings["INSTANCE_STATE_CONFIRMED"])

    work_item = work_item_factory(
        case=so_instance.case,
        task_id=so_decision_settings["TASK"],
        status=WorkItem.STATUS_COMPLETED,
        document=document_factory(form=FormFactory(slug="decision")),
    )

    work_item.document.answers.create(
        question=question_factory(slug=so_decision_settings["QUESTIONS"]["DECISION"]),
        value=so_decision_settings["ANSWERS"]["DECISION"]["WITHDRAWAL"],
    )

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    so_instance.refresh_from_db()

    assert so_instance.instance_state.name == "withdrawn"

    assert (
        so_instance.history.filter(history_type=HistoryActionConfig.HISTORY_TYPE_STATUS)
        .latest("created_at")
        .get_trans_attr("title")
        == "Rückzug bestätigt"
    )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "previous_instance_state,expected_instance_state,decision,expect_copy,expected_copy_instance_state",
    [
        (
            "construction-monitoring",
            "construction-monitoring",
            "CONFIRMED",
            False,
            None,
        ),
        ("finished", "finished", "CONFIRMED", False, None),
        ("construction-monitoring", "finished", "CHANGED", True, "decision"),
        ("finished", "finished", "CHANGED", True, "decision"),
        ("construction-monitoring", "finished", "REJECTED", True, "subm"),
        ("finished", "finished", "REJECTED", True, "subm"),
    ],
)
def test_complete_decision_appeal_so(
    db,
    admin_user,
    so_appeal_settings,
    so_instance,
    caluma_admin_user,
    decision_factory_so,
    decision,
    expect_copy,
    expected_instance_state,
    expected_copy_instance_state,
    instance_state_factory,
    previous_instance_state,
    settings,
    application_settings,
    so_decision_settings,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_so"
    application_settings["SHORT_NAME"] = "so"

    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    instance_state_factory(name="construction-monitoring")
    instance_state_factory(name="finished")
    instance_state_factory(name="decision")

    so_instance.previous_instance_state = InstanceState.objects.get(
        name=previous_instance_state
    )
    so_instance.save()

    so_instance.case.workflow = Workflow.objects.get(pk="building-permit")
    so_instance.case.meta.update({"has-appeal": True})
    so_instance.case.save()

    instance = copy_instance(
        instance=so_instance,
        group=admin_user.groups.first(),
        user=admin_user,
        caluma_user=caluma_admin_user,
        new_meta={"dossier-number": "2024-1", "is-appeal": True},
    )

    work_item = decision_factory_so(
        instance, so_appeal_settings["ANSWERS"]["DECISION"][decision]
    )

    send_event(
        post_complete_work_item,
        sender="post_complete_work_item",
        work_item=work_item,
        user=caluma_admin_user,
        context={},
    )

    instance.refresh_from_db()

    assert instance.instance_state.name == expected_instance_state

    if expect_copy:
        new_instance = Instance.objects.get(
            case__document__source=instance.case.document
        )

        assert "is-rejected-appeal" in new_instance.case.meta
        assert "dossier-number" in new_instance.case.meta
        assert "dossier-number-sort" in new_instance.case.meta
        assert new_instance.instance_state.name == expected_copy_instance_state
