import pytest
from caluma.caluma_form.models import DynamicOption
from caluma.caluma_workflow.models import WorkItem
from django.urls import reverse
from rest_framework import status

from camac.core.models import InstanceService
from camac.permissions import api as permissions_api
from camac.permissions.models import InstanceACL
from camac.tests.form_utils import FormUtils
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
    celery_fake_worker,
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


def test_change_geometer_task(
    db,
    admin_client,
    be_instance,
    mocker,
    service_factory,
    instance_acl_factory,
    caluma_work_item_factory,
    attachment_factory,
    attachment_section_factory,
    instance_service_factory,
    access_level_factory,
):
    selected_geometer = service_factory()
    selected_municipality = service_factory(
        service_group__name="municipality",
    )
    instance_service_factory(
        instance=be_instance, service=selected_municipality, active=1
    )

    existing_geometer = service_factory()

    attachment_section = attachment_section_factory()
    mocker.patch(
        "camac.constants.kt_bern.ATTACHMENT_SECTION_BEILAGEN_SB1_PAPIER",
        attachment_section.pk,
    )
    attachment = attachment_factory(instance=be_instance, service=existing_geometer)
    attachment.attachment_sections.add(attachment_section)

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

    assert (
        str(selected_geometer.pk)
        in WorkItem.objects.filter(task_id="geometer").first().addressed_groups
    )
    assert be_instance.attachments.first().context["for_geometer"]

    assert ServiceRelation.objects.first().provider == selected_geometer

    class FakeTask:
        def save(*args, **kwargs): ...

    fake_task = FakeTask()
    change_geometer_task(task=fake_task)
    assert fake_task.status == "failed"


@pytest.mark.parametrize(
    "lead_authority_situation,geometer_has_changed",
    [
        ("only_active_municipality", [True, False]),
        ("only_involved_municipality", [True, False]),
        ("active_and_involved_municipalities", [True, False]),
        ("multiple_only_involved_municipalities", [False, True]),
    ],
)
def test_instance_selection_for_geometer_change(
    db,
    admin_client,
    lead_authority_situation,
    geometer_has_changed,
    be_instance,
    be_permissions_settings,
    instance_service_factory,
    instance_acl_factory,
    service_factory,
    form_utils: FormUtils,
):
    InstanceService.objects.all().delete()
    selected_geometer = service_factory()
    selected_municipality = service_factory(
        name="Selected Municipality",
        service_group__name="municipality",
    )
    selected_rsta = service_factory(
        service_group__name="district",
    )
    other_municipality_1 = service_factory(
        service_group__name="municipality",
    )
    other_municipality_2 = service_factory(
        service_group__name="municipality",
    )
    form_utils.add_answer(
        be_instance.case.document, "gemeinde", str(other_municipality_1.pk)
    )
    DynamicOption.objects.create(
        document=be_instance.case.document,
        question_id="gemeinde",
        slug=str(other_municipality_1.pk),
        label="Selected Municipality",
    )

    # Example: active lead authority: Gemeinde Thun, involved lead authority: -
    if lead_authority_situation == "only_active_municipality":
        instance_service_factory(
            instance=be_instance, service=selected_municipality, active=1
        )
    # Example: active lead authority: RSTA Thun, involved lead authority: Gemeinde Thun
    elif lead_authority_situation == "only_involved_municipality":
        instance_service_factory(
            instance=be_instance, service=selected_municipality, active=0
        )
        instance_service_factory(instance=be_instance, service=selected_rsta, active=1)
    # Example: active lead authority: Gemeinde Thun, involved lead authorities: Gemeinde Köniz, Gemeinde Bern
    elif lead_authority_situation == "active_and_involved_municipalities":
        instance_service_factory(
            instance=be_instance, service=selected_municipality, active=1
        )
        instance_service_factory(
            instance=be_instance, service=other_municipality_1, active=0
        )
        instance_service_factory(
            instance=be_instance, service=other_municipality_2, active=0
        )
    # Example: active lead authority: RSTA Thun, involved lead authorities: Gemeinde Köniz, Gemeinde Bern
    elif lead_authority_situation == "multiple_only_involved_municipalities":
        instance_service_factory(instance=be_instance, service=selected_rsta, active=1)
        instance_service_factory(
            instance=be_instance, service=other_municipality_1, active=0
        )
        instance_service_factory(
            instance=be_instance, service=other_municipality_2, active=0
        )

    existing_geometer = service_factory()

    instance_acl_factory(
        service=existing_geometer,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level__slug="geometer",
        instance=be_instance,
    )

    # Test geometer change with selected municipality
    geometer_change_task = GeometerChangeTask.objects.create(
        municipality_id=selected_municipality.pk,
        geometer_id=selected_geometer.pk,
        status="scheduled",
    )

    change_geometer_task(task=geometer_change_task)

    assert (
        InstanceACL.currently_active()
        .filter(
            instance=be_instance, service=selected_geometer, access_level="geometer"
        )
        .exists()
        == geometer_has_changed[0]
    )
    assert (
        not InstanceACL.currently_active()
        .filter(
            instance=be_instance, service=existing_geometer, access_level="geometer"
        )
        .exists()
        == geometer_has_changed[0]
    )

    InstanceACL.objects.all().delete()
    instance_acl_factory(
        service=existing_geometer,
        grant_type=permissions_api.GRANT_CHOICES.SERVICE.value,
        access_level_id="geometer",
        instance=be_instance,
    )

    # Test geometer change with other municipality
    geometer_change_task = GeometerChangeTask.objects.create(
        municipality_id=other_municipality_1.pk,
        geometer_id=selected_geometer.pk,
        status="scheduled",
    )

    change_geometer_task(task=geometer_change_task)

    assert (
        InstanceACL.currently_active()
        .filter(
            instance=be_instance, service=selected_geometer, access_level="geometer"
        )
        .exists()
        == geometer_has_changed[1]
    )
    assert (
        not InstanceACL.currently_active()
        .filter(
            instance=be_instance, service=existing_geometer, access_level="geometer"
        )
        .exists()
        == geometer_has_changed[1]
    )


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


@pytest.mark.parametrize(
    "role__name,expected_status",
    [
        ("Applicant", status.HTTP_403_FORBIDDEN),
        ("Municipality", status.HTTP_403_FORBIDDEN),
        ("Service", status.HTTP_403_FORBIDDEN),
        ("Canton", status.HTTP_403_FORBIDDEN),
        ("Support", status.HTTP_400_BAD_REQUEST),
    ],
)
def test_service_merge_municipality_permission(admin_client, expected_status):
    url = reverse("service-merge-municipality")
    response = admin_client.post(url)

    assert response.status_code == expected_status


@pytest.mark.parametrize("role__name", ["Support"])
@pytest.mark.parametrize(
    "expected_result,expected_status",
    [
        ("municipality_not_found", status.HTTP_400_BAD_REQUEST),
        ("municipality_same", status.HTTP_400_BAD_REQUEST),
        ("invalid_mapping", status.HTTP_400_BAD_REQUEST),
        ("mapping_service_not_found", status.HTTP_400_BAD_REQUEST),
        ("merge_with_self", status.HTTP_400_BAD_REQUEST),
        ("merge_empty", status.HTTP_400_BAD_REQUEST),
        ("adopt_nonempty", status.HTTP_400_BAD_REQUEST),
        ("adopt_to_service", status.HTTP_400_BAD_REQUEST),
        ("success", status.HTTP_200_OK),
    ],
)
def test_service_merge_municipality(
    admin_client,
    service_factory,
    attachment_factory,
    expected_result,
    expected_status,
):
    municipality_1 = service_factory(service_group__name="municipality")
    municipality_2 = service_factory(service_group__name="municipality")

    service_1 = service_factory(
        name=f"From service 1 merge to 4 ({municipality_1.name})"
    )
    service_1_attachment = attachment_factory(service=service_1)
    service_2 = service_factory(
        name=f"From service 2 merge to 5 ({municipality_1.name})"
    )
    service_2_attachment = attachment_factory(service=service_2)
    service_3 = service_factory(name=f"From service 3 to adopt ({municipality_1.name})")
    service_3_attachment = attachment_factory(service=service_3)
    service_4 = service_factory(name=f"To service 4 ({municipality_2.name})")
    service_4_attachment = attachment_factory(service=service_4)
    service_5 = service_factory(name=f"To service 5 ({municipality_2.name})")
    service_5_attachment = attachment_factory(service=service_5)

    # link service parents to municipalities
    service_1.service_parent = municipality_1
    service_1.save()
    service_2.service_parent = municipality_1
    service_2.save()
    service_3.service_parent = municipality_1
    service_3.save()
    service_4.service_parent = municipality_2
    service_4.save()
    service_5.service_parent = municipality_2
    service_5.save()

    # default succesful payload
    payload = {
        "data": {
            "type": "services",
            "attributes": {
                "from_municipality": municipality_1.pk,
                "to_municipality": municipality_2.pk,
                "mapping": [
                    {
                        "from_service": service_1.pk,
                        "to_service": service_4.pk,
                        "action": "merge",
                    },
                    {
                        "from_service": service_2.pk,
                        "to_service": service_5.pk,
                        "action": "merge",
                    },
                    {
                        "from_service": service_3.pk,
                        "to_service": None,
                        "action": "adopt",
                    },
                ],
            },
        }
    }

    # non-existing municipality id
    if expected_result == "municipality_not_found":
        payload["data"]["attributes"]["from_municipality"] = 9999

    # from and to municipality are the same
    elif expected_result == "municipality_same":
        payload["data"]["attributes"]["to_municipality"] = municipality_1.pk

    # mapping is invalid or incomplete in the request
    elif expected_result == "invalid_mapping":
        payload["data"]["attributes"]["mapping"] = [
            {
                "action": "merge",
            }
        ]

    # mapping contains a non-existing service id
    elif expected_result == "mapping_service_not_found":
        payload["data"]["attributes"]["mapping"][0]["from_service"] = 9999

    # merge service with itself
    elif expected_result == "merge_with_self":
        payload["data"]["attributes"]["mapping"][0]["to_service"] = service_1.pk

    # merge service with empty target
    elif expected_result == "merge_empty":
        payload["data"]["attributes"]["mapping"][0]["to_service"] = None

    # adopt service with a non-empty target
    elif expected_result == "adopt_nonempty":
        payload["data"]["attributes"]["mapping"][2]["to_service"] = service_3.pk

    # adopt a service that is not in the from municipality
    elif expected_result == "adopt_to_service":
        payload["data"]["attributes"]["mapping"][2]["from_service"] = service_4.pk

    response = admin_client.post(
        reverse("service-merge-municipality"),
        data=payload,
    )

    assert response.status_code == expected_status

    if expected_result == "success":
        json_response = response.json()

        # expected result counts of the merge result
        assert json_response["data"]["merge"] == 2
        assert json_response["data"]["adopt"] == 1

        # reload models after the command has executed raw queries
        service_1.refresh_from_db()
        service_1_attachment.refresh_from_db()
        service_2.refresh_from_db()
        service_2_attachment.refresh_from_db()
        service_3.refresh_from_db()
        service_3_attachment.refresh_from_db()
        service_4.refresh_from_db()
        service_4_attachment.refresh_from_db()
        service_5.refresh_from_db()
        service_5_attachment.refresh_from_db()

        # merged services keep their service parent
        assert service_1.service_parent.pk == municipality_1.pk
        assert service_2.service_parent.pk == municipality_1.pk

        # adopted services get the target municipality as service parent
        assert service_3.service_parent.pk == municipality_2.pk

        # unchanged services keep their service parent
        assert service_4.service_parent.pk == municipality_2.pk
        assert service_5.service_parent.pk == municipality_2.pk

        # merged services their attachments will be moved
        assert service_1_attachment.service.pk == service_4.pk
        assert service_2_attachment.service.pk == service_5.pk

        # adopted/retained/unchanged services keep their attachments as is
        assert service_3_attachment.service.pk == service_3.pk
        assert service_4_attachment.service.pk == service_4.pk
        assert service_5_attachment.service.pk == service_5.pk

        # assert service names
        assert (
            service_1.get_name() == f"From service 1 merge to 4 ({municipality_2.name})"
        )
        assert (
            service_2.get_name() == f"From service 2 merge to 5 ({municipality_2.name})"
        )
        assert (
            service_3.get_name() == f"From service 3 to adopt ({municipality_2.name})"
        )
        assert service_4.get_name() == f"To service 4 ({municipality_2.name})"
        assert service_5.get_name() == f"To service 5 ({municipality_2.name})"


@pytest.mark.parametrize("multilingual", [True, False])
@pytest.mark.parametrize("role__name", ["Municipality"])
def test_service_list_sorted(
    service_factory, admin_client, multilingual, application_settings
):
    """Ensure the returned list of services is sorted by (translated) name."""

    application_settings["IS_MULTILINGUAL"] = multilingual
    service_factory.create_batch(20)

    url = reverse("service-list")
    displayed_names = []

    for page in range(1, 6):
        response = admin_client.get(url, {"page[size]": 5, "page[number]": page})
        assert response.status_code == status.HTTP_200_OK
        data = response.json()

        for rec in data["data"]:
            displayed_names.append(rec["attributes"]["name"])

        assert sorted(displayed_names) == displayed_names, (
            f"After loading page {page}, ordering is inconsistent"
        )
