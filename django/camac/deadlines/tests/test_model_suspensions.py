import pytest
from django.urls import reverse
from django.utils.translation import gettext as _
from rest_framework import status

from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.deadlines import models
from camac.permissions import api as permissions_api
from camac.user.factories import GroupFactory, UserFactory


@pytest.mark.parametrize(
    "reason_type,expected_reason,expected_formatted_reason",
    [
        (
            models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL.value,
            models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL.value,
            models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL.label,
        ),
        (
            models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND.value,
            models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND.value,
            models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND.label,
        ),
    ],
)
def test_suspensions_reason_formatted(
    db,
    service,
    instance,
    instance_deadline_factory,
    suspension_factory,
    reason_type,
    expected_reason,
    expected_formatted_reason,
    disable_deadline_side_effects,
):
    """Test the formatted reason for suspensions."""
    deadline = instance_deadline_factory(instance=instance, service=service)
    suspension = suspension_factory(
        deadline=deadline,
        reason=reason_type,
        remark="Some remark",
    )

    assert suspension.reason == expected_reason
    assert suspension.reason_formatted == expected_formatted_reason
    assert suspension.remark == "Some remark"


@pytest.mark.parametrize(
    "author_type,expected_author",
    [
        ("user", ("Test", "User")),
        ("group", "Test Group"),
        ("none", _("Automatic")),
    ],
)
def test_suspensions_author_formatted(
    db,
    service,
    instance,
    instance_deadline_factory,
    suspension_factory,
    author_type,
    expected_author,
    disable_deadline_side_effects,
):
    """Test the formatted author for suspensions."""
    deadline = instance_deadline_factory(instance=instance, service=service)
    suspension = suspension_factory(
        deadline=deadline,
        group=GroupFactory(name=expected_author) if author_type == "group" else None,
        user=UserFactory(name=expected_author[0], surname=expected_author[1])
        if author_type == "user"
        else None,
    )

    if author_type == "user":
        assert (
            suspension.author_formatted == f"{expected_author[0]} {expected_author[1]}"
        )
    else:
        assert suspension.author_formatted == expected_author


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_count",
    [
        ("distribution-service", "service-lead", "service", 0),
        ("lead-authority", "municipality-lead", "municipality", 2),
        ("distribution-service", "service-lead", ARE_SERVICE_GROUP, 0),
        ("distribution-service", "service-lead", "service-afb", 0),
    ],
)
def test_suspension_list_default(
    db,
    admin_client,
    gr_instance,
    instance_deadline_factory,
    suspension_factory,
    instance_factory,
    caluma_case_factory,
    expected_count,
    service,
    service_factory,
    access_level,
    service_group,
    role,
    gr_deadlines_settings,
    gr_permissions_settings,
    disable_deadline_side_effects,
    settings,
    mocker,
):
    """Test the default suspension list visibility."""
    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality-lead" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality-lead",
    )

    # for other instance
    deadline_other_instance = instance_deadline_factory(
        instance=instance_factory(case=caluma_case_factory()), service=service
    )
    suspension_factory.create_batch(2, deadline=deadline_other_instance)

    # for other service
    other_service = service_factory()
    deadline_other_service = instance_deadline_factory(
        instance=gr_instance, service=other_service
    )
    suspension_factory.create_batch(2, deadline=deadline_other_service)

    # for current service/instance
    deadline_current = instance_deadline_factory(instance=gr_instance, service=service)
    instance_suspensions = suspension_factory.create_batch(2, deadline=deadline_current)

    url = reverse("suspensions-list")
    response = admin_client.get(url, {"filter[deadline]": deadline_current.pk})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count

    if expected_count > 0:
        assert set([entry["id"] for entry in response.data]) == set(
            [str(entry.pk) for entry in instance_suspensions]
        )


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_count",
    [
        ("lead-authority", "municipality-lead", "municipality", 2),
        ("distribution-service", "service-lead", "service", 0),
        ("distribution-service", "service-lead", ARE_SERVICE_GROUP, 2),
        ("distribution-service", "service-lead", "service-afb", 0),
    ],
)
def test_suspension_list_gr(
    db,
    admin_client,
    gr_instance,
    instance_deadline_factory,
    suspension_factory,
    instance_factory,
    caluma_case_factory,
    expected_count,
    service,
    service_factory,
    access_level,
    service_group,
    role,
    gr_permissions_settings,
    gr_deadlines_settings,
    set_application_gr,
    disable_deadline_side_effects,
    mocker,
):
    """Test the suspension list visibility for GR."""
    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality-lead" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality-lead",
    )

    # for other instance
    deadline_other_instance = instance_deadline_factory(
        instance=instance_factory(case=caluma_case_factory()), service=service
    )
    suspension_factory.create_batch(2, deadline=deadline_other_instance)

    # for other service
    other_service = service_factory()
    deadline_other_service = instance_deadline_factory(
        instance=gr_instance, service=other_service
    )
    suspension_factory.create_batch(2, deadline=deadline_other_service)

    # for current service/instance
    deadline_current = instance_deadline_factory(instance=gr_instance, service=service)
    instance_suspensions = suspension_factory.create_batch(2, deadline=deadline_current)

    url = reverse("suspensions-list")
    response = admin_client.get(url, {"filter[deadline]": deadline_current.pk})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count

    if expected_count > 0:
        assert set([entry["id"] for entry in response.data]) == set(
            [str(entry.pk) for entry in instance_suspensions]
        )


@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,create_for_service,expected_count",
    [
        ("lead-authority", "municipality-lead", "municipality", "self", 2),
        ("distribution-service", "service-lead", "service", "self", 0),
        ("distribution-service", "service-lead", ARE_SERVICE_GROUP, "self", 0),
        ("distribution-service", "service-lead", "service-afb", "self", 2),
        ("distribution-service", "service-lead", "service-cantonal", "self", 0),
        ("distribution-service", "service-lead", "service-cantonal", "afb", 2),
        ("distribution-service", "service-lead", "service", "parent", 0),
    ],
)
def test_suspension_list_ag(
    db,
    admin_client,
    ag_instance,
    instance_deadline_factory,
    suspension_factory,
    instance_factory,
    caluma_case_factory,
    expected_count,
    service,
    service_factory,
    access_level,
    service_group,
    role,
    ag_permissions_settings,
    ag_deadlines_settings,
    set_application_ag,
    disable_deadline_side_effects,
    create_for_service,
    mocker,
):
    """Test the suspension list visibility for AG."""
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality-lead" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality-lead",
    )
    service_afb = service_factory(slug="afb", service_group__name="service-afb")
    other_service = service_factory()

    # check for who the deadline/suspensions are created
    if create_for_service == "afb":
        deadline_service = service_afb
    elif create_for_service == "parent":
        deadline_service = service_factory()
        service.service_parent = deadline_service
        service.save()
    else:
        deadline_service = service

    # for other instance
    deadline_other_instance = instance_deadline_factory(
        instance=instance_factory(case=caluma_case_factory()), service=deadline_service
    )
    suspension_factory.create_batch(2, deadline=deadline_other_instance)

    # for other service
    deadline_other_service = instance_deadline_factory(
        instance=ag_instance, service=other_service
    )
    suspension_factory.create_batch(2, deadline=deadline_other_service)

    # for current service/instance
    deadline = instance_deadline_factory(instance=ag_instance, service=deadline_service)
    instance_suspensions = suspension_factory.create_batch(2, deadline=deadline)

    url = reverse("suspensions-list")
    response = admin_client.get(url, {"filter[deadline]": deadline.pk})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count

    if expected_count > 0:
        assert set([entry["id"] for entry in response.data]) == set(
            [str(entry.pk) for entry in instance_suspensions]
        )


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_status",
    [
        # municipality can create suspensions
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            status.HTTP_201_CREATED,
        ),
        # in GR also the ARE can create suspensions
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            status.HTTP_201_CREATED,
        ),
        # other services can not create suspensions
        ("distribution-service", "service-lead", "service", status.HTTP_403_FORBIDDEN),
        (
            "distribution-service",
            "service-lead",
            "service-afb",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_suspension_creation_gr(
    db,
    admin_client,
    expected_status,
    gr_instance,
    service,
    access_level,
    service_group,
    role,
    instance_deadline_factory,
    service_factory,
    set_application_gr,
    gr_permissions_settings,
    gr_deadlines_settings,
    mocker,
):
    """Test the suspension creation for GR."""
    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality-lead" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality-lead",
    )

    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
    )

    data = {
        "type": "suspensions",
        "id": None,
        "attributes": {
            "start_date": "2023-01-01",
            "end_date": "2023-01-02",
        },
        "relationships": {
            "deadline": {
                "data": {"type": "instance-deadlines", "id": str(deadline.pk)},
            },
        },
    }

    response = admin_client.post(reverse("suspensions-list"), {"data": data})

    assert response.status_code == expected_status


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,method,reason,success",
    [
        # municipality can delete suspensions in GR
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "delete",
            "manual",
            True,
        ),
        # can also delete suspensions created by system
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "delete",
            "additional_demand",
            True,
        ),
        # in GR also the ARE can delete suspensions
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            "delete",
            "manual",
            True,
        ),
        # other services can not delete suspensions
        (
            "distribution-service",
            "service-lead",
            "service-afb",
            "delete",
            "manual",
            False,
        ),
        ("distribution-service", "service-lead", "service", "delete", "manual", False),
        # municipality can update suspensions in GR
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "patch",
            "manual",
            True,
        ),
        # in GR also the ARE can update suspensions
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            "patch",
            "manual",
            True,
        ),
        # other services can not update suspensions
        ("distribution-service", "service-lead", "service", "patch", "manual", False),
        (
            "distribution-service",
            "service-lead",
            "service-afb",
            "patch",
            "manual",
            False,
        ),
    ],
)
def test_suspension_deletion_and_update_gr(
    db,
    admin_client,
    instance_deadline_factory,
    suspension_factory,
    access_level,
    service,
    service_group,
    role,
    service_factory,
    gr_instance,
    method,
    reason,
    success,
    set_application_gr,
    gr_permissions_settings,
    gr_deadlines_settings,
    mocker,
):
    """Test the suspension deletion and update for GR."""
    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality-lead" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality-lead",
    )

    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
    )
    suspension = suspension_factory(
        deadline=deadline,
        start_date="2023-01-01",
        reason=models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_ADDITIONAL_DEMAND
        if reason == "additional_demand"
        else models.Suspension.SuspensionReasonChoices.SUSPENSION_TYPE_MANUAL,
    )

    data = (
        {
            "data": {
                "type": "suspensions",
                "id": str(suspension.pk),
                "attributes": {
                    "reason-text": "test reason",
                    "start-date": "2023-02-02",
                },
                "relationships": {
                    "deadline": {
                        "data": {"type": "instance-deadlines", "id": str(deadline.pk)},
                    },
                },
            }
        }
        if method == "patch"
        else {}
    )

    response = getattr(admin_client, method)(
        reverse("suspensions-detail", args=[suspension.pk]),
        data,
    )

    if success:
        assert (
            response.status_code == status.HTTP_200_OK
            if method == "patch"
            else status.HTTP_204_NO_CONTENT
        )
        if method == "patch":
            suspension.refresh_from_db()
            assert suspension.start_date.isoformat() == "2023-02-02"

    else:
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_403_FORBIDDEN,
        ]


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name",
    [
        ("lead-authority", "municipality-lead", "municipality"),
    ],
)
@pytest.mark.parametrize(
    "test_case,error",
    [
        ("ok", False),
        ("date_order", _("End date can not be before start date.")),
    ],
)
def test_suspension_save_validation_gr(
    db,
    admin_client,
    instance_deadline_factory,
    suspension_factory,
    access_level,
    service,
    service_group,
    role,
    service_factory,
    gr_instance,
    test_case,
    error,
    set_application_gr,
    gr_permissions_settings,
    gr_deadlines_settings,
    mocker,
):
    """Test the suspension save validation."""
    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality-lead" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality-lead",
    )

    deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
    )
    suspension_factory(
        deadline=deadline,
        start_date="2023-02-10",
        end_date="2023-02-15",
    )
    suspension = suspension_factory(
        deadline=deadline,
        start_date="2023-01-01",
    )

    post_attributes = {}
    if test_case == "ok":
        post_attributes = {
            "reason-text": test_case,
            "start_date": "2023-02-02",
            "end_date": "2023-02-03",
        }
    elif test_case == "date_order":
        post_attributes = {
            "reason-text": test_case,
            "start_date": "2023-02-10",
            "end_date": "2023-02-09",
        }

    data = {
        "data": {
            "type": "suspensions",
            "id": str(suspension.pk),
            "attributes": post_attributes,
            "relationships": {
                "deadline": {
                    "data": {"type": "instance-deadlines", "id": str(deadline.pk)},
                },
            },
        }
    }

    response = getattr(admin_client, "patch")(
        reverse("suspensions-detail", args=[suspension.pk]),
        data,
    )

    if not error:
        assert response.status_code == status.HTTP_200_OK
    else:
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.json()["errors"][0]["detail"] == error


def test_suspension_queryset_status(
    db,
    service,
    instance_deadline_factory,
    suspension_factory,
    instance_factory,
    disable_deadline_side_effects,
):
    instance = instance_factory()
    deadline = instance_deadline_factory(instance=instance, service=service)

    # suspension for other instance will be ignored.
    suspension_factory(
        deadline=instance_deadline_factory(
            instance=instance_factory(), service=service
        ),
        start_date="2023-01-01",
        end_date="2023-02-01",
    )

    # create closed and open suspensions.
    closed_suspensions = [
        suspension_factory(
            deadline=deadline, start_date="2023-01-01", end_date="2023-02-01"
        ),
        suspension_factory(
            deadline=deadline, start_date="2023-01-01", end_date="2023-02-01"
        ),
    ]
    open_suspensions = [
        suspension_factory(deadline=deadline, start_date="2023-01-01", end_date=None),
        suspension_factory(deadline=deadline, start_date="2023-01-01", end_date=None),
    ]

    assert set([s.pk for s in closed_suspensions]) == set(
        deadline.suspensions.only_closed().values_list("pk", flat=True)
    )
    assert set([s.pk for s in open_suspensions]) == set(
        deadline.suspensions.only_open().values_list("pk", flat=True)
    )
