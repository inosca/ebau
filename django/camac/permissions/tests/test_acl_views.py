from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.permissions import api
from camac.permissions.conditions import Always
from camac.permissions.models import AccessLevel, InstanceACL
from camac.permissions.switcher import PERMISSION_MODE
from camac.utils import get_dict_item


@pytest.mark.parametrize(
    "role__name, expect_data",
    [
        ("Municipality", True),
        ("Something-else", False),
    ],
)
def test_list_acl_view(
    db,
    instance,
    admin_client,
    service,
    permissions_settings,
    location_factory,
    access_level,
    role,
    group_factory,
    expect_data,
):
    url = reverse("instance-acls-list")

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [("foo", "*"), ("bar", "*")]
    }

    # Check ACLs before... there should be none
    result = admin_client.get(url, {"instance": instance.pk})
    assert result.json() == {"data": []}

    # Point to some other group... for now, to make the instance
    # invisible
    old_group = instance.group
    old_location = instance.location
    instance.group = group_factory()
    instance.location = location_factory()
    instance.save()

    # Grant this access level to our user
    api.grant(
        instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
    )

    # And check the permissions after.
    result = admin_client.get(url, {"instance": instance.pk})
    # This should be empty, user has no old-style permission on the instance
    assert len(result.json()["data"]) == 0

    if role.name != "Municipality":
        # Group with no service
        admin_client.user.groups.set(
            [group_factory(service=None)], through_defaults={"default_group": True}
        )
    else:
        # set group to our user's group, this should make the instance
        # visible (again)
        instance.group = old_group
        instance.location = old_location
        instance.save()

    result = admin_client.get(url, {"instance": instance.pk})
    acls_data = result.json()["data"]

    if expect_data:
        # Not doing a full snapshot here due to the timestamps
        assert len(acls_data) == 1
        assert acls_data[0]["attributes"]["end-time"] is None
        assert acls_data[0]["attributes"]["start-time"] is not None
        assert acls_data[0]["attributes"]["grant-type"] == "USER"
    else:
        assert len(acls_data) == 0


@pytest.mark.parametrize("role__name", ["Applicant"])
def test_list_acl_view_for_applicant(
    db,
    access_level_factory,
    admin_client,
    admin_user,
    applicant_factory,
    instance,
    service,
):
    applicant_factory(instance=instance, invitee=admin_user)

    visible_access_level = access_level_factory(slug="municipality-before-submission")
    hidden_access_level = access_level_factory()

    for access_level in [visible_access_level, hidden_access_level]:
        api.grant(
            instance,
            grant_type=api.GRANT_CHOICES.SERVICE.value,
            access_level=access_level,
            service=service,
        )

    response = admin_client.get(
        reverse("instance-acls-list"), {"instance": instance.pk}
    )

    result = response.json()["data"]
    assert len(result) == 1

    ids = [i["relationships"]["access-level"]["data"]["id"] for i in result]
    assert visible_access_level.slug in ids
    assert hidden_access_level.slug not in ids


@pytest.mark.parametrize("set_end_time", [True, False])
@pytest.mark.parametrize("set_start_time", [True, False])
@pytest.mark.parametrize(
    "role__name, responsible_for_instance, expect_success",
    [
        ("Municipality", True, True),
        ("Support", True, False),
        ("Municipality", False, False),
    ],
)
def test_create_acl(
    db,
    instance,
    admin_client,
    permissions_settings,
    access_level,
    service,
    group_factory,
    expect_success,
    responsible_for_instance,
    set_start_time,
    set_end_time,
):
    url = reverse("instance-acls-list")

    tz = timezone.get_current_timezone()
    if set_start_time:
        set_start_time = datetime.now(tz=tz) + timedelta(days=5)
    if set_end_time:
        set_end_time = datetime.now(tz=tz) + timedelta(days=30)

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [("foo", "*"), ("bar", "*")]
    }

    if not responsible_for_instance:
        instance.group = group_factory()
        instance.save()

    post_data = {
        "data": {
            "attributes": {
                "grant-type": "SERVICE",
            },
            "relationships": {
                "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "service": {"data": {"id": service.pk, "type": "public-services"}},
                "access-level": {
                    "data": {"id": access_level.pk, "type": "access-levels"}
                },
            },
            "type": "instance-acls",
        },
    }
    if set_end_time:
        post_data["data"]["attributes"]["end-time"] = set_end_time.isoformat()
    if set_start_time:
        # In the future, but still before end time
        post_data["data"]["attributes"]["start-time"] = set_start_time.isoformat()

    result = admin_client.post(url, post_data)

    result_data = result.json()

    if expect_success:
        assert result.status_code == status.HTTP_201_CREATED, result_data

        attrs = get_dict_item(result_data, "data.attributes")
        relationships = get_dict_item(result_data, "data.relationships")
        created_by_user = get_dict_item(relationships, "created-by-user.data.id")

        if set_start_time:
            assert attrs["start-time"] == set_start_time.astimezone().isoformat()
        else:
            # start time should be now-ish
            created_start_time = datetime.fromisoformat(attrs["start-time"])
            delta = timezone.now() - created_start_time
            assert abs(delta) < timedelta(minutes=1)

        if set_end_time:
            assert relationships["revoked-by-service"]["data"]["id"]
            assert relationships["revoked-by-user"]["data"]["id"]
            assert attrs["revoked-by-event"]
            assert attrs["end-time"] == set_end_time.astimezone().isoformat()

        assert created_by_user == str(admin_client.user.id)
    else:
        assert result.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "role__name, end_time, is_responsible_service, expect_success",
    [
        # responsible service can revoke
        ("Municipality", None, True, True),
        # non-responsible service cannot revoke
        ("Municipality", None, False, False),
        # non-municipality user cannot revoke
        ("Support", None, True, False),
        # just expired acl cannot be revoked again
        ("Municipality", timezone.now(), True, False),
        # shortening = ok
        ("Municipality", timezone.now() + timedelta(days=5), True, True),
        # extending expired acl = not ok
        ("Municipality", timezone.now() - timedelta(days=5), True, False),
    ],
)
def test_revoke_acl(
    db,
    instance,
    admin_client,
    permissions_settings,
    access_level,
    service,
    group_factory,
    end_time,
    is_responsible_service,
    expect_success,
    use_instance_service,
):
    the_acl = InstanceACL.objects.create(
        instance=instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
        end_time=end_time,
        start_time=timezone.now() - timedelta(days=50),
    )

    if is_responsible_service:
        instance.instance_services.create(
            service=admin_client.user.get_default_group().service
        )
    else:
        # The instance's responsible group (and therefore it's responsible
        # service) should be someone else - don't care, just not *us*
        instance.group = group_factory()
        instance.save()

    url = reverse("instance-acls-revoke", args=[the_acl.pk])

    time_before_request = timezone.now()

    result = admin_client.post(url)

    result_data = result.json()

    the_acl.refresh_from_db()

    if expect_success:
        assert result.status_code == status.HTTP_200_OK, result_data

        assert the_acl.revoked_by_user == admin_client.user
        assert the_acl.revoked_by_event == "manual-revocation"

        time_after_request = timezone.now()

        # The end time must be *at* the time of request, which must be
        # between now and just before the request
        assert time_before_request <= the_acl.end_time <= time_after_request

    else:
        # 404 allowed as well because not being responsible service makes the
        # ACLs invisible to the user, so we won't even get to the permission
        # checking stage
        assert result.status_code in (
            status.HTTP_404_NOT_FOUND,
            status.HTTP_400_BAD_REQUEST,
        )


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_deny_modify_acl(
    db, instance, admin_client, permissions_settings, access_level, service
):
    # For now, no modification or creation of ACLs via API is allowed, only
    # viewing. The only modification is revoke, which has it's own action
    # endpoint.

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [("foo", "*"), ("bar", "*")]
    }

    # Grant this access level to our user
    new_acl = api.grant(
        instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
    )
    url = reverse("instance-acls-detail", args=[new_acl.pk])

    # Try to modify - should fail
    result = admin_client.patch(
        url,
        {
            "data": {
                "attributes": {"grant-type": api.GRANT_CHOICES.ANONYMOUS_PUBLIC.value},
                "type": "instance-acls",
                "id": str(new_acl.pk),
            },
        },
    )

    assert result.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize("role__name", ["Municipality"])
def test_deny_delete_acl(
    db, instance, admin_client, permissions_settings, access_level, service
):
    instance.group = admin_client.user.groups.first()
    instance.save()

    # Grant this access level to our user
    new_acl = api.grant(
        instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
    )
    url = reverse("instance-acls-detail", args=[new_acl.pk])

    # Try to delete - should fail
    result = admin_client.delete(url)

    assert result.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "role__name, expect_results",
    [
        ("Service", False),
        ("Municipality", True),
        ("Applicant", False),
    ],
)
def test_get_access_levels(
    db,
    instance,
    admin_client,
    permissions_settings,
    access_level,
    service,
    expect_results,
):
    # Listing of access levels should only be allowed for the users who can
    # create (or revoke) ACLs (at least for now).

    # TODO: This can be dropped in favour of test_assignable_filter() below,
    # once we drop the permission_aware get_queryset in the AccessLevelViewset

    url = reverse("access-levels-list")
    result = admin_client.get(url)
    assert result.status_code == status.HTTP_200_OK
    if expect_results:
        assert result.json() == {
            "data": [
                {
                    "attributes": {
                        "slug": "guess-white-art",
                        "name": access_level.name.de,
                        "description": access_level.description.de,
                        "required-grant-type": None,
                        "applicable-area": access_level.applicable_area,
                    },
                    "id": "guess-white-art",
                    "type": "access-levels",
                }
            ],
        }
    else:
        assert result.json() == {"data": []}


@pytest.mark.parametrize(
    "do_filter,grant,permission_mode, role__name, expect_results",
    [
        # Permission mode is FULL: User can only see access levels that are
        # explicitly allowed to be assigned *on the given instance*
        (True, "geometer", "FULL", "Municipality", 1),
        (True, None, "FULL", "Municipality", 0),
        (False, None, "FULL", "Municipality", "ALL"),
        (False, "geometer", "FULL", "Municipality", "ALL"),
        (True, "any", "FULL", "Municipality", "ALL"),
        (False, "any", "FULL", "Municipality", "ALL"),
        # Permission mode is OFF: Old mode, can't filter except by role
        (True, "geometer", "OFF", "Municipality", "ALL"),
        (True, "geometer", "OFF", "Geometer", 0),
        (False, "geometer", "OFF", "Municipality", "ALL"),
        # AccessLevelViewset.get_queryset() is @permission_aware, therefore
        # non-municipality users never see anything here (for now)
        (False, "geometer", "OFF", "Geometer", 0),
    ],
)
def test_assignable_filter(
    db,
    be_instance,
    admin_client,
    instance_acl_factory,
    be_permissions_settings,
    be_access_levels,
    # params
    permission_mode,
    do_filter,
    grant,
    expect_results,
):
    """
    Test the asssignable_in_instance filter on the access levels.

    The filter is supposed to only return the access levels that the current
    user can assign to someone on the given instance.
    """
    if expect_results == "ALL":
        expect_results = AccessLevel.objects.all().count()

    # Drop any configured "grant" permisisons, so we can test the exact
    # behaviour
    be_permissions_settings["ACCESS_LEVELS"]["lead-authority"] = [
        (p, c)
        for p, c in be_permissions_settings["ACCESS_LEVELS"]["lead-authority"]
        if not p.startswith("permissions-grant-")
    ]
    if grant:
        # Allow granting of some access levels
        be_permissions_settings["ACCESS_LEVELS"]["lead-authority"].append(
            (f"permissions-grant-{grant}", Always())
        )

    be_permissions_settings["PERMISSION_MODE"] = permission_mode

    instance_acl_factory(
        instance=be_instance,
        service=admin_client.user.get_default_group().service,
        access_level=AccessLevel.objects.get(pk="lead-authority"),
    )

    url = reverse("access-levels-list")

    filter_param = {"assignable_in_instance": str(be_instance.pk)}

    resp = admin_client.get(url, filter_param if do_filter else {})
    assert resp.status_code == status.HTTP_200_OK

    resp_data = resp.json()
    assert len(resp_data["data"]) == expect_results


@pytest.mark.parametrize("role__name", ["Municipality"])
@pytest.mark.parametrize(
    "filter, filtervalue, expect_results",
    [
        ("user", "IMPLICIT", ["user"]),
        ("service", "IMPLICIT", ["sched", "inact", "service"]),
        ("is_active", "true", ["service", "user"]),
        ("is_active", "false", ["sched", "inact"]),
        ("status", "scheduled", ["sched"]),
        ("status", "active", ["service", "user"]),
        ("status", "expired", ["inact"]),
    ],
)
def test_list_acl_filters(
    db,
    instance,
    admin_client,
    service,
    permissions_settings,
    access_level_factory,
    instance_acl_factory,
    role,
    group_factory,
    filter,
    filtervalue,
    expect_results,
):
    url = reverse("instance-acls-list")

    level_1 = access_level_factory(slug="level1")
    level_2 = access_level_factory(slug="level2")
    filter_dict = {filter: filtervalue}
    if filter == "user":
        filter_dict["user"] = str(admin_client.user.pk)
    if filter == "service":
        filter_dict["service"] = str(service.pk)

    permissions_settings["ACCESS_LEVELS"] = {
        level_1.pk: [("foo", "*"), ("bar", "*")],
        level_2.pk: [("baz", "*"), ("ding", "*")],
    }

    # One active USER ACL
    user_acl = instance_acl_factory(
        instance=instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=level_1,
        user=admin_client.user,
        start_time=timezone.now() - timedelta(days=5),
    )

    # one active SERVICE ACL
    service_acl = instance_acl_factory(
        instance=instance,
        grant_type=api.GRANT_CHOICES.SERVICE.value,
        access_level=level_2,
        service=service,
        start_time=timezone.now() - timedelta(days=4),
    )
    # one inactive SERVICE ACL
    inact_service_acl = instance_acl_factory(
        instance=instance,
        grant_type=api.GRANT_CHOICES.SERVICE.value,
        access_level=level_2,
        service=service,
        start_time=timezone.now() - timedelta(days=3),
        end_time=timezone.now(),
    )
    # one scheduled SERVICE ACL
    sched_acl = instance_acl_factory(
        instance=instance,
        grant_type=api.GRANT_CHOICES.SERVICE.value,
        access_level=level_2,
        service=service,
        start_time=timezone.now() + timedelta(days=2),
    )

    acl_to_name = {
        str(user_acl.pk): "user",
        str(service_acl.pk): "service",
        str(inact_service_acl.pk): "inact",
        str(sched_acl.pk): "sched",
    }

    result = admin_client.get(url, filter_dict)
    acls_data = result.json()["data"]

    acl_ids = [a["id"] for a in acls_data]

    acl_names = [acl_to_name[id] for id in acl_ids]

    # Note: we set the start times to slightly different values. We implicitly
    # test the result order as well, we want the latest starting ACL first
    assert acl_names == expect_results


@pytest.mark.parametrize("access_level__slug", ["foo"])
@pytest.mark.parametrize(
    "have_permission, expect_success",
    [
        ("permissions-grant-foo", True),
        ("permissions-grant-any", True),
        ("permissions-grant-bar", False),
    ],
)
def test_create_with_permissions(
    # params
    have_permission,
    expect_success,
    # fixtures
    db,
    user,
    user_factory,
    permissions_settings,
    access_level,
    instance,
    instance_acl_factory,
    admin_client,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [(have_permission, Always())]
    }
    instance_acl_factory(
        user=admin_client.user,
        access_level=access_level,
        start_time=timezone.now(),
        grant_type="USER",
        instance=instance,
    )

    other_user = user_factory()

    url = reverse("instance-acls-list")
    result = admin_client.post(
        url,
        {
            "data": {
                "attributes": {
                    "grant-type": "USER",
                },
                "relationships": {
                    "instance": {"data": {"id": instance.pk, "type": "instances"}},
                    "access-level": {
                        "data": {"id": access_level.pk, "type": "access-levels"}
                    },
                    "user": {"data": {"id": other_user.pk, "type": "public-users"}},
                },
                "type": "instance-acls",
            }
        },
    )
    expect_status = (
        status.HTTP_201_CREATED if expect_success else status.HTTP_403_FORBIDDEN
    )

    assert result.status_code == expect_status


@pytest.mark.parametrize("access_level__slug", ["foo"])
@pytest.mark.parametrize(
    "have_permission, expect_success",
    [
        ("permissions-revoke-foo", True),
        ("permissions-revoke-any", True),
        ("permissions-revoke-bar", False),
    ],
)
def test_revoke_with_permissions(
    # params
    have_permission,
    expect_success,
    # fixtures
    db,
    user,
    user_factory,
    permissions_settings,
    access_level,
    instance,
    instance_acl_factory,
    admin_client,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            (have_permission, Always()),
            # the read permission is given here, we only test revocation rights
            ("permissions-read-any", Always()),
        ]
    }

    # the one we need to *do the thing*
    instance_acl_factory(
        user=admin_client.user,
        access_level=access_level,
        start_time=timezone.now(),
        grant_type="USER",
        instance=instance,
    )

    other_user = user_factory()

    # the one being tested on
    to_delete = instance_acl_factory(
        user=other_user,
        access_level=access_level,
        start_time=timezone.now(),
        grant_type="USER",
        instance=instance,
    )

    url = reverse("instance-acls-revoke", args=[to_delete.pk])
    result = admin_client.post(
        url,
    )
    expect_status = status.HTTP_200_OK if expect_success else status.HTTP_403_FORBIDDEN

    assert result.status_code == expect_status


@pytest.mark.parametrize("access_level__slug", ["foo"])
@pytest.mark.parametrize(
    "query_instance, have_permission, expected_count",
    [
        (True, "permissions-revoke-foo", 0),
        (True, "permissions-revoke-any", 0),
        (True, "permissions-revoke-bar", 0),
        (True, "permissions-read-foo", 1),
        (True, "permissions-read-any", 2),
        (False, "permissions-read-any", 0),
    ],
)
def test_list_with_permissions(
    # params
    query_instance,
    have_permission,
    expected_count,
    # fixtures
    db,
    user,
    user_factory,
    access_level_factory,
    permissions_settings,
    access_level,
    instance,
    instance_acl_factory,
    admin_client,
):
    permissions_settings["PERMISSION_MODE"] = PERMISSION_MODE.FULL
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [(have_permission, Always())]
    }

    # the one we need to *do the thing*
    instance_acl_factory(
        user=admin_client.user,
        access_level=access_level,
        start_time=timezone.now(),
        grant_type="USER",
        instance=instance,
    )

    other_user = user_factory()

    # some "other" ACL with an access level we can't see (but on "our" instance)
    instance_acl_factory(
        user=other_user,
        access_level=access_level_factory(),
        start_time=timezone.now(),
        grant_type="USER",
        instance=instance,
    )

    url = reverse("instance-acls-list")
    result = admin_client.get(url, {"instance": instance.pk} if query_instance else {})

    assert len(result.json()["data"]) == expected_count
