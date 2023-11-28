from datetime import datetime, timedelta

import pytest
from django.urls import reverse
from django.utils import timezone
from rest_framework import status

from camac.permissions import api
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
                "service": {"data": {"id": service.pk, "type": "services"}},
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
            assert attrs["start-time"] == set_start_time.isoformat()
        else:
            # start time should be now-ish
            created_start_time = datetime.fromisoformat(attrs["start-time"])
            delta = timezone.now() - created_start_time
            assert abs(delta) < timedelta(minutes=1)

        if set_end_time:
            assert relationships["revoked-by-service"]["data"]["id"]
            assert relationships["revoked-by-user"]["data"]["id"]
            assert attrs["revoked-by-event"]
            assert attrs["end-time"] == set_end_time.isoformat()

        assert created_by_user == str(admin_client.user.id)
    else:
        assert result.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "role__name, end_time, is_responsible_service, expect_success",
    [
        ("Municipality", None, True, True),
        ("Municipality", None, False, False),
        ("Support", None, True, False),
        ("Municipality", timezone.now(), True, False),
        ("Municipality", timezone.now() + timedelta(days=5), True, True),
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
):
    the_acl = api.grant(
        instance,
        grant_type=api.GRANT_CHOICES.USER.value,
        access_level=access_level,
        user=admin_client.user,
    )

    if not is_responsible_service:
        # The instance's responsible group (and therefore it's responsible
        # service) should be someone else - don't care, just not *us*
        instance.group = group_factory()
        instance.save()

    url = reverse("instance-acls-revoke", args=[the_acl.pk])
    post_data = {
        "data": {
            "attributes": {
                "grant-type": the_acl.grant_type,
            },
            "relationships": {
                "" "instance": {"data": {"id": instance.pk, "type": "instances"}},
                "service": {"data": {"id": service.pk, "type": "services"}},
                "access-level": {
                    "data": {"id": access_level.pk, "type": "access-levels"}
                },
            },
            "id": the_acl.pk,
            "type": "instance-acls",
        },
    }
    if end_time:
        post_data["data"]["attributes"]["end-time"] = end_time.isoformat()

    result = admin_client.post(
        url,
        post_data,
    )

    result_data = result.json()

    if expect_success:
        assert result.status_code == status.HTTP_200_OK, result_data

        revoked_by = get_dict_item(
            result_data, "data.relationships.revoked-by-user.data.id"
        )
        event = get_dict_item(result_data, "data.attributes.revoked-by-event")
        ends_at = get_dict_item(result_data, "data.attributes.end-time")
        assert revoked_by == str(admin_client.user.id)
        assert event == "manual-revocation"

        # end time of the ACL should be within a few seconds of the requested
        # end time (if we send it), or within a few seconds of *now* if we
        # didn't. We allow for a few seconds due to processing time
        expected_end_time = end_time or timezone.now()
        actual_end_time = datetime.fromisoformat(ends_at)
        time_diff = abs(actual_end_time - expected_end_time)
        assert time_diff < timedelta(seconds=5)
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

    url = reverse("access-levels-list")
    result = admin_client.get(url)
    assert result.status_code == status.HTTP_200_OK
    if expect_results:
        assert result.json() == {
            "data": [
                {
                    "attributes": {
                        "slug": "page-event-two",
                        "name": access_level.name.de,
                        "description": access_level.description.de,
                        "required-grant-type": None,
                    },
                    "id": "page-event-two",
                    "type": "access-levels",
                }
            ],
        }
    else:
        assert result.json() == {"data": []}


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
