import pytest
from caluma.caluma_workflow.api import complete_work_item
from caluma.caluma_workflow.models import Case, WorkItem
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

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
    be_decision_settings,
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
                    decision=(
                        be_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
                        if instance_state_name == "sb1"
                        else be_decision_settings["ANSWERS"]["DECISION"]["REJECTED"]
                    )
                )

            complete_work_item(work_item=work_item, user=caluma_admin_user)

        be_instance.previous_instance_state = InstanceState.objects.get(
            name=previous_instance_state_name
        )
        be_instance.instance_state = InstanceState.objects.get(name=instance_state_name)
        be_instance.save()

        return be_instance

    return wrapper


@pytest.fixture
def instance_for_appeal_so(
    application_settings,
    so_appeal_settings,
    so_instance,
    instance,
    caluma_admin_user,
    decision_factory_so,
    group_factory,
    instance_state_factory,
    mocker,
    service,
    settings,
    so_decision_settings,
):
    application_settings["ACTIVE_SERVICES"] = settings.APPLICATIONS["kt_so"][
        "ACTIVE_SERVICES"
    ]

    call_command(
        "loaddata", settings.ROOT_DIR("kt_so/config/caluma_formal_exam_form.json")
    )
    call_command(
        "loaddata", settings.ROOT_DIR("kt_so/config/caluma_material_exam_form.json")
    )

    mocker.patch("camac.notification.utils.send_mail", return_value=None)

    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    instance_state_factory(name="material-exam")
    instance_state_factory(name="init-distribution")
    instance_state_factory(name="distribution")
    instance_state_factory(name="decision")
    instance_state_factory(name="construction-monitoring")
    instance_state_factory(name="finished")

    def wrapper(instance_state_name, previous_instance_state_name):
        so_instance.case.meta.update({"dossier-number": "2023-123"})
        so_instance.case.save()

        for task_id in [
            "submit",
            "formal-exam",
            "material-exam",
            "complete-distribution",
            "decision",
        ]:
            work_item = WorkItem.objects.get(
                case__family__instance=so_instance,
                task_id=task_id,
                status=WorkItem.STATUS_READY,
            )

            if task_id == "formal-exam":
                work_item.document.answers.create(
                    question_id="formelle-pruefung-resultat",
                    value="formelle-pruefung-resultat-positiv",
                )

            if task_id == "material-exam":
                work_item.document.answers.create(
                    question_id="materielle-pruefung-resultat",
                    value="materielle-pruefung-resultat-positiv",
                )

            if task_id == "decision":
                decision_factory_so(
                    decision=(
                        so_decision_settings["ANSWERS"]["DECISION"]["APPROVED"]
                        if instance_state_name == "construction-monitoring"
                        else so_decision_settings["ANSWERS"]["DECISION"]["REJECTED"]
                    )
                )

            complete_work_item(work_item=work_item, user=caluma_admin_user)

        so_instance.previous_instance_state = InstanceState.objects.get(
            name=previous_instance_state_name
        )
        so_instance.instance_state = InstanceState.objects.get(name=instance_state_name)
        so_instance.save()

        return so_instance

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
    be_appeal_settings,
    expected_instance_state,
    expected_status,
    instance_for_appeal,
    instance_state_name,
    mailoutbox,
    multilang,
    notification_template,
    previous_instance_state_name,
    role,
    settings,
    application_settings,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    be_appeal_settings["NOTIFICATIONS"]["APPEAL_SUBMITTED"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["applicant"],
        }
    ]

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

        assert len(mailoutbox) == 1
        assert notification_template.subject in mailoutbox[0].subject

        history = instance.history.exclude(history_type="notification").last()
        assert history.get_trans_attr("title", "de") == "Beschwerde eingegangen"
        assert history.get_trans_attr("title", "fr") == "Recours reçu"


@pytest.mark.parametrize(
    "role__name,previous_instance_state_name,instance_state_name,expected_instance_state,expected_status",
    [
        # Wrong role
        (
            "Service",
            "decision",
            "construction-monitoring",
            "construction-monitoring",
            status.HTTP_403_FORBIDDEN,
        ),
        # Wrong instance state
        ("Municipality", "decision", "new", "new", status.HTTP_403_FORBIDDEN),
        # Wrong previous instance state
        (
            "Municipality",
            "new",
            "finished",
            "finished",
            status.HTTP_403_FORBIDDEN,
        ),
        # Correct instance state and previous instance state
        (
            "Municipality",
            "decision",
            "construction-monitoring",
            "finished",
            status.HTTP_201_CREATED,
        ),
        (
            "Municipality",
            "decision",
            "finished",
            "finished",
            status.HTTP_201_CREATED,
        ),
    ],
)
def test_instance_appeal_so(
    db,
    active_inquiry_factory,
    admin_client,
    so_appeal_settings,
    expected_instance_state,
    expected_status,
    instance_for_appeal_so,
    instance_state_name,
    mailoutbox,
    multilang,
    notification_template,
    previous_instance_state_name,
    role,
    settings,
    application_settings,
    disable_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_so"
    application_settings["SHORT_NAME"] = "so"
    so_appeal_settings["NOTIFICATIONS"]["APPEAL_SUBMITTED"] = [
        {
            "template_slug": notification_template.slug,
            "recipient_types": ["applicant"],
        }
    ]

    instance = instance_for_appeal_so(instance_state_name, previous_instance_state_name)

    if role.name != "Municipality":
        active_inquiry_factory()

    response = admin_client.post(reverse("instance-appeal", args=[instance.pk]))

    instance.refresh_from_db()

    assert response.status_code == expected_status
    assert instance.instance_state.name == expected_instance_state

    if response.status_code == status.HTTP_201_CREATED:
        new_instance = Instance.objects.get(pk=response.json()["data"]["id"])

        # TODO: This should be completed when we implement the construction
        # monitoring process. For now, this is kept open as we still have to
        # work item to create manual work items.
        # assert instance.case.status == Case.STATUS_COMPLETED

        assert new_instance.pk != instance.pk
        assert (
            new_instance.case.meta["dossier-number"]
            != instance.case.meta["dossier-number"]
        )

        assert new_instance.instance_state.name == "subm"

        assert len(mailoutbox) == 1
        assert notification_template.subject in mailoutbox[0].subject

        history = instance.history.exclude(history_type="notification").last()
        assert history.get_trans_attr("title", "de") == "Beschwerde eingegangen"
