from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Union

from django.conf import ImproperlyConfigured, settings
from django.core.cache import cache
from django.db.models import QuerySet, Subquery
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from camac.instance.models import Instance
from camac.permissions import models
from camac.permissions.conditions import Callback, Check
from camac.permissions.models import AccessLevel, InstanceACL
from camac.user import models as user_models
from camac.user.models import Service, User

from . import exceptions

# for direct access
GRANT_CHOICES = models.GRANT_CHOICES


@dataclass
class ACLUserInfo:
    """Representation of a user as required by the lower-level ACL APIs."""

    user: Optional[user_models.User] = None
    service: Optional[user_models.Service] = None
    token: Optional[str] = None
    role: Optional[user_models.Role] = None

    @classmethod
    def from_request(cls, request):
        # TODO: Token ACL is not specified yet, so this part is always unset

        user = request.user if hasattr(request, "user") else None
        try:
            service = request.group.service
        except AttributeError:
            service = None
        try:
            role = request.group.role
        except AttributeError:  # pragma: no cover
            role = None

        return cls(user=user, service=service, token=None, role=role)

    def to_kwargs(self):
        """Turn the userinfo into a "kwargs" dict.

        The kwargs dict consists of the keys `user`, `service`, `token`, and
        `area` - suitable for passing along to the filtering methods in
        `camac.permissions.models`.
        """

        # Same logic as camac.user.permissions.get_role_name()
        perms = settings.APPLICATION.get("ROLE_PERMISSIONS", {})

        if not self.role:
            area = models.APPLICABLE_AREAS.PUBLIC.value
        else:
            role_name = perms.get(self.role.name)
            area = (
                models.APPLICABLE_AREAS.APPLICANT.value
                if role_name == "applicant"
                else models.APPLICABLE_AREAS.INTERNAL.value
            )

        return {
            "user": self.user,
            "service": self.service,
            "token": self.token,
            "area": area,
        }

    def to_cache_key(self, instance: Union[Instance, str, int]):
        user = self.user.pk if self.user else "-"
        service = self.service.pk if self.service else "-"
        token = self.token.pk if self.token else "-"
        role = self.role.pk if self.role else "-"

        # instance may be passed in as ID or model object
        instance_id = (
            str(instance.pk) if isinstance(instance, Instance) else str(instance)
        )

        # The instance is first, so we can match better when revoking permissions
        return f"permissions:i={instance_id},r={role},u={user},s={service},t={token}"


class PermissionManager:
    userinfo: ACLUserInfo
    default_event: Optional[str] = None

    def __init__(self, userinfo: ACLUserInfo):
        self.userinfo = userinfo

    @classmethod
    def for_anonymous(cls) -> "PermissionManager":
        userinfo = ACLUserInfo(user=None, service=None, token=None)
        return cls(userinfo=userinfo)

    @classmethod
    def from_params(cls, user=None, service=None, token=None):
        userinfo = ACLUserInfo(user=user, service=service, token=token)
        return cls(userinfo=userinfo)

    @classmethod
    def from_request(cls, request) -> "PermissionManager":
        # TODO: Token ACL is not specified yet, so
        # this part is always unset
        userinfo = ACLUserInfo.from_request(request)
        return cls(userinfo=userinfo)

    def get_permissions(self, instance: Union[Instance, str, int]) -> List[str]:
        cache_key = self.userinfo.to_cache_key(instance)
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        acls = (
            models.InstanceACL.for_current_user(**self.userinfo.to_kwargs())
            # this filter should work regardless of whether `instance`
            # is a model or just an FK reference
            .filter(instance=instance)
            .select_related("access_level")
        )

        granted_permissions = set()
        # We try to cache rather long
        expiry = timezone.now() + timedelta(days=10)

        enable_cache = True

        for acl in acls:
            access_level = acl.access_level
            if acl.end_time:
                # shorten expiry for the cache
                expiry = min(expiry, acl.end_time)

            for perm, condition in self._access_level_config(access_level.slug):
                # Cache gets disabled on the first condition that doesn't
                # allow caching
                enable_cache = enable_cache and getattr(
                    condition, "allow_caching", False
                )

                if callable(condition):
                    condition = Callback(condition)
                if isinstance(condition, Check):
                    if condition.apply(userinfo=self.userinfo, instance=instance):
                        granted_permissions.add(perm)

                else:  # pragma: no cover
                    raise ImproperlyConfigured(
                        "Plain string-based conditionals for permissions are "
                        "not supported anymore. Use InstanceState(...) from "
                        "camac.permissions.conditions instead. Problematic "
                        f"config entry: Access Level {access_level.slug}, "
                        f"permission {perm}"
                    )

        permissions_sorted = sorted(granted_permissions)
        if enable_cache:
            cache_duration = expiry - timezone.now()
            cache.set(cache_key, permissions_sorted, cache_duration.total_seconds())
        return permissions_sorted

    def has_any(self, instance, required_permissions: List[str]):
        """Return True if user has at least one of the required permissions."""
        assert isinstance(required_permissions, list)
        have = self.get_permissions(instance)
        return any(permission in have for permission in required_permissions)

    def has_all(self, instance, required_permissions: List[str]):
        """Return True if user has all required permissions."""
        assert isinstance(required_permissions, list)
        have = self.get_permissions(instance)
        return all(permission in have for permission in required_permissions)

    def require_any(self, instance, required_permissions: List[str]):
        """Enforce presence of at least one of the given permissions."""
        if self.has_any(instance, required_permissions):
            return
        raise PermissionDenied("You do not have the required permission to do this")

    def require_all(self, instance, required_permissions: List[str]):
        """Enforce presence of all of the given the given permissions."""
        if self.has_all(instance, required_permissions):
            return
        raise PermissionDenied("You do not have the required permission to do this")

    def _access_level_config(self, access_level_slug):
        """Return the config for the given access level.

        The result is a list of (permission, condition) tuples (see the
        `camac.settings.modules.permissions` module, or the permission module
        documentation for details)
        """
        try:
            return settings.PERMISSIONS["ACCESS_LEVELS"][access_level_slug]
        except KeyError:  # pragma: no cover
            raise ImproperlyConfigured(
                f"Permissions config is missing an entry for access level {access_level_slug}"
            )

    def grant(
        self,
        instance: Instance,
        grant_type: str,
        access_level: Union[AccessLevel, str],
        user: Optional[User] = None,
        service: Optional[Service] = None,
        token: Optional[str] = None,
        starting_at: Optional[datetime] = None,
        ends_at: Optional[datetime] = None,
        event_name: Optional[str] = None,
    ):
        """Grant permissions by creating a new ACL on the given Instance.

        Depending on the `grant_type` given, the parameters `user`,
        `service`, or `token` may be required or disallowed.

        If you pass `starting_at`, the ACL will be valid starting exactly at
        the given time. Otherwise, it starts at the current time.

        If you pass `ends_at`, the ACL will be valid until just before the
        given time (In other words, `ends_at` specifies the first second where
        the ACL isn't valid anymore). If no `ends_at` is passed, the ACL is
        valid indefinitely (or until explicitly revoked).

        The `access_level` denotes a named group of permissions. The access
        level may also restrict the type of grant that can be allowed

        Return the new ACL object.
        """
        starting_at = starting_at or timezone.now()
        # if default event has been set and no override is given, use it
        event_name = event_name or self.default_event

        if isinstance(access_level, str):
            access_level = models.AccessLevel.objects.get(pk=access_level)

        _validate_grant(
            grant_type=grant_type,
            user=user,
            service=service,
            token=token,
            starting_at=starting_at,
            ends_at=ends_at,
            access_level=access_level,
        )

        new_acl = InstanceACL.objects.create(
            grant_type=grant_type,
            user=user,
            instance=instance,
            access_level=access_level,
            service=service,
            token=token,
            end_time=ends_at,
            created_by_user=self.userinfo.user,
            created_by_event=event_name,
            created_by_service=self.userinfo.service,
            revoked_by_user=self.userinfo.user if ends_at else None,
        )
        return new_acl

    def revoke(
        self,
        acl: InstanceACL,
        ends_at: Optional[datetime] = None,
        event_name: Optional[str] = None,
    ):
        # if default event has been set and no override is given, use it
        event_name = event_name or self.default_event

        acl.revoked_by_user = self.userinfo.user
        acl.revoked_by_event = event_name
        acl.revoked_by_service = self.userinfo.service

        acl.revoke(ends_at)
        acl.save()
        # Any revocation clears the permissions cache for the affected instance.
        # We must clear the cache *after* the ACL has been revoked to avoid any
        # race condition (ACL gets re-cached before it's in the DB, thus it's
        # expiration date is not yet known)
        _clear_cache_for_acl(acl)

    def filter_queryset(self, queryset, instance_prefix):
        """Filter a given queryset to only show the entries with active ACL.

        The queryset is limited to those entries where the current user has
        an active InstanceACL.
        """
        # Need to make the QS distinct, as users may have multiple active
        # ACLs, and we don't want to return a cartesian product

        return queryset.filter(self.get_q_object(instance_prefix)).distinct()

    def get_q_object(self, instance_prefix):
        """Return a Q object to only show the entries with active ACL.

        The Q object will filter a queryset such that only entries are returned
        where the current user has an active InstanceACL.

        In contrast to the `filter_queryset()` method above, this is useful if
        you need to invert the filtering mechanism, or combine it with other
        expressions (combine using OR to extend visibilities for example)
        """

        acl_prefix = f"{instance_prefix}__acls" if instance_prefix else "acls"
        filter = InstanceACL.filter_for_current_user(
            **self.userinfo.to_kwargs(), acl_prefix=acl_prefix
        )
        return filter

    def involved_services(self, instance: Instance) -> QuerySet:
        """Return a queryset of involved services for the given instance.

        Note: Only active ACLs are taken into account. Future or expired ACLs
        are considered as "not involved"
        """
        acls = (
            models.InstanceACL.currently_active()
            .filter(instance=instance)
            .filter(grant_type=GRANT_CHOICES.SERVICE.value)
        )
        services = Service.objects.filter(pk__in=Subquery(acls.values("service")))
        return services


def grant(instance, **kwargs):
    """Shortcut grant for "anonymous" users (ie system, testing).

    You should probably always go through the PermissionManager instead.
    """
    return PermissionManager.for_anonymous().grant(instance, **kwargs)


def revoke(acl: InstanceACL, ends_at: Optional[datetime] = None, **kwargs):
    """Shortcut revoke for "anonymous" users (ie system, testing).

    You should probably always go through the PermissionManager instead.
    """
    # Any revocation clears the permissions cache for the affected instance
    return PermissionManager.for_anonymous().revoke(acl, ends_at=ends_at, **kwargs)


def _validate_grant(  # noqa: C901
    grant_type,
    user,
    service,
    token,
    ends_at,
    starting_at,
    access_level,
):
    if (
        access_level.required_grant_type
        and access_level.required_grant_type != grant_type
    ):
        raise exceptions.GrantValidationError(
            f"Access level requires grant type {access_level.required_grant_type}"
        )

    if grant_type == models.GRANT_CHOICES.USER.value:
        is_ok = user and not service and not token
        if not is_ok:
            raise exceptions.GrantValidationError(
                "Grant type USER must have only the `user` value set"
            )
    elif grant_type == models.GRANT_CHOICES.SERVICE.value:
        is_ok = service and not user and not token
        if not is_ok:
            raise exceptions.GrantValidationError(
                "Grant type SERVICE must have only the `service` value set"
            )
    elif grant_type == models.GRANT_CHOICES.TOKEN.value:
        is_ok = token and not service and not user
        if not is_ok:
            raise exceptions.GrantValidationError(
                "Grant type TOKEN must have only the `token` value set"
            )
    elif grant_type in [
        models.GRANT_CHOICES.ANONYMOUS_PUBLIC.value,
        models.GRANT_CHOICES.AUTHENTICATED_PUBLIC.value,
    ]:
        if user or service or token:
            raise exceptions.GrantValidationError(
                "Anonymous grants must not have user or service or token"
            )
    else:
        raise exceptions.GrantValidationError(f"Unhandled grant type {grant_type}")

    if ends_at and ends_at <= starting_at:
        raise exceptions.GrantValidationError(
            "End time must be either None or later than start time"
        )


def _clear_cache_for_acl(acl):
    """Clear cache for the instance affected by this ACL.

    This is required, because when revoking an ACL, this may affect an undefined
    set of user's access to that instance. We "naively" evict any related cache
    to ensure the next permissions check actually checks the new situation.
    """
    # Not sure we should keep this.. but it's the only way found (till now)
    # Note we cannot check for 'key startswith prefix', as the LocmemCache
    # does the versioning by prefixing our key with the version, which we don't
    # use
    actual_cache = cache._connections["default"]
    if hasattr(actual_cache, "keys"):  # pragma: no cover
        # REDIS, MEMCACHE etc have this.
        # TODO: Maybe we can mock a "proper" cache to test these lines?
        revoke_keys = actual_cache.keys(f"permissions:i={acl.instance_id},.*")
        cache.delete_many(keys=revoke_keys)
    else:
        # LocmemCache - we can't reliably find keys with given
        # prefix, so we just evict all. This should only happen in testing,
        # as we normally do have a Memcache instance connected
        cache.clear()
