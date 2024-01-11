from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from camac.instance import models as instance_models
from camac.permissions import api, conditions, exceptions, models


@pytest.mark.parametrize("grant_type", ["user", "service", "token"])
def test_grant_permission(db, grant_type, user, service, token, instance, access_level):
    """Test whether visibility of the ACLs themselves works correctly"""
    # Fetch before grant - should be no access
    visible_acls = models.InstanceACL.for_current_user(user=user, service=service)
    assert visible_acls.count() == 0

    # Grant permission to our user
    grant_kwargs = {
        grant_type: locals().get(grant_type),
        "grant_type": grant_type.upper(),
    }
    api.grant(**grant_kwargs, instance=instance, access_level=access_level)

    visible_acls = models.InstanceACL.for_current_user(
        user=user, service=service, token=token
    )
    assert visible_acls.count() == 1


def _get_instances(user, service, token):
    return api.PermissionManager.from_params(user, service, token).filter_queryset(
        instance_models.Instance.objects.all(), instance_prefix=""
    )


@pytest.mark.parametrize("grant_type", ["user", "service", "token"])
def test_visible_instances(
    db, grant_type, user, service, token, instance, access_level
):
    """Test whether the "simple" ACL types all work on the "instance" queryset"""
    visible_instances = _get_instances(user, service, token)

    assert visible_instances.count() == 0

    # Grant permission to our user
    grant_kwargs = {
        grant_type: locals().get(grant_type),
        "grant_type": grant_type.upper(),
    }
    api.grant(**grant_kwargs, instance=instance, access_level=access_level)

    visible_instances = _get_instances(user, service, token)
    assert visible_instances.count() == 1


_some_user = pytest.lazy_fixture("user")


@pytest.mark.parametrize(
    "grant_type, request_user, expect_result",
    [
        # Authenticated users can see stuff that's visible to anonymous users
        ("ANONYMOUS_PUBLIC", _some_user, 1),
        # Anonymous users can see instances that are publicised for them
        ("ANONYMOUS_PUBLIC", None, 1),
        # Authenticated users can see stuff that's public for authenticated users
        ("AUTHENTICATED_PUBLIC", _some_user, 1),
        # Anonymous users CANNOT see stuff that's only public for authenticated users
        ("AUTHENTICATED_PUBLIC", None, 0),
    ],
)
def test_visible_instances_public_access(
    db,
    grant_type,
    expect_result,
    request_user,
    instance,
    access_level,
):
    """Test access using the "public" grant types"""
    visible_instances = _get_instances(request_user, None, None)

    # With no ACL, nothing's visible
    assert visible_instances.count() == 0

    # Grant permission to our user
    api.grant(grant_type=grant_type, instance=instance, access_level=access_level)

    visible_instances = _get_instances(request_user, None, None)
    assert visible_instances.count() == expect_result


@pytest.mark.parametrize(
    "end_time, expect_result",
    [
        # None in the end time means "still active"
        (lambda: None, 1),
        # Future revocation means we can still see the instance
        (lambda: timezone.now() + timedelta(days=5), 1),
        # Immediate revocation means we can no longer see the instance
        (lambda: timezone.now(), 0),
        # Past revocation = invisible instance
        (lambda: timezone.now() - timedelta(seconds=1), 0),
        # Near-future revocation = we can still see it (Note: May be flaky
        # if test runs too slow, but we're optimistic that this test
        # takes less than 10s)
        (lambda: timezone.now() + timedelta(seconds=10), 1),
    ],
)
def test_revoked_acl(
    db, freezer, user, access_level, instance, end_time, expect_result
):
    """Test whether the ACL's revocation is handled correctly"""

    # Note: the `end_time` parameter is a lambda so it runs within the
    # `freezer` and thus does not generate "unfrozen" times

    visible_instances = _get_instances(user, None, None)

    assert visible_instances.count() == 0

    # Grant permission to our user
    new_acl = api.grant(
        instance=instance, grant_type="USER", access_level=access_level, user=user
    )

    visible_instances = _get_instances(user, None, None)
    assert visible_instances.count() == 1

    # we don't call the revoke API, as it would forbid revocation in the past
    # which we need for this test. We test behaviour around the end time in DB,
    # not around *setting* it
    new_acl.end_time = end_time()

    new_acl.save()

    visible_instances = _get_instances(user, None, None)
    assert visible_instances.count() == expect_result


@pytest.mark.parametrize(
    "start_time, expect_result",
    [
        # None means "immediate activation"
        (None, 1),
        # Future  grant means we can not yet see the instance
        (timezone.now() + timedelta(days=5), 1),
        # Immediate grant means we can see the instance
        (timezone.now(), 1),
        # Past grant also means we can see it
        (timezone.now() - timedelta(weeks=2), 1),
    ],
)
def test_future_acl(db, user, access_level, instance, start_time, expect_result):
    """Test whether the ACL's start time is handled correctly"""
    visible_instances = _get_instances(user, None, None)

    assert visible_instances.count() == 0

    api.grant(
        starting_at=start_time,
        instance=instance,
        grant_type="USER",
        access_level=access_level,
        user=user,
    )

    visible_instances = _get_instances(user, None, None)
    assert visible_instances.count() == expect_result


@pytest.mark.parametrize("instance_acl__grant_type", ["USER"])
@pytest.mark.parametrize(
    "instance_acl__end_time, end_time, expect_error",
    [
        # Revoke without end time = immediately
        (None, None, False),
        # Future revocation = OK
        (None, timezone.now() + timedelta(days=5), False),
        # Right now revocation = Fail - by the time it's validated, it's already
        # past
        (None, timezone.now(), True),
        # Past revocation = Nope
        (None, timezone.now() - timedelta(weeks=2), True),
        # Shortening existing revocation = OK (but why would you...)
        (timezone.now() + timedelta(days=2), timezone.now() + timedelta(days=1), False),
        # Extending existing revocation = Nope, make a new one instead
        (timezone.now(), timezone.now() + timedelta(weeks=2), True),
    ],
)
def test_extending_acl(db, instance_acl, end_time, expect_error):
    if expect_error:
        with pytest.raises(exceptions.RevocationRejected):
            instance_acl.revoke(end_time)
    else:
        instance_acl.revoke(end_time)
        assert True


def test_cache_eviction(db, user, permissions_settings, access_level, instance):
    perm_check_call_counts = {"": 0}

    def funkytown():
        perm_check_call_counts[""] += 1
        return True

    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            ("foo", conditions.Always()),
            ("bar", conditions.Always()),
            ("func", funkytown),
        ]
    }

    the_acl = api.grant(
        user=user,
        service=None,
        token=None,
        instance=instance,
        access_level=access_level,
        grant_type="USER",
    )

    manager = api.PermissionManager(api.ACLUserInfo(user=user))

    permissions = manager.get_permissions(instance)
    assert permissions == ["bar", "foo", "func"]
    # Assume one call to the permissions call
    assert perm_check_call_counts[""] == 1

    # Second call should be cached
    permissions = manager.get_permissions(instance)
    assert perm_check_call_counts[""] == 1

    # Revoke some time in the future. This should still trigger cache eviction
    # and with it, recalculation
    api.revoke(the_acl, ends_at=timezone.now() + timedelta(seconds=30))

    permissions = manager.get_permissions(instance)
    assert permissions == ["bar", "foo", "func"]
    assert perm_check_call_counts[""] == 2

    # Calling again should not increase the permissions check call count
    permissions = manager.get_permissions(instance)
    assert perm_check_call_counts[""] == 2

    # Immediate revocation must drop all permissions immediately
    api.revoke(the_acl)
    permissions = manager.get_permissions(instance)
    assert permissions == []


MSG_USER = "Grant type USER must have only the `user` value set"
MSG_SERVICE = "Grant type SERVICE must have only the `service` value set"
MSG_TOKEN = "Grant type TOKEN must have only the `token` value set"
MSG_ENDTIME = "End time must be either None or later than start time"
MSG_ANON = "Anonymous grants must not have user or service or token"
MSG_INVALID_GRANT = "Unhandled grant type blah"
MSG_GRANTTYPE = "Access level requires grant type USER"


@pytest.mark.parametrize(
    [
        "set_user",
        "set_service",
        "token",
        "grant_type",
        "end_time",
        "access_level__required_grant_type",
        "expect_error",
    ],
    [
        # First some "OK" validations
        (True, False, None, "USER", None, None, None),
        (False, False, "blah", "TOKEN", None, None, None),
        (False, True, None, "SERVICE", None, None, None),
        # Setting the wrong attributes for given grant type
        (False, False, None, "USER", None, None, MSG_USER),
        (True, False, None, "SERVICE", None, None, MSG_SERVICE),
        (True, True, None, "SERVICE", None, None, MSG_SERVICE),
        (True, True, "blah", "TOKEN", None, None, MSG_TOKEN),
        (False, True, None, "TOKEN", None, None, MSG_TOKEN),
        # End time too early
        (True, False, None, "USER", timezone.now(), None, MSG_ENDTIME),
        # Anonymous grant validations
        (True, False, None, "ANONYMOUS_PUBLIC", None, None, MSG_ANON),
        (True, False, None, "AUTHENTICATED_PUBLIC", None, None, MSG_ANON),
        # Invalid grant label
        (True, False, None, "blah", None, None, MSG_INVALID_GRANT),
        # Required grant type
        (False, False, None, "AUTHENTICATED_PUBLIC", None, "USER", MSG_GRANTTYPE),
    ],
)
@pytest.mark.parametrize("accesslevel_as_pk", [True, False])
def test_grant_validations(
    db,
    user,
    service,
    permissions_settings,
    access_level,
    instance,
    set_user,
    set_service,
    token,
    grant_type,
    end_time,
    expect_error,
    accesslevel_as_pk,
):
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [("foo", conditions.Always()), ("bar", conditions.Always())]
    }

    def _make_acl():
        api.grant(
            user=user if set_user else None,
            service=service if set_service else None,
            token=token,
            instance=instance,
            access_level=access_level.pk if accesslevel_as_pk else access_level,
            grant_type=grant_type,
            ends_at=end_time,
        )

    if expect_error:
        with pytest.raises(exceptions.GrantRejected) as exc:
            _make_acl()
        assert exc.match(expect_error)
    else:
        _make_acl()
        assert True


@pytest.mark.parametrize("instance_state__name", ["state-foo"])
@pytest.mark.parametrize("role__name", ["role-bar"])
def test_condition_objects(
    db, permissions_settings, access_level, instance, admin_client
):
    permissions_settings["ACCESS_LEVELS"] = {
        access_level.pk: [
            ("foo", conditions.InstanceState(["state-foo"])),
            ("bar", conditions.HasRole(["role-bar"])),
            ("never", conditions.Never()),
            ("never-or-always", conditions.Always() | conditions.Never()),
            (
                "role-bar-and-never",
                conditions.HasRole(["role-bar"]) & conditions.Never(),
            ),
            ("not-bar", ~conditions.HasRole(["role-bar"])),
        ]
    }

    api.grant(
        user=admin_client.user,
        service=None,
        token=None,
        instance=instance,
        access_level=access_level,
        grant_type="USER",
    )

    # We request permissions via API so we can test the full userinfo stuff
    # that we'd have to (badly) fake if talking directly to the lowlevel api
    # Check permissions before...
    resp = admin_client.get(reverse("instance-permissions-detail", args=[instance.pk]))

    result = resp.json()["data"]["attributes"]["permissions"]
    assert sorted(result) == sorted(["foo", "bar", "never-or-always"])
