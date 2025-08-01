from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_gr import ARE_SERVICE_GROUP
from camac.permissions import api as permissions_api


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_count",
    [
        # services can not see any instance deadlines
        ("distribution-service", "service-lead", "service", 0),
        # municipality can see instance deadlines
        ("lead-authority", "municipality-lead", "municipality", 2),
        # ARE can see instance deadlines in GR
        ("lead-authority", "service-lead", ARE_SERVICE_GROUP, 2),
        # other services can not see instance deadlines in GR
        ("lead-authority", "service-lead", "service-afb", 0),
    ],
)
def test_instance_deadlines_list_gr(
    db,
    admin_client,
    gr_instance,
    instance_deadline_factory,
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
    disable_deadline_progression,
    mocker,
):
    """Test the instance deadlines list visibility for GR."""
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
    instance_deadline_factory.create_batch(
        2,
        instance=instance_factory(case=caluma_case_factory()),
        service=service,
    )

    # for other service
    other_service = service_factory()
    instance_deadline_factory.create_batch(
        2, instance=gr_instance, service=other_service
    )

    # for current service/instance
    instance_deadlines = instance_deadline_factory.create_batch(
        2, instance=gr_instance, service=service
    )

    url = reverse("instance-deadlines-list")
    response = admin_client.get(url, {"filter[instance]": gr_instance.pk})

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == expected_count

    if expected_count > 0:
        assert response.data[0]["id"] == str(instance_deadlines[0].pk)
        assert response.data[1]["id"] == str(instance_deadlines[1].pk)


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,expected_status",
    [
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
        (
            "distribution-service",
            "service-lead",
            "service",
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
        (
            "distribution-service",
            "service-lead",
            "service-afb",
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
    ],
)
def test_instance_deadlines_creation_gr(
    db,
    admin_client,
    expected_status,
    gr_instance,
    service,
    access_level,
    service_group,
    role,
    service_factory,
    deadline_type_factory,
    set_application_gr,
    gr_permissions_settings,
    gr_deadlines_settings,
    disable_deadline_progression,
    mocker,
):
    """Test that no role can create deadlines through the API."""
    deadline_type = deadline_type_factory()
    permissions_api.grant(
        gr_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service if role.name == "municipality" else service_factory(),
    )
    mocker.patch(
        "camac.instance.models.Instance.has_inquiry",
        return_value=role.name != "municipality",
    )

    data = {
        "type": "instance-deadlines",
        "id": None,
        "attributes": {
            "start_date": "2023-01-01",
        },
        "relationships": {
            "deadline_type": {
                "data": {
                    "type": "deadline-types",
                    "id": str(deadline_type.pk),
                },
            },
            "instance": {
                "data": {"type": "instances", "id": str(gr_instance.pk)},
            },
            "service": {
                "data": {"type": "services", "id": str(service.pk)},
            },
        },
    }

    response = admin_client.post(reverse("instance-deadlines-list"), {"data": data})

    assert response.status_code == expected_status


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,method,success",
    [
        ("lead-authority", "municipality-lead", "municipality", "delete", False),
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            "delete",
            False,
        ),
        ("distribution-service", "service-lead", "service", "delete", False),
        ("distribution-service", "service-lead", "service-afb", "delete", False),
        ("lead-authority", "municipality-lead", "municipality", "patch", True),
        ("distribution-service", "service-lead", ARE_SERVICE_GROUP, "patch", True),
        ("distribution-service", "service-lead", "service", "patch", False),
        ("distribution-service", "service-lead", "service-afb", "patch", False),
    ],
)
def test_instance_deadlines_deletion_and_update_gr(
    db,
    admin_client,
    instance_deadline_factory,
    service,
    access_level,
    role,
    service_group,
    service_factory,
    gr_instance,
    method,
    success,
    set_application_gr,
    gr_permissions_settings,
    gr_deadlines_settings,
    disable_deadline_progression,
    mocker,
):
    """Test that only municipality can update instance deadlines.

    No role can delete instance deadlines through the API.
    """
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
    instance_deadline = instance_deadline_factory(
        instance=gr_instance,
        service=service,
        start_date=None,
    )
    data = (
        {
            "data": {
                "type": "instance-deadlines",
                "id": str(instance_deadline.pk),
                "attributes": {
                    "start-date": "2023-02-02",
                },
                "relationships": {
                    "instance": {
                        "data": {"type": "instances", "id": str(gr_instance.pk)},
                    },
                    "service": {
                        "data": {"type": "services", "id": str(service.pk)},
                    },
                },
            }
        }
        if method == "patch"
        else {}
    )

    response = getattr(admin_client, method)(
        reverse("instance-deadlines-detail", args=[instance_deadline.pk]),
        data,
    )

    if success:
        assert response.status_code == status.HTTP_200_OK
        if method == "patch":
            instance_deadline.refresh_from_db()
            assert instance_deadline.start_date.isoformat() == "2023-02-02"

    else:
        assert response.status_code in [
            status.HTTP_404_NOT_FOUND,
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ]


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    "access_level__slug,role__name,service_group__name,process_deadline_date,expected_status",
    [
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "2025-12-31",
            status.HTTP_200_OK,
        ),
        (
            "distribution-service",
            "trusted-service-lead",
            "service-afb",
            "2025-12-31",
            status.HTTP_200_OK,
        ),
        (
            "distribution-service",
            "trusted-service-read",
            "service-afb",
            None,
            status.HTTP_200_OK,
        ),
        (
            "distribution-service",
            "trusted-service-read",
            "service-afb",
            "2025-12-31",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
def test_validate_process_deadline_date_ag(
    db,
    admin_client,
    instance_deadline_factory,
    service,
    access_level,
    role,
    service_group,
    service_factory,
    ag_instance,
    process_deadline_date,
    expected_status,
    set_application_ag,
    ag_permissions_settings,
    ag_deadlines_settings,
    disable_deadline_progression,
    mocker,
):
    """Test validation of process_deadline_date field for different roles and values."""
    permissions_api.grant(
        ag_instance,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level=access_level,
        service=service,
    )
    mocker.patch(
        "camac.instance.models.Instance.responsible_service",
        return_value=service,
    )

    ag_instance.case.document.form_id = "plangenehmigungsverfahren-gas"
    ag_instance.case.document.save()

    instance_deadline = instance_deadline_factory(
        instance=ag_instance,
        service=service,
        start_date=date(2023, 6, 1),
    )

    data = {
        "data": {
            "type": "instance-deadlines",
            "id": str(instance_deadline.pk),
            "attributes": {
                "process-deadline-date": process_deadline_date,
            },
            "relationships": {
                "instance": {
                    "data": {"type": "instances", "id": str(ag_instance.pk)},
                },
                "service": {
                    "data": {"type": "services", "id": str(service.pk)},
                },
            },
        }
    }

    response = admin_client.patch(
        reverse("instance-deadlines-detail", args=[instance_deadline.pk]),
        data,
    )

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK and process_deadline_date is not None:
        instance_deadline.refresh_from_db()
        assert (
            instance_deadline.process_deadline_date.isoformat() == process_deadline_date
        )
