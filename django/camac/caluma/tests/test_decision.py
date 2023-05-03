import pytest
from caluma.caluma_core.events import send_event
from caluma.caluma_workflow.events import post_complete_work_item
from caluma.caluma_workflow.models import Workflow, WorkItem
from django.core.management import call_command

from camac.constants.kt_bern import (
    DECISION_TYPE_BUILDING_PERMIT,
    DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
    DECISIONS_ABGELEHNT,
    DECISIONS_BEWILLIGT,
)
from camac.instance.models import HistoryEntryT, Instance
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
    "workflow,decision,decision_type,expected_instance_state,expected_text",
    [
        (
            "building-permit",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "sb1",
            "Bauentscheid verfügt",
        ),
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_BUILDING_PERMIT,
            "finished",
            "Bauentscheid verfügt",
        ),
        (
            "building-permit",
            DECISIONS_ABGELEHNT,
            DECISION_TYPE_CONSTRUCTION_TEE_WITH_RESTORATION,
            "sb1",
            "Bauentscheid verfügt",
        ),
        (
            "migrated",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "finished",
            "Beurteilung abgeschlossen",
        ),
        (
            "preliminary-clarification",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "evaluated",
            "Beurteilung abgeschlossen",
        ),
        (
            "internal",
            DECISIONS_BEWILLIGT,
            DECISION_TYPE_BUILDING_PERMIT,
            "finished_internal",
            "Beurteilung abgeschlossen",
        ),
    ],
)
def test_complete_decision(
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
):
    instance_state_factory(name=expected_instance_state)

    application_settings["CALUMA"]["DECISION_TASK"] = "decision"
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

    be_instance.case.workflow = Workflow.objects.get(pk=workflow)
    be_instance.case.save()

    work_item = decision_factory(decision=decision, decision_type=decision_type)

    if workflow == "internal":
        ebau_number_work_item = work_item_factory(case=be_instance.case)
        application_settings["CALUMA"][
            "EBAU_NUMBER_TASK"
        ] = ebau_number_work_item.task_id

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
    previous_instance_state,
    settings,
):
    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_ebau_number_form.json")
    )

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

    if expect_copy:
        new_instance = Instance.objects.get(
            case__document__source=instance.case.document
        )

        assert new_instance.case.meta["is-rejected-appeal"]
        assert (
            new_instance.case.meta["ebau-number"] == instance.case.meta["ebau-number"]
        )
        assert new_instance.instance_state.name == "circulation_init"
