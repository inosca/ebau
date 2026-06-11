import pytest
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.responsible.domain_logic import ResponsibleServiceDomainLogic


def test_responsible_service_list(admin_client, responsible_service):
    url = reverse("responsibleservice-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK

    json = response.json()
    assert len(json["data"]) == 1
    assert json["data"][0]["id"] == str(responsible_service.pk)


@pytest.mark.parametrize(
    "role__name,instance__user,status_code",
    [
        ("Service", lf("admin_user"), status.HTTP_201_CREATED),
        ("Municipality", lf("admin_user"), status.HTTP_201_CREATED),
        ("Coordination", lf("admin_user"), status.HTTP_201_CREATED),
        ("Applicant", lf("admin_user"), status.HTTP_403_FORBIDDEN),
        ("Geometer", lf("admin_user"), status.HTTP_201_CREATED),
        ("Legal-Authority", lf("admin_user"), status.HTTP_201_CREATED),
    ],
)
def test_responsible_service_create(
    admin_client,
    mailoutbox,
    application_settings,
    notification_template,
    instance,
    service,
    admin_user,
    status_code,
    activation,
    caluma_work_item_factory,
    caluma_case_factory,
):
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_USER"] = {
        "template_slug": notification_template.slug,
    }

    case = caluma_case_factory()
    instance.case = case
    instance.save()
    work_item = caluma_work_item_factory(
        case=case, addressed_groups=[instance.group.service.pk]
    )

    url = reverse("responsibleservice-list")

    data = {
        "data": {
            "type": "responsible-services",
            "id": None,
            "attributes": {},
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "responsible-user": {"data": {"id": instance.user.pk, "type": "users"}},
            },
        }
    }
    response = admin_client.post(url, data=data)
    assert response.status_code == status_code
    json = response.json()

    if status_code == status.HTTP_201_CREATED:
        assert (
            int(json["data"]["relationships"]["instance"]["data"]["id"])
            == instance.instance_id
        )
        work_item.refresh_from_db()
        assert work_item.assigned_users[0] == instance.user.username
        # there is no email notification sent when the user being assigned is the user making the request.
        assert len(mailoutbox) == 0


@pytest.mark.parametrize(
    "role__name,responsible_service__responsible_user,status_code",
    [
        ("Service", lf("admin_user"), status.HTTP_200_OK),
        ("Municipality", lf("admin_user"), status.HTTP_200_OK),
        ("Coordination", lf("admin_user"), status.HTTP_200_OK),
        ("Applicant", lf("admin_user"), status.HTTP_403_FORBIDDEN),
        ("Geometer", lf("admin_user"), status.HTTP_200_OK),
        ("Legal-Authority", lf("admin_user"), status.HTTP_200_OK),
    ],
)
def test_responsible_service_update(
    admin_client,
    application_settings,
    mailoutbox,
    notification_template,
    responsible_service,
    status_code,
    activation,
    service,
    instance,
    caluma_work_item_factory,
    caluma_case_factory,
    admin_user,
):
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_USER"] = {
        "template_slug": notification_template.slug,
    }

    case = caluma_case_factory()
    responsible_service.instance.case = case
    responsible_service.instance.save()
    work_item = caluma_work_item_factory(
        case=case, addressed_groups=[responsible_service.service.pk]
    )
    other_work_item = caluma_work_item_factory(
        case=caluma_case_factory(),
        addressed_groups=[responsible_service.service.pk],
        assigned_users=[],
    )

    url = reverse("responsibleservice-detail", args=[responsible_service.pk])

    data = {
        "data": {
            "type": "responsible-services",
            "id": responsible_service.pk,
            "attributes": {},
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "responsible-user": {
                    "data": {
                        "id": responsible_service.responsible_user.pk,
                        "type": "users",
                    }
                },
            },
        }
    }

    response = admin_client.patch(url, data=data)
    assert response.status_code == status_code

    if status_code == status.HTTP_200_OK:
        work_item.refresh_from_db()
        other_work_item.refresh_from_db()

        assert (
            work_item.assigned_users[0] == responsible_service.responsible_user.username
        )
        assert other_work_item.assigned_users == []
        # there is no email notification sent when the user being assigned is the user making the request.
        assert len(mailoutbox) == 0


@pytest.mark.parametrize("has_previous_responsible_user", [True, False])
def test_update_work_item_assigned_user_ag(
    db,
    ag_instance,
    application_settings,
    caluma_work_item_factory,
    has_previous_responsible_user,
    responsible_service_factory,
    service,
    user_factory,
):
    application_settings["SHORT_NAME"] = "ag"

    old_user = user_factory(username="old")
    new_user = user_factory(username="new")
    other_user = user_factory(username="other")

    responsible_service = responsible_service_factory(
        instance=ag_instance,
        service=service,
        responsible_user=new_user,
    )

    work_item_completed = caluma_work_item_factory(
        case=ag_instance.case,
        assigned_users=[other_user.username],
        status=WorkItem.STATUS_COMPLETED,
        addressed_groups=[str(service.pk)],
    )
    work_item_bypassed = caluma_work_item_factory(
        case=ag_instance.case,
        assigned_users=[],
        meta={"bypass-responsible-user": True},
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )
    work_item_bypassed_assigned = caluma_work_item_factory(
        case=ag_instance.case,
        assigned_users=[old_user.username],
        meta={"bypass-responsible-user": True},
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )
    work_item_unassigned = caluma_work_item_factory(
        case=ag_instance.case,
        assigned_users=[],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )
    work_item_assigned_other = caluma_work_item_factory(
        case=ag_instance.case,
        assigned_users=[other_user.username],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )
    work_item_assigned_old = caluma_work_item_factory(
        case=ag_instance.case,
        assigned_users=[old_user.username],
        status=WorkItem.STATUS_READY,
        addressed_groups=[str(service.pk)],
    )

    ResponsibleServiceDomainLogic.update_work_item_assigned_user(
        responsible_service, old_user if has_previous_responsible_user else None
    )

    for work_item in [
        work_item_completed,
        work_item_bypassed,
        work_item_bypassed_assigned,
        work_item_unassigned,
        work_item_assigned_other,
        work_item_assigned_old,
    ]:
        work_item.refresh_from_db()

    assert work_item_completed.assigned_users == [other_user.username]
    assert work_item_bypassed.assigned_users == []
    assert work_item_assigned_other.assigned_users == [other_user.username]

    if has_previous_responsible_user:
        assert work_item_unassigned.assigned_users == []
        assert work_item_assigned_old.assigned_users == [new_user.username]
        assert work_item_bypassed_assigned.assigned_users == [new_user.username]
    else:
        assert work_item_unassigned.assigned_users == [new_user.username]
        assert work_item_assigned_old.assigned_users == [old_user.username]
        assert work_item_bypassed_assigned.assigned_users == [old_user.username]


@pytest.mark.parametrize("is_self_assignment", [True, False])
def test_send_notification(
    db,
    application_settings,
    mailoutbox,
    notification_template,
    be_instance,
    service,
    group,
    admin_user,
    user_factory,
    responsible_service_factory,
    is_self_assignment,
):
    application_settings["NOTIFICATIONS"]["CHANGE_RESPONSIBLE_USER"] = {
        "template_slug": notification_template.slug,
    }

    assigned_user = admin_user if is_self_assignment else user_factory(username="other")

    responsible_service = responsible_service_factory(
        instance=be_instance,
        service=service,
        responsible_user=assigned_user,
    )

    ResponsibleServiceDomainLogic.send_notification(
        responsible_service, admin_user, group
    )

    if is_self_assignment:
        assert len(mailoutbox) == 0
    else:
        assert len(mailoutbox) == 1
        assert mailoutbox[0].to[0] == assigned_user.email
