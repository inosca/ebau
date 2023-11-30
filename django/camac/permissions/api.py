from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Union

from django.conf import settings
from django.core.cache import cache
from django.utils import timezone

from camac.instance.models import Instance
from camac.permissions import models
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

    @classmethod
    def from_request(cls, request):
        # TODO: Token ACL is not specified yet, so this part is always unset

        user = request.user if hasattr(request, "user") else None
        try:
            service = request.group.service
        except AttributeError:
            service = None

        return cls(
            user=user,
            service=service,
            token=None,
        )

    def to_kwargs(self):
        return {"user": self.user, "service": self.service, "token": self.token}

    def to_cache_key(self, instance: Instance):
        user = self.user.pk if self.user else "-"
        service = self.service.pk if self.service else "-"
        token = self.token.pk if self.token else "-"

        # The instance is first, so we can match better when revoking permissions
        return f"permissions:i={instance.pk},u={user},s={service},t={token}"


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

    def get_permissions(self, instance: Instance) -> List[str]:
        cache_key = self.userinfo.to_cache_key(instance)
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        acls = (
            models.InstanceACL.for_current_user(**self.userinfo.to_kwargs())
            .filter(instance=instance)
            .select_related("access_level")
        )

        granted_permissions = []
        # We try to cache rather long
        expiry = timezone.now() + timedelta(days=10)

        for acl in acls:
            access_level = acl.access_level
            permissions = settings.PERMISSIONS["ACCESS_LEVELS"][access_level.slug]
            if acl.end_time:
                # shorten expiry for the cache
                expiry = min(expiry, acl.end_time)

            for perm, condition in permissions:
                if callable(condition):
                    # This is a dynamic permission
                    kwargs = _get_callback_kwargs(
                        condition, {"userinfo": self.userinfo, "instance": instance}
                    )
                    if condition(**kwargs):
                        granted_permissions.append(perm)
                elif condition == "*" or condition == instance.instance_state:
                    granted_permissions.append(perm)
                # else: condition didn't match - permission not granted

        cache_duration = expiry - timezone.now()
        cache.set(cache_key, granted_permissions, cache_duration.total_seconds())
        return granted_permissions

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
        acl_prefix = f"{instance_prefix}__acls" if instance_prefix else "acls"
        filter = InstanceACL.filter_for_current_user(
            **self.userinfo.to_kwargs(), acl_prefix=acl_prefix
        )
        return queryset.filter(filter)


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


def _get_callback_kwargs(callback, possible_kwargs):
    """Return only the kwargs that the given callback accepts."""
    new_kwargs = {}
    for k, v in possible_kwargs.items():
        if k in callback.__code__.co_varnames:
            new_kwargs[k] = v
    return new_kwargs
