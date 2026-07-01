import pytest

from camac.permissions.api import PermissionManager


@pytest.mark.parametrize(
    "service__slug,role__name,has_acl,has_work_item,expected_result",
    [
        # ROLES_INTERNAL_NO_READONLY: read & write
        (
            "agr-bauen",
            "service-lead",
            True,
            True,
            {"form-rpg2-read", "form-rpg2-write"},
        ),
        (
            "agr-bauen",
            "service-clerk",
            True,
            True,
            {"form-rpg2-read", "form-rpg2-write"},
        ),
        # ROLES_INTERNAL (readonly): read
        ("agr-bauen", "service-readonly", True, True, {"form-rpg2-read"}),
        # No ACL: inquiry not sent
        ("agr-bauen", "service-lead", False, True, set()),
        # No work item
        ("agr-bauen", "service-lead", True, False, set()),
        # Wrong service
        (None, "service-lead", True, True, set()),
        ("other-slug", "service-lead", True, True, set()),
    ],
)
@pytest.mark.django_db
def test_form_rpg2_permissions_be(
    be_instance,
    be_permissions_settings,
    be_access_levels,
    userinfo,
    has_acl,
    has_work_item,
    expected_result,
    caluma_work_item_factory,
):
    manager = PermissionManager(userinfo)
    if has_acl:
        manager.grant(
            be_instance,
            grant_type="SERVICE",
            access_level="distribution-service",
            service=userinfo.service,
            event_name="inquiry-sent",
        )

    if has_work_item:
        # Work item status is not relevant
        caluma_work_item_factory(case=be_instance.case, task_id="rpg2")

    granted_rpg2_permissions = {
        p for p in manager.get_permissions(be_instance) if "rpg2" in p
    }
    assert set(granted_rpg2_permissions) == expected_result


@pytest.mark.parametrize(
    "service__slug,role__name,instance_state_name,expected_result",
    [
        # ROLES_INTERNAL_NO_READONLY: read & write, allowed instance state
        (
            "agr-bauen",
            "service-lead",
            "subm",
            {"form-rpg2-read", "form-rpg2-write"},
        ),
        # ROLES_INTERNAL_NO_READONLY, disallowed instance state
        (
            "agr-bauen",
            "service-lead",
            "correction",
            set(),
        ),
    ],
)
@pytest.mark.django_db
def test_form_rpg2_permissions_state_be(
    be_instance,
    be_permissions_settings,
    be_access_levels,
    userinfo,
    instance_state_name,
    instance_state_factory,
    expected_result,
    caluma_work_item_factory,
):
    manager = PermissionManager(userinfo)
    manager.grant(
        be_instance,
        grant_type="SERVICE",
        access_level="distribution-service",
        service=userinfo.service,
        event_name="inquiry-sent",
    )
    caluma_work_item_factory(case=be_instance.case, task_id="rpg2")

    be_instance.instance_state = instance_state_factory(name=instance_state_name)
    be_instance.save()

    granted_rpg2_permissions = {
        p for p in manager.get_permissions(be_instance) if "rpg2" in p
    }
    assert set(granted_rpg2_permissions) == expected_result


@pytest.mark.parametrize(
    "service__slug,role__name,access_level,has_acl,has_work_item,expected_result",
    [
        # ROLES_NO_READONLY: read & write
        (
            "afb",
            "trusted-service-lead",
            "distribution-service",
            True,
            True,
            {"form-rpg2-read", "form-rpg2-write"},
        ),
        (
            "afb",
            "trusted-service-clerk",
            "distribution-service",
            True,
            True,
            {"form-rpg2-read", "form-rpg2-write"},
        ),
        # Readonly role: read
        (
            "afb",
            "trusted-service-read",
            "distribution-service",
            True,
            True,
            {"form-rpg2-read"},
        ),
        # Lead authority
        (
            "afb",
            "trusted-service-lead",
            "lead-authority",
            True,
            True,
            {"form-rpg2-read", "form-rpg2-write"},
        ),
        (
            "afb",
            "trusted-service-read",
            "lead-authority",
            True,
            True,
            {"form-rpg2-read"},
        ),
        # No ACL: inquiry not sent
        ("afb", "trusted-service-lead", "distribution-service", False, True, set()),
        # No work item
        ("afb", "trusted-service-lead", "distribution-service", True, False, set()),
        # Wrong service
        (None, "trusted-service-lead", "distribution-service", True, True, set()),
        (
            "other-slug",
            "trusted-service-lead",
            "distribution-service",
            True,
            True,
            set(),
        ),
        ("other-slug", "trusted-service-lead", "lead-authority", True, True, set()),
    ],
)
@pytest.mark.django_db
def test_form_rpg2_permissions_ag(
    ag_instance,
    ag_permissions_settings,
    ag_access_levels,
    userinfo,
    access_level,
    has_acl,
    has_work_item,
    expected_result,
    caluma_work_item_factory,
):
    manager = PermissionManager(userinfo)
    if has_acl:
        manager.grant(
            ag_instance,
            grant_type="SERVICE",
            access_level=access_level,
            service=userinfo.service,
            event_name="inquiry-sent",
        )

    if has_work_item:
        # Work item status is not relevant
        caluma_work_item_factory(case=ag_instance.case, task_id="rpg2")

    granted_rpg2_permissions = {
        p for p in manager.get_permissions(ag_instance) if "rpg2" in p
    }
    assert set(granted_rpg2_permissions) == expected_result
