import pytest
from django.core.management import call_command
from django.urls import reverse
from rest_framework import status

from camac.instance.models import Instance, InstanceState
from camac.permissions.models import AccessLevel, InstanceACL
from camac.permissions.switcher import PERMISSION_MODE


@pytest.fixture
def instance_for_copy(
    admin_client,
    application_settings,
    multilang,
    be_instance,
    caluma_admin_user,
    instance_state_factory,
    mocker,
    settings,
    use_instance_service,
    service_factory,
    instance_service_factory,
):
    call_command(
        "loaddata", settings.ROOT_DIR("kt_bern/config/caluma_ebau_number_form.json")
    )

    mocker.patch("camac.notification.utils.send_mail", return_value=None)
    instance_state_factory(name="new")
    instance_state_factory(name="subm")
    instance_state_factory(name="circulation_init")
    instance_state_factory(name="coordination")
    instance_state_factory(name="sb1")
    instance_state_factory(name="conclusion")
    instance_state_factory(name="rejected")
    instance_state_factory(name="finished")
    instance_state_factory(name="finished_internal")
    instance_state_factory(name="archived")
    instance_state_factory(name="evaluated")

    def wrapper(instance_state_name):
        be_instance.case.meta.update({"ebau-number": "2026-456"})
        be_instance.case.save()

        be_instance.instance_state = InstanceState.objects.get(name=instance_state_name)

        last_active_municipality = service_factory(
            service_group__name="municipality",
            trans__name="Last Active Leitbehörde",
            trans__language="de",
        )
        # add last active municipality to test it is copied to new instance
        be_instance.instance_services.add(
            instance_service_factory(service=last_active_municipality, active=1)
        )

        other_inactive_municipality = service_factory(
            service_group__name="municipality",
            trans__name="Another Inactive Leitbehörde",
            trans__language="de",
        )

        # add other active services to test they are copied to new instance
        be_instance.instance_services.add(
            instance_service_factory(service=other_inactive_municipality, active=0)
        )

        construction_control = service_factory(
            service_group__name="construction-control",
            trans__name="Baukontrolle Bern",
            trans__language="de",
        )
        # add construction-control to test it is not copied to new instance
        be_instance.instance_services.add(
            instance_service_factory(service=construction_control, active=1)
        )

        # create another involved applicant to test that all involved applicants
        # are copied to new instance
        be_instance.involved_applicants.create(
            invitee=admin_client.user, user=admin_client.user
        )

        be_instance.save()

        return be_instance

    return wrapper


def test_instance_copy_404(db, instance, admin_client):
    response = admin_client.post(reverse("instance-copy", args=[instance.pk]))

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.parametrize(
    "role__name,access_level,grant_type,instance_state_name,expected_status",
    [
        # Forbidden: wrong access level,
        (
            "applicant",
            "applicant",
            "USER",
            "archived",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "service-lead",
            "distribution-service",
            "SERVICE",
            "archived",
            status.HTTP_403_FORBIDDEN,
        ),
        (
            "municipality-lead",
            "lead-authority",
            "SERVICE",
            "archived",
            status.HTTP_403_FORBIDDEN,
        ),
        # Forbidden: right access level, wrong instance state
        ("Support", "support", "ROLE", "new", status.HTTP_403_FORBIDDEN),
        ("Support", "support", "ROLE", "subm", status.HTTP_403_FORBIDDEN),
        # Allowed: right access level, right instance state
        ("Support", "support", "ROLE", "archived", status.HTTP_201_CREATED),
        ("Support", "support", "ROLE", "finished", status.HTTP_201_CREATED),
    ],
)
def test_instance_copy_with_permissions_module_be(
    db,
    admin_client,
    access_level,
    grant_type,
    expected_status,
    instance_for_copy,
    instance_state_name,
    permissions_settings,
    application_settings,
    be_permissions_settings,
    be_access_levels,
    instance_acl_factory,
    settings,
    multilang,
    be_ech0211_settings,
):
    settings.APPLICATION_NAME = "kt_bern"
    application_settings["SHORT_NAME"] = "be"
    be_permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    be_permissions_settings["EVENT_HANDLER"] = (
        "camac.permissions.config.kt_bern.PermissionEventHandlerBE"
    )

    instance = instance_for_copy(instance_state_name)

    granted_access_level = AccessLevel.objects.get(pk=access_level)
    granting_service = admin_client.user.get_default_group().service
    granting_user = admin_client.user
    granting_role = admin_client.user.groups.first().role

    granting_entity_by_grant_type = {
        "USER": ("user", granting_user),
        "SERVICE": ("service", granting_service),
        "ROLE": ("role", granting_role),
    }

    key, value = granting_entity_by_grant_type[grant_type]

    instance_acl_factory(
        instance=instance,
        access_level=granted_access_level,
        grant_type=grant_type,
        **{key: value},
    )

    lead_authority_service = (
        instance.instance_services.filter(service__service_group__name="municipality")
        .first()
        .service
    )

    # add a lead-authority ACL to original instance to test that it is copied over.
    instance_acl_factory(
        instance=instance,
        service=lead_authority_service,
        access_level=AccessLevel.objects.get(pk="lead-authority"),
        grant_type="SERVICE",
    )

    original_municipality_service_ids = set(
        instance.instance_services.filter(
            service__service_group__name="municipality"
        ).values_list("service_id", flat=True)
    )

    original_service_ids_to_be_copied = set(
        instance.instance_services.exclude(
            service__service_group__name="construction-control"
        ).values_list("service_id", flat=True)
    )

    original_applicant_user_ids = set(
        instance.involved_applicants.values_list("user_id", flat=True)
    )

    assert instance.instance_services.count() == 4
    assert instance.involved_applicants.count() == 2

    response = admin_client.post(reverse("instance-copy", args=[instance.pk]))

    assert response.status_code == expected_status

    if response.status_code == status.HTTP_201_CREATED:
        new_instance = Instance.objects.get(pk=response.json()["data"]["id"])

        assert new_instance.case.meta.get("is-copy") is True
        assert new_instance.instance_state.name == "subm"

        copied_municipality_service_ids = set(
            new_instance.instance_services.filter(
                service__service_group__name="municipality"
            ).values_list("service_id", flat=True)
        )

        all_copied_service_ids = set(
            new_instance.instance_services.all().values_list("service_id", flat=True)
        )

        # municipality services are copied
        assert copied_municipality_service_ids == original_municipality_service_ids

        # construction-control services are not copied
        assert original_service_ids_to_be_copied == all_copied_service_ids
        assert new_instance.instance_services.count() == 3

        # involved applicants are all copied
        copied_applicant_user_ids = set(
            new_instance.involved_applicants.values_list("user_id", flat=True)
        )
        assert copied_applicant_user_ids == original_applicant_user_ids
        assert new_instance.involved_applicants.count() == 2

        # instance ACLs are granted on the copy
        new_acls = InstanceACL.objects.filter(instance=new_instance)

        # instance ACL granted by InstanceCreationHandlerMixin.instance_created()
        assert new_acls.filter(access_level_id="support").exists()

        # instance ACL granted by InstanceCopyHandlerMixin.instance_copied()
        assert new_acls.filter(
            service=lead_authority_service,
            access_level_id="lead-authority",
        ).exists()

        history = new_instance.history.exclude(history_type="notification").last()
        assert (
            history.get_trans_attr(name="title", lang="de")
            == "Kopie des Dossiers erstellt"
        )
