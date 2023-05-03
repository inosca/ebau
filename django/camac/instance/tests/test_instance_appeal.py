import pytest
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import Case, WorkItem
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_bern import DECISIONS_ABGELEHNT, DECISIONS_BEWILLIGT
from camac.instance.models import Instance, InstanceState


@pytest.fixture
def instance_for_appeal(
    application_settings,
    be_appeal_settings,
    be_instance,
    caluma_admin_user,
    construction_control_for,
    decision_factory,
    instance_state_factory,
    mocker,
    service,
    settings,
):
    application_settings["ACTIVE_SERVICES"] = settings.APPLICATIONS["kt_bern"][
        "ACTIVE_SERVICES"
    ]

    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_ebau_number_form.json")
    )

    construction_control_for(service)

    mocker.patch("camac.notification.utils.send_mail", return_value=None)

    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    instance_state_factory(name="circulation_init")
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb1")
    instance_state_factory(name="conclusion")
    instance_state_factory(name="finished")

    def wrapper(instance_state_name, previous_instance_state_name):
        be_instance.case.meta.update({"ebau-number": "2023-123"})
        be_instance.case.save()

        for task_id in ["submit", "ebau-number", "complete-distribution", "decision"]:
            work_item = WorkItem.objects.get(
                case__family__instance=be_instance,
                task_id=task_id,
                status=WorkItem.STATUS_READY,
            )

            if task_id == "ebau-number":
                work_item.document.answers.create(
                    question_id="ebau-number-has-existing",
                    value="ebau-number-has-existing-yes",
                )
                work_item.document.answers.create(
                    question_id="ebau-number-existing",
                    value="2023-123",
                )

            if task_id == "decision":
                decision_factory(
                    decision=DECISIONS_BEWILLIGT
                    if instance_state_name == "sb1"
                    else DECISIONS_ABGELEHNT
                )

            complete_work_item(work_item=work_item, user=caluma_admin_user)

        be_instance.previous_instance_state = InstanceState.objects.get(
            name=previous_instance_state_name
        )
        be_instance.instance_state = InstanceState.objects.get(name=instance_state_name)
        be_instance.save()

        return be_instance

    return wrapper


def test_instance_appeal_404(db, instance, admin_client):
    response = admin_client.post(reverse("instance-appeal", args=[instance.pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "role__name,previous_instance_state_name,instance_state_name,expected_instance_state,expected_status",
    [
        # Wrong role
        ("Service", "coordination", "sb1", "sb1", status.HTTP_403_FORBIDDEN),
        # Wrong instance state
        ("Municipality", "coordination", "new", "new", status.HTTP_403_FORBIDDEN),
        # Wrong previous instance state
        (
            "Municipality",
            "conclusion",
            "finished",
            "finished",
            status.HTTP_403_FORBIDDEN,
        ),
        # Correct instance state and previous instance state
        (
            "Municipality",
            "coordination",
            "sb1",
            "finished",
            status.HTTP_201_CREATED,
        ),
        (
            "Municipality",
            "coordination",
            "finished",
            "finished",
            status.HTTP_201_CREATED,
        ),
    ],
)
def test_instance_appeal(
    db,
    active_inquiry_factory,
    admin_client,
    expected_instance_state,
    expected_status,
    instance_for_appeal,
    instance_state_name,
    multilang,
    previous_instance_state_name,
    role,
):
    instance = instance_for_appeal(instance_state_name, previous_instance_state_name)

    if role.name != "Municipality":
        active_inquiry_factory()

    response = admin_client.post(reverse("instance-appeal", args=[instance.pk]))

    instance.refresh_from_db()

    assert response.status_code == expected_status
    assert instance.instance_state.name == expected_instance_state

    if response.status_code == status.HTTP_201_CREATED:
        new_instance = Instance.objects.get(pk=response.json()["data"]["id"])

        assert instance.case.status == Case.STATUS_COMPLETED

        assert new_instance.pk != instance.pk
        assert (
            new_instance.case.meta["ebau-number"] == instance.case.meta["ebau-number"]
        )

        assert new_instance.instance_state.name == "circulation_init"

        history = instance.history.last()
        assert history.get_trans_attr("title", "de") == "Beschwerde eingegangen"
        assert history.get_trans_attr("title", "fr") == "Recours reçu"
