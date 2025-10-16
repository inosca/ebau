import pytest
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status

from camac.permissions import api as permissions_api
from camac.user.models import GeometerChangeTask, Service, ServiceRelation
from camac.user.tasks import change_geometer_task


@pytest.mark.parametrize(
    "role__name,size",
    [
        ("Applicant", 0),
        ("Service", 1),
        ("Canton", 1),
        ("Municipality", 1),
        ("Coordination", 1),
        ("Reader", 1),
        ("Geometer", 1),
        ("building_commission", 1),
        ("Legal-Authority", 1),
    ],
)
def test_service_list(admin_client, service, size):
    url = reverse("service-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["attributes"]["name"] == service.name
        assert json["data"][0]["attributes"]["city"] == service.get_trans_attr("city")


@pytest.mark.parametrize(
    "role__name,role_t__name,role__group_prefix,role_t__group_prefix,status_code",
    [
        ("Applicant", "Applicant", None, None, status.HTTP_404_NOT_FOUND),
        (
            "Municipality",
            "Municipality",
            "Leitung",
            "Leitung",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "Administration Leitbehörde",
            "Administration Leitbehörde",
            None,
            None,
            status.HTTP_200_OK,
        ),
        (
            "Administration Leitbehörde",
            "Administration Leitbehörde",
            "Administration",
            "Administration",
            status.HTTP_200_OK,
        ),
    ],
)
@pytest.mark.parametrize(
    "service_t__name,service_t__description,service_t__city",
    [("service name", "service name", "city name")],
)
@pytest.mark.parametrize(
    "service_t__language,role_t__language,group_t__language", [("de",) * 3, ("fr",) * 3]
)
@pytest.mark.parametrize("service__name,group__name", [(None, None)])
@pytest.mark.parametrize("multilang", [True, False])
def test_service_update(
    admin_client,
    service,
    service_t,
    group,
    group_t,
    role,
    role_t,
    status_code,
    multilang,
    application_settings,
):
    if multilang:
        application_settings["IS_MULTILINGUAL"] = True
        group_t.name = f"{role_t.name} {service_t.name}"
        group_t.save()
    else:
        group.name = f"{role_t.name} {service_t.name}"
        group.save()
    service.groups.add(group)
    url = reverse("service-detail", args=[service.pk])
    data = {
        "data": {
            "type": "services",
            "id": service.pk,
            "attributes": {
                "name": "new service name",
                "description": "new service name",
                "city": "new city name",
                "department": "new department name",
            },
        }
    }
    response = admin_client.patch(
        url, data=data, HTTP_ACCEPT_LANGUAGE=service_t.language
    )
    assert response.status_code == status_code
    if status_code == status.HTTP_200_OK:
        service.refresh_from_db()
        assert service.get_name() == "new service name"
        if role_t.group_prefix:
            assert (
                service.groups.first().get_name()
                == f"{role_t.group_prefix} new service name"
            )
        else:
            assert service.groups.first().get_name() == "new service name"
        if multilang:
            service_t.refresh_from_db()
            assert service_t.description == service_t.name == "new service name"
            assert service_t.city == "new city name"
            assert service_t.department == "new department name"
        else:
            assert service.name == "new service name"
            assert service.city == "new city name"
            assert service.department == "new department name"


@pytest.mark.parametrize(
    "role__name,allowed_roles,same_service,status_code",
    [
        ("Municipality", None, False, status.HTTP_403_FORBIDDEN),
        ("Municipality", ["Municipality"], True, status.HTTP_200_OK),
        ("Municipality", ["some other role"], True, status.HTTP_403_FORBIDDEN),
        ("Municipality", None, True, status.HTTP_200_OK),
    ],
)
def test_service_update_permissions(
    admin_client,
    service,
    service_factory,
    status_code,
    application_settings,
    allowed_roles,
    same_service,
):
    application_settings.pop("SERVICE_UPDATE_ALLOWED_ROLES", None)
    if allowed_roles:
        application_settings["SERVICE_UPDATE_ALLOWED_ROLES"] = allowed_roles

    if not same_service:
        service = service_factory()

    url = reverse("service-detail", args=[service.pk])
    response = admin_client.patch(url)

    assert response.status_code == status_code


@pytest.mark.parametrize(
    "role__name",
    ["Municipality"],
)
@pytest.mark.parametrize(
    "email,success",
    [
        ("not.an.email", False),
        (" VALID@eXample.COM", True),
        ("foo@bar.ch, nope@, x@y.com", False),
    ],
)
def test_service_update_invalid_email(
    admin_client, service, application_settings, email, success
):
    application_settings["SERVICE_UPDATE_ALLOWED_ROLES"] = ["Municipality"]
    url = reverse("service-detail", args=[service.pk])
    old_email = service.email
    data = {
        "data": {
            "type": "services",
            "id": service.pk,
            "attributes": {
                "email": email,
                "description": "service name",
                "city": "city name",
            },
        }
    }
    response = admin_client.patch(url, data=data)

    expected_status = status.HTTP_200_OK if success else status.HTTP_400_BAD_REQUEST
    assert response.status_code == expected_status
    service.refresh_from_db()
    expected_email = email.lower().strip() if success else old_email
    assert service.email == expected_email


@pytest.mark.parametrize(
    "role__name,status_code",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Coordination", status.HTTP_403_FORBIDDEN),
    ],
)
def test_service_delete(admin_client, service, status_code):
    url = reverse("service-detail", args=[service.pk])
    response = admin_client.delete(url)
    assert response.status_code == status_code


@pytest.mark.parametrize(
    "service_t__name,service_t__language", [("je ne sais pas", "fr")]
)
@pytest.mark.parametrize(
    "role__name,size", [("Applicant", 0), ("Canton", 1), ("Service", 1)]
)
def test_service_list_multilingual(admin_client, service_t, size, multilang):
    url = reverse("service-list")

    response = admin_client.get(url, HTTP_ACCEPT_LANGUAGE=service_t.language)
    assert response.status_code == status.HTTP_200_OK
    json = response.json()
    assert len(json["data"]) == size
    if size > 0:
        assert json["data"][0]["attributes"]["name"] == service_t.name


@pytest.mark.parametrize("multilang", [True, False])
@pytest.mark.parametrize(
    "name,expected_status",
    [
        ("Subservice 1", status.HTTP_201_CREATED),
        ("Existing", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_service_create(
    admin_client,
    application_settings,
    expected_status,
    multilang,
    name,
    role_t,
    role,
    service_factory,
    service,
):
    if multilang:
        application_settings["IS_MULTILINGUAL"] = True
        role_t.group_prefix = ""
        role_t.save()
        service_factory(trans__name="Existing", trans__language="de")
    else:
        role.group_prefix = ""
        role.save()
        service_factory(name="Existing")

    application_settings["SUBSERVICE_ROLES"] = [role.name]

    data = {
        "data": {
            "id": None,
            "type": "services",
            "attributes": {
                "name": name,
                "email": "test@example.com",
                "description": name,
                "city": "Musterhausen",
                "notification": True,
            },
        }
    }

    response = admin_client.post(reverse("service-list"), data=data)

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        new_service = Service.objects.get(pk=response.json()["data"]["id"])
        new_group = new_service.groups.first()

        if multilang:
            assert new_service.name is None
            assert new_group.name is None

        assert new_service.get_name() == name
        assert new_group.get_name() == name

        assert new_service.service_parent == service
        assert new_service.service_group == service.service_group


@pytest.mark.parametrize(
    "role__name,expected_status,task_already_exists",
    [
        ("Support", status.HTTP_200_OK, False),
        ("Support", status.HTTP_400_BAD_REQUEST, True),
        ("Applicant", status.HTTP_400_BAD_REQUEST, False),
        ("Municipality", status.HTTP_400_BAD_REQUEST, False),
        ("Geometer", status.HTTP_400_BAD_REQUEST, False),
    ],
)
def test_change_geometer_permission(
    admin_client,
    be_instance,
    service_factory,
    expected_status,
    task_already_exists,
    instance_acl_factory,
    access_level_factory,
    caluma_work_item_factory,
):
    selected_municipality = service_factory()
    selected_geometer = service_factory()
    existing_geometer = service_factory()

    existing_geometer = service_factory()
    ServiceRelation.objects.create(
        provider=existing_geometer,
        receiver=selected_municipality,
        function=ServiceRelation.FUNCTION_GEOMETER,
    )
    instance_acl_factory(
        user=admin_client.user,
        grant_type="GEOMETER",
        access_level=access_level_factory(slug="geometer"),
        instance=be_instance,
    )
    caluma_work_item_factory(
        task_id="geometer",
        case=be_instance.case,
        status=WorkItem.STATUS_READY,
        addressed_groups=[existing_geometer.pk],
    )

    data = {
        "data": {
            "type": "services",
            "attributes": {
                "selected_geometer_service_id": selected_geometer.pk,
            },
        }
    }

    if task_already_exists:
        GeometerChangeTask.objects.create(
            municipality_id=selected_municipality.pk,
            geometer_id=selected_geometer.pk,
            status="scheduled",
        )

    response = admin_client.post(
        reverse("service-change-geometer", args=[selected_municipality.pk]), data=data
    )
    assert response.status_code == expected_status


@pytest.mark.parametrize("geometer_exists", [True, False])
def test_change_geometer_task(
    db,
    admin_client,
    be_instance,
    geometer_exists,
    service_factory,
    instance_acl_factory,
    caluma_work_item_factory,
    access_level_factory,
):
    selected_geometer = service_factory()
    selected_municipality = service_factory()
    be_instance.services.add(selected_municipality)

    if geometer_exists:
        existing_geometer = service_factory()
        ServiceRelation.objects.create(
            provider=existing_geometer,
            receiver=selected_municipality,
            function=ServiceRelation.FUNCTION_GEOMETER,
        )
        instance_acl_factory(
            service=existing_geometer,
            grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
            access_level=access_level_factory(slug="geometer"),
            instance=be_instance,
        )
        caluma_work_item_factory(
            task_id="geometer",
            case=be_instance.case,
            status=WorkItem.STATUS_READY,
            addressed_groups=[existing_geometer.pk],
        )
    geometer_change_task = GeometerChangeTask.objects.create(
        municipality_id=selected_municipality.pk,
        geometer_id=selected_geometer.pk,
        status="scheduled",
    )

    change_geometer_task(task=geometer_change_task)

    if geometer_exists:
        assert (
            str(selected_geometer.pk)
            in WorkItem.objects.filter(task_id="geometer").first().addressed_groups
        )

    assert ServiceRelation.objects.first().provider == selected_geometer

    class FakeTask:
        def save(*args, **kwargs): ...

    fake_task = FakeTask()
    change_geometer_task(task=fake_task)
    assert fake_task.status == "failed"


@pytest.mark.parametrize(
    "role__name,task_exists,task_status,expected_status",
    [
        ("Support", False, "", status.HTTP_200_OK),
        ("Support", True, "running", status.HTTP_202_ACCEPTED),
        ("Support", True, "failed", status.HTTP_200_OK),
        ("Support", True, "completed", status.HTTP_200_OK),
        ("Support", False, "", status.HTTP_200_OK),
        ("Applicant", False, "", status.HTTP_400_BAD_REQUEST),
        ("Municipality", False, "", status.HTTP_400_BAD_REQUEST),
        ("Geometer", False, "", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_check_change_geometer_status(
    db,
    admin_client,
    task_exists,
    task_status,
    expected_status,
    service_factory,
):
    municipality = service_factory()
    geometer = service_factory()

    if task_exists:
        GeometerChangeTask.objects.create(
            municipality_id=municipality.pk,
            geometer_id=geometer.pk,
            status=task_status,
            errors="There is an error" if task_status == "failed" else "",
        )

    resp = admin_client.get(reverse("service-check-change-geometer-status"))

    if task_status == "failed":
        assert resp.data["errors"] == "There is an error"
    assert resp.status_code == expected_status
