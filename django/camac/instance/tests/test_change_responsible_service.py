import pytest
from caluma.caluma_workflow import api as workflow_api, models as caluma_workflow_models
from django.urls import reverse
from rest_framework import status

from camac.ech0211.models import Message
from camac.instance.models import HistoryEntry
from camac.permissions import api as permissions_api
from camac.permissions.switcher import PERMISSION_MODE


@pytest.mark.parametrize("role__name", ["Municipality", "Support"])
@pytest.mark.parametrize(
    "service_type,expected_status",
    [
        ("municipality", status.HTTP_204_NO_CONTENT),
        ("construction_control", status.HTTP_204_NO_CONTENT),
        ("invalidtype", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_change_responsible_service(
    db,
    admin_client,
    admin_user,
    be_instance,
    be_ech0211_settings,
    notification_template,
    role,
    group,
    mailoutbox,
    service_factory,
    user_factory,
    user_group_factory,
    application_settings,
    service_type,
    expected_status,
    caluma_admin_user,
    be_distribution_settings,
):
    application_settings["SHORT_NAME"] = "be"
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_SERVICE"] = {
        "template_slug": notification_template.slug,
        "recipient_types": ["leitbehoerde"],
    }

    if expected_status == status.HTTP_400_BAD_REQUEST:
        old_service = be_instance.responsible_service()
    else:
        old_service = be_instance.responsible_service(filter_type=service_type)
    new_service = service_factory()

    group.service = old_service
    group.save()

    for task_id in ["submit", "ebau-number"]:
        workflow_api.complete_work_item(
            work_item=be_instance.case.work_items.get(task_id=task_id),
            user=caluma_admin_user,
        )

    # other user is no member of the new service
    other_user = user_factory()
    # admin user is a member of the new service
    user_group_factory(user=admin_user, group__service=new_service)

    init_distribution = caluma_workflow_models.WorkItem.objects.get(
        task_id=be_distribution_settings["DISTRIBUTION_INIT_TASK"],
        case__family=be_instance.case,
    )
    init_distribution.assigned_users = [admin_user.username, other_user.username]
    init_distribution.save()

    assert (
        be_instance.case.work_items.filter(
            status="ready", addressed_groups__contains=[str(old_service.pk)]
        ).count()
        == 7
    )
    assert (
        be_instance.case.work_items.filter(
            status="ready", addressed_groups__contains=[str(new_service.pk)]
        ).count()
        == 0
    )

    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": service_type},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_204_NO_CONTENT:
        be_instance.refresh_from_db()

        # responsible service changed
        assert not be_instance.instance_services.filter(
            active=1, service=old_service
        ).exists()
        assert be_instance.responsible_service(filter_type=service_type) == new_service

        # notification was sent
        assert len(mailoutbox) == 1
        assert new_service.email in mailoutbox[0].recipients()

        # history entry was created
        history = HistoryEntry.objects.filter(instance=be_instance).last()
        assert (
            history.trans.get(language="de").title
            == f"Neue Leitbehörde: {new_service.trans.get(language='de').name}"
        )

        # caluma work items are reassigned
        assert (
            be_instance.case.work_items.filter(
                status="ready", addressed_groups__contains=[str(old_service.pk)]
            ).count()
            == 0
        )
        assert (
            be_instance.case.work_items.filter(
                status="ready", addressed_groups__contains=[str(new_service.pk)]
            ).count()
            == 7
        )

        assert caluma_workflow_models.WorkItem.objects.filter(
            task_id=be_distribution_settings["INQUIRY_CREATE_TASK"],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            addressed_groups__overlap=[str(new_service.pk)],
        ).exists()

        assert not caluma_workflow_models.WorkItem.objects.filter(
            task_id__in=[
                be_distribution_settings["INQUIRY_CREATE_TASK"],
                be_distribution_settings["INQUIRY_REDO_TASK"],
            ],
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            addressed_groups__overlap=[str(old_service.pk)],
        ).exists()

        # assigned users are filtered
        init_distribution.refresh_from_db()
        assert admin_user.username in init_distribution.assigned_users
        assert other_user.username not in init_distribution.assigned_users
        if service_type == "municipality":
            assert Message.objects.count() == 1
        else:
            assert Message.objects.count() == 0
    elif expected_status == status.HTTP_400_BAD_REQUEST:
        assert (
            response.data[0]["detail"]
            == f"{service_type} is not a valid service type - valid types are: municipality, construction_control"
        )


@pytest.mark.parametrize("role__name", ["municipality-lead"])
@pytest.mark.parametrize(
    "access_level_name,change_to_municipality,expected_status",
    [
        ("lead-authority", True, status.HTTP_204_NO_CONTENT),
        ("lead-authority", False, status.HTTP_204_NO_CONTENT),
        ("involved-authority", False, status.HTTP_403_FORBIDDEN),
    ],
)
def test_change_responsible_service_with_permission_module(
    db,
    admin_client,
    be_instance,
    be_permissions_settings,
    access_level_factory,
    service,
    access_level_name,
    change_to_municipality,
    expected_status,
    service_factory,
    instance_state_factory,
    disable_ech0211_settings,
):
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    be_instance.instance_state = instance_state_factory(name="subm")
    be_instance.save()

    access_levels = {
        "lead-authority": access_level_factory(pk="lead-authority"),
        "involved-authority": access_level_factory(pk="involved-authority"),
    }

    permissions_api.grant(
        be_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_levels[access_level_name],
        service=service,
    )
    new_service = (
        service_factory(service_group__name="municipality")
        if change_to_municipality
        else service_factory()
    )
    response = admin_client.post(
        reverse("instance-change-responsible-service", args=[be_instance.pk]),
        {
            "data": {
                "type": "instance-change-responsible-services",
                "attributes": {"service-type": "municipality"},
                "relationships": {
                    "to": {"data": {"id": new_service.pk, "type": "services"}}
                },
            }
        },
    )
    assert response.status_code == expected_status
    if change_to_municipality:
        be_instance.case.document.answers.filter(
            question_id="gemeinde"
        ).first().value == new_service.pk
