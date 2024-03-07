import pytest
from django.urls import reverse
from pytest_factoryboy import LazyFixture
from rest_framework import status

from camac.permissions.conditions import Always


@pytest.mark.parametrize(
    "role__name,instance__user",
    [
        ("Applicant", LazyFixture("admin_user")),
    ],
)
def test_instance_form_name_filter(
    application_settings,
    admin_client,
    instance,
    instance_factory,
    instance_resource_factory,
    instance_state_factory,
    ir_role_acl_factory,
):
    role = admin_client.user.groups.first().role

    ir1 = instance_resource_factory()
    ir2 = instance_resource_factory()

    other_instance_state = instance_state_factory()

    ir_role_acl_factory(
        role=role, instance_state=instance.instance_state, instance_resource=ir1
    )
    ir_role_acl_factory(
        role=role, instance_state=other_instance_state, instance_resource=ir1
    )
    ir_role_acl_factory(
        role=role, instance_state=other_instance_state, instance_resource=ir2
    )

    url = reverse("instance-resource-list")

    response = admin_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    # without the filter, both IRs are returned
    assert len(response.json()["data"]) == 2

    response = admin_client.get(url, {"instance": instance.pk})
    assert response.status_code == status.HTTP_200_OK
    # with the filter, only the first IR is returned
    assert len(response.json()["data"]) == 1


@pytest.mark.parametrize(
    "has_permission, has_role_acl_a, has_role_acl_b, expect_results",
    [
        # without instance acls, the IR acls "win"
        (False, False, False, []),
        (False, False, True, ["b"]),
        (False, True, False, ["a"]),
        (False, True, True, ["a", "b"]),
        # with instance ACLs, the instance ACLs win
        (True, False, False, ["a"]),
        (True, False, True, ["a"]),
        (True, True, False, ["a"]),
        (True, True, True, ["a"]),
    ],
)
@pytest.mark.parametrize(
    "role__name,instance__user",
    [
        ("Applicant", LazyFixture("admin_user")),
    ],
)
def test_instance_resource_filter_instance(
    application_settings,
    admin_client,
    instance,
    instance_factory,
    instance_resource_factory,
    instance_state_factory,
    ir_role_acl_factory,
    access_level,
    permissions_settings,
    instance_acl_factory,
    has_permission,
    has_role_acl_a,
    has_role_acl_b,
    expect_results,
):
    permissions_settings["ACCESS_LEVELS"] = {access_level.pk: [("foo", Always())]}

    role = admin_client.user.groups.first().role

    # ir_a requires "foo" permission and has a role ACL as well.
    ir_a = instance_resource_factory(require_permission="foo")
    # ir_b requires "bar" permission and has a role ACL as well
    ir_b = instance_resource_factory(require_permission="bar")

    check_lookups = {
        str(ir_a.pk): "a",
        str(ir_b.pk): "b",
    }

    if has_permission:
        instance_acl_factory(
            instance=instance,
            access_level=access_level,
            user=admin_client.user,
            grant_type="USER",
        )

    if has_role_acl_a:
        ir_role_acl_factory(
            role=role, instance_state=instance.instance_state, instance_resource=ir_a
        )
    if has_role_acl_b:
        ir_role_acl_factory(
            role=role, instance_state=instance.instance_state, instance_resource=ir_b
        )

    url = reverse("instance-resource-list")
    response = admin_client.get(url, {"instance": instance.pk})
    assert response.status_code == status.HTTP_200_OK

    data = response.json()["data"]
    received = sorted([check_lookups[rec["id"]] for rec in data])
    assert received == expect_results


@pytest.mark.parametrize("is_appeal", [True, False])
def test_instance_resource_appeal_only(
    admin_client,
    so_instance,
    instance_resource_factory,
    role,
    ir_role_acl_factory,
    is_appeal,
):
    visible_ir = instance_resource_factory()
    appeal_include_ir = instance_resource_factory(class_field="appeal-include")
    appeal_exclude_ir = instance_resource_factory(class_field="appeal-exclude")

    for ir in [visible_ir, appeal_include_ir, appeal_exclude_ir]:
        ir_role_acl_factory(
            role=role,
            instance_state=so_instance.instance_state,
            instance_resource=ir,
        )

    if is_appeal:
        so_instance.case.meta.update({"is-appeal": True})
        so_instance.case.save()

    response = admin_client.get(
        reverse("instance-resource-list"), {"instance": so_instance.pk}
    )

    assert response.status_code == status.HTTP_200_OK

    ids = [int(record["id"]) for record in response.json()["data"]]

    assert visible_ir.pk in ids
    assert (appeal_include_ir.pk in ids) == is_appeal
    assert (appeal_exclude_ir.pk in ids) != is_appeal
