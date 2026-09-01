from datetime import date

import pytest
from django.urls import reverse
from rest_framework import status

from camac.constants.kt_gr import (
    ARE_SERVICE_GROUP,
    BAUBEITRAGSWESEN_FORM_PHASE_1,
    BUILDING_DEPARTMENT_SERVICE_GROUP,
)
from camac.permissions import api as permissions_api


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    (
        "access_level__slug",
        "role__name",
        "service_group__name",
        "form_slug",
        "expected_count",
    ),
    [
        # services can not see any instance deadlines
        ("distribution-service", "service-lead", "service", "baugesuch-v6", 0),
        # municipality can see instance deadlines
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "baugesuch-v6",
            2,
        ),
        # ARE can see instance deadlines in GR
        (
            "lead-authority",
            "service-lead",
            ARE_SERVICE_GROUP,
            "baugesuch-v6",
            2,
        ),
        # HBA can see inquiry deadlines for EBBW dossiers
        (
            "distribution-service",
            "service-lead",
            BUILDING_DEPARTMENT_SERVICE_GROUP,
            BAUBEITRAGSWESEN_FORM_PHASE_1,
            2,
        ),
        # other services can not see instance deadlines in GR
        ("lead-authority", "service-lead", "service-afb", "baugesuch-v6", 0),
    ],
)
@pytest.mark.django_db
def test_instance_deadlines_list_gr(
    admin_client,
    gr_instance,
    caluma_form_factory,
    instance_deadline_factory,
    instance_factory,
    caluma_case_factory,
    expected_count,
    form_slug,
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
    """Test the instance deadlines list visibility for GR."""
    gr_instance.case.family.document.form = caluma_form_factory(slug=form_slug)
    gr_instance.case.family.document.save(update_fields=["form"])

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
    data = response.json()["data"]
    assert len(data) == expected_count

    if expected_count > 0:
        assert data[0]["id"] == str(instance_deadlines[0].pk)
        assert data[1]["id"] == str(instance_deadlines[1].pk)


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    ("access_level__slug", "role__name", "service_group__name", "expected_status"),
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
@pytest.mark.django_db
def test_instance_deadlines_creation_gr(
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
    (
        "access_level__slug",
        "role__name",
        "service_group__name",
        "form_slug",
        "method",
        "expected_status",
    ),
    [
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "baugesuch-v6",
            "delete",
            status.HTTP_405_METHOD_NOT_ALLOWED,
        ),
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            "baugesuch-v6",
            "patch",
            status.HTTP_200_OK,
        ),
        (
            "lead-authority",
            "municipality-lead",
            "municipality",
            BAUBEITRAGSWESEN_FORM_PHASE_1,
            "patch",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            "baugesuch-v6",
            "patch",
            status.HTTP_200_OK,
        ),
        (
            "distribution-service",
            "service-lead",
            ARE_SERVICE_GROUP,
            BAUBEITRAGSWESEN_FORM_PHASE_1,
            "patch",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "distribution-service",
            "service-lead",
            BUILDING_DEPARTMENT_SERVICE_GROUP,
            BAUBEITRAGSWESEN_FORM_PHASE_1,
            "patch",
            status.HTTP_200_OK,
        ),
        (
            "distribution-service",
            "service-lead",
            BUILDING_DEPARTMENT_SERVICE_GROUP,
            "baugesuch-v6",
            "patch",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "distribution-service",
            "service-lead",
            "service",
            "baugesuch-v6",
            "patch",
            status.HTTP_404_NOT_FOUND,
        ),
        (
            "distribution-service",
            "service-lead",
            "service-afb",
            "baugesuch-v6",
            "patch",
            status.HTTP_404_NOT_FOUND,
        ),
    ],
)
@pytest.mark.django_db
def test_instance_deadlines_deletion_and_update_gr(
    admin_client,
    caluma_form_factory,
    instance_deadline_factory,
    service,
    access_level,
    role,
    service_group,
    service_factory,
    gr_instance,
    form_slug,
    method,
    expected_status,
    set_application_gr,
    gr_permissions_settings,
    gr_deadlines_settings,
    mocker,
):
    """Test that only allowed services can update instance deadlines.

    No role can delete instance deadlines through the API.
    """
    gr_instance.case.family.document.form = caluma_form_factory(slug=form_slug)
    gr_instance.case.family.document.save(update_fields=["form"])

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

    assert response.status_code == expected_status

    if expected_status == status.HTTP_200_OK:
        instance_deadline.refresh_from_db()
        assert instance_deadline.start_date.isoformat() == "2023-02-02"


@pytest.mark.parametrize("instance_state__name", ["subm"])
@pytest.mark.parametrize(
    (
        "access_level__slug",
        "role__name",
        "service_group__name",
        "process_deadline_date",
        "expected_status",
    ),
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
            "no-permission-test",
            "service-afb",
            None,
            status.HTTP_200_OK,
        ),
        (
            "distribution-service",
            "no-permission-test",
            "service-afb",
            "2025-12-31",
            status.HTTP_403_FORBIDDEN,
        ),
    ],
)
@pytest.mark.django_db
def test_validate_process_deadline_date_ag(
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
                "process-deadline-date-override": process_deadline_date is not None,
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
