import pytest
from caluma.caluma_workflow import models as caluma_workflow_models
from django.conf import settings
from django.urls import reverse
from pytest_lazy_fixtures import lf
from rest_framework import status

from camac.permissions import api, models
from camac.permissions.conditions import Always

R = ["read"]
W = ["write"]
RW = R + W

FULL_PERMISSIONS = {
    "case-meta": RW,
    "main": RW,
    "sb1": RW,
    "sb2": RW,
    "dossierpruefung": RW,
}


def sort_permissions(permissions):
    return {key: sorted(value) for key, value in permissions.items()}


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "instance_state__name",
    [
        "new",
        "subm",
        "rejected",
        "circulation_init",
        "circulation",
        "coordination",
        "correction",
        "sb1",
        "sb2",
        "conclusion",
        "finished",
        # preliminary clarification
        "evaluated",
        # migrated
        "in_progress",
        # internal
        "in_progress_internal",
        "finished_internal",
    ],
)
@pytest.mark.parametrize(
    "role__name,service_group__name",
    [
        ("applicant", None),
        ("municipality-lead", "municipality"),
        ("municipality-lead", "district"),
        ("municipality-readonly", "municipality"),
        ("municipality-readonly", "district"),
        ("construction-control", "construction-control"),
        ("construction-control-readonly", "construction-control"),
        ("service-lead", "service"),
        ("service-readonly", "service"),
        ("geometer-lead", "geometer"),
        ("geometer-readonly", "geometer"),
        ("support", None),
    ],
)
def test_instance_permissions_be(
    admin_client,
    be_instance,
    active_inquiry_factory,
    instance_state,
    use_caluma_form,
    snapshot,
    caluma_work_item_factory,
    caluma_document_factory,
    application_settings,
    permissions_settings,
    access_level,
):
    application_settings["ROLE_PERMISSIONS"] = settings.APPLICATIONS["kt_bern"][
        "ROLE_PERMISSIONS"
    ]
    application_settings["CALUMA"]["FORM_PERMISSIONS"] = settings.APPLICATIONS[
        "kt_bern"
    ]["CALUMA"]["FORM_PERMISSIONS"]
    application_settings["INSTANCE_PERMISSIONS"] = settings.APPLICATIONS["kt_bern"][
        "INSTANCE_PERMISSIONS"
    ]
    # SB1 additional setup
    caluma_work_item_factory(
        case=be_instance.case,
        task_id="sb1",
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        document=caluma_document_factory(form_id="sb1"),
    )
    caluma_work_item_factory(
        case=be_instance.case,
        task_id="sb1",
        status=caluma_workflow_models.WorkItem.STATUS_READY,
        document=caluma_document_factory(form_id="sb1-v2"),
    )
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [("foo", Always()), ("bar", Always())],
        "geometer": [("foo", Always()), ("bar", Always())],
    }

    active_inquiry_factory(be_instance)
    user_active_service = admin_client.user.groups.get().service
    manager = api.PermissionManager.for_anonymous()
    manager.grant(
        be_instance,
        "SERVICE",
        models.AccessLevel.objects.create(pk="geometer"),
        service=user_active_service,
    )

    response = admin_client.get(reverse("instance-detail", args=[be_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(
        sort_permissions(response.json()["data"]["meta"]["permissions"])
    )


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name", ["Coordination", "Support", "building_commission"]
)
@pytest.mark.parametrize("instance_state__name", ["ext", "circ", "redac"])
def test_instance_permissions_ur(
    admin_client,
    instance_service,
    ur_instance,
    instance_state,
    use_caluma_form,
    snapshot,
    application_settings,
):
    application_settings["CALUMA"]["FORM_PERMISSIONS"] = settings.APPLICATIONS[
        "kt_uri"
    ]["CALUMA"]["FORM_PERMISSIONS"]

    response = admin_client.get(reverse("instance-detail", args=[ur_instance.pk]))

    assert response.status_code == status.HTTP_200_OK

    snapshot.assert_match(
        sort_permissions(response.json()["data"]["meta"]["permissions"])
    )


@pytest.mark.parametrize("instance__user", [lf("admin_user")])
@pytest.mark.parametrize(
    "role__name,instance_state__name,expected_status",
    [
        ("Gemeinde", "new", status.HTTP_200_OK),
        ("Gemeinde", "circ", status.HTTP_200_OK),
        ("Gemeinde", "redac", status.HTTP_200_OK),
        ("Gemeinde", "internal", status.HTTP_200_OK),
        ("Gemeinde", "construction-monitoring", status.HTTP_200_OK),
        ("Gemeinde", "instance-completed", status.HTTP_200_OK),
        ("Gemeinde", "done", status.HTTP_200_OK),
        ("Fachstelle", "new", status.HTTP_200_OK),
        ("Fachstelle", "circ", status.HTTP_200_OK),
        ("Fachstelle", "redac", status.HTTP_200_OK),
        ("Fachstelle", "internal", status.HTTP_200_OK),
        ("Fachstelle", "construction-monitoring", status.HTTP_200_OK),
        ("Fachstelle", "instance-completed", status.HTTP_200_OK),
        ("Fachstelle", "done", status.HTTP_200_OK),
        ("Publikation", "new", status.HTTP_404_NOT_FOUND),
        ("Publikation", "circ", status.HTTP_404_NOT_FOUND),
        ("Publikation", "redac", status.HTTP_404_NOT_FOUND),
        ("Publikation", "internal", status.HTTP_404_NOT_FOUND),
        ("Support", "nfd", status.HTTP_200_OK),
    ],
)
def test_instance_permissions_sz(
    admin_client,
    sz_instance,
    instance_state,
    expected_status,
    snapshot,
    application_settings,
):
    application_settings["ROLE_PERMISSIONS"] = settings.APPLICATIONS["kt_schwyz"][
        "ROLE_PERMISSIONS"
    ]

    response = admin_client.get(reverse("instance-detail", args=[sz_instance.pk]))

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        snapshot.assert_match(
            sort_permissions(response.json()["data"]["meta"]["permissions"])
        )


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "instance_state__name,group_name,form_slug,expected_permissions",
    [
        ("new", "municipality", "main", RW),
        ("new", "construction-control", "main", []),
        ("rejected", "municipality", "main", R),
        ("rejected", "construction-control", "main", R),
        ("sb1", "municipality", "sb1", R),
        ("sb1", "construction-control", "sb1", RW),
        ("sb1", "municipality", "sb1-v2", R),
        ("sb1", "construction-control", "sb1-v2", RW),
        ("sb2", "municipality", "sb2", R),
        ("sb2", "construction-control", "sb2", RW),
    ],
)
def test_instance_paper_permissions(
    admin_client,
    admin_user,
    role,
    be_instance,
    instance_state,
    group_name,
    form_slug,
    expected_permissions,
    use_caluma_form,
    mocker,
    group_factory,
    service_factory,
    user_group_factory,
    caluma_work_item_factory,
    caluma_document_factory,
    application_settings,
    instance_service_factory,
):
    mocker.patch("camac.caluma.api.CalumaApi.is_paper", lambda s, i: True)

    groups = {
        "municipality": group_factory(role=role),
        "construction-control": group_factory(role=role),
    }

    municipality_group = groups["municipality"]
    construction_control_group = groups["construction-control"]

    for name, group in groups.items():
        user_group_factory(group=group, user=admin_user)
        instance_service_factory(instance=be_instance, service=group.service)

    application_settings["PAPER"] = {
        "ALLOWED_ROLES": {
            "SB1": [construction_control_group.role.pk],
            "SB2": [construction_control_group.role.pk],
            "DEFAULT": [municipality_group.role.pk],
        },
        "ALLOWED_SERVICE_GROUPS": {
            "SB1": [construction_control_group.service.service_group.pk],
            "SB2": [construction_control_group.service.service_group.pk],
            "DEFAULT": [municipality_group.service.service_group.pk],
        },
    }
    # SB1 additional setup
    if instance_state.name == "sb1":
        caluma_work_item_factory(
            case=be_instance.case,
            task_id="sb1",
            status=caluma_workflow_models.WorkItem.STATUS_READY,
            document=caluma_document_factory(form_id=form_slug),
        )

    response = admin_client.get(
        reverse("instance-detail", args=[be_instance.pk]),
        data={"group": groups.get(group_name).pk},
    )

    assert response.status_code == status.HTTP_200_OK
    assert sorted(response.json()["data"]["meta"]["permissions"][form_slug]) == sorted(
        expected_permissions
    )
