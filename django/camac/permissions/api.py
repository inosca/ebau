from __future__ import annotations

import operator
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import reduce
from typing import List, Optional, Union

from django.conf import ImproperlyConfigured, settings
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db.models import Exists, OuterRef, Q, QuerySet, Subquery
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import PermissionDenied

from camac.instance.models import Instance
from camac.permissions import models
from camac.permissions.conditions import PermissionContext, Static
from camac.permissions.models import AccessLevel, InstanceACL
from camac.user import models as user_models
from camac.user.models import Role, Service, ServiceGroup, User

from . import exceptions

# for direct access
GRANT_CHOICES = models.GRANT_CHOICES


class P:
    """P classes to be used for representing complex permission requirements.

    Sometimes, one action might be allowed by multiple permissions, or one
    action might require more than one permission.

    Some examples:

    # Specify both "foo" and "bar" permissions are required
    >>> permission_manager.has_permission(P('foo') & P('bar'))

    # You can pass in multiple permissions directly, this is equivalent
    # above line to the
    >>> permission_manager.has_permission(P('foo', 'bar'))

    # Specify either "foo" or "bar" permissions are required
    >>> permission_manager.has_permission(P('foo') | P('bar'))

    # Similarly, multiple permissions can be passed, with the operator
    # explicitly set to "or", to denote "at least one is needed". The
    # following line is equivalent to the previous one
    >>> permission_manager.has_permission(P.any('foo', 'bar'))

    The expressions can be combined as well, of course. A more realistic,
    complex example is this: Assume you have an "action-all" permission that
    allows all actions in a module, as well as the finer-grained "action-a" and
    "action-b" permissions: If one operation requires both permissions, you can
    now check it like this:

    >>> permission_manager.has_permission(P("action-all") | P("action-a", "action-b"))
    """

    def __init__(self, *perm_names, op=operator.and_):
        if not callable(op):
            op = {"or": operator.or_, "and": operator.and_}[op]

        self._perms = perm_names
        self._op = op

    @classmethod
    def any(cls, *perms):
        """Return a P expression from the given permissions, combines with OR.

        The following two lines are equivalent:
        >>> P("foo") | P("bar")
        >>> P("foo", "bar", op="or")
        >>> P.any("foo", "bar")
        """
        return cls(*perms, op=operator.or_)

    @classmethod
    def all(cls, *perms):
        """Return a P expression from the given permissions, combines with OR.

        The following two lines are equivalent:
        >>> P("foo") & P("bar")
        >>> P("foo", "bar")
        >>> P("foo", "bar", op="and")
        >>> P.all("foo", "bar")
        """
        return cls(*perms, op=operator.and_)

    def apply(self, has_perms: list[str]) -> bool:
        """Check if the permission expression is satisfied by the given permissions."""

        def _check(perm, have_perms: list[str]) -> bool:
            if isinstance(perm, str):
                return perm in have_perms
            return perm.apply(has_perms)

        return reduce(self._op, (_check(p, has_perms) for p in self._perms))

    def _collect_referenced_permissions(self):
        for perm in self._perms:
            if isinstance(perm, str):
                yield perm
            else:
                yield from perm._collect_referenced_permissions()

    def __and__(self, other):
        return P(self, other, op=operator.and_)

    def __or__(self, other):
        return P(self, other, op=operator.or_)

    def __eq__(self, other):
        return (
            isinstance(other, P)
            and self._perms == other._perms
            and self._op == other._op
        )

    def __repr__(self):
        op_symbols = {operator.and_: " & ", operator.or_: " | "}
        op_symbol = op_symbols[self._op]

        return f"P({op_symbol.join([str(p) for p in self._perms])})"


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
        if isinstance(user, AnonymousUser):
            user = None

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

        The kwargs dict consists of the keys `user`, `service`, `role`, `token`
        and `area` - suitable for passing along to the filtering methods in
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
            "role": self.role,
        }

    def to_cache_key(self, context: PermissionContext) -> str:
        instance_id = context.instance.pk
        context_key = context.as_cache_key() or "-"
        role = self.role.pk if self.role else "-"
        user = self.user.pk if self.user else "-"
        service = self.service.pk if self.service else "-"
        token = self.token.pk if self.token else "-"

        parts = [
            f"i={instance_id}",
            f"c={context_key}",
            f"r={role}",
            f"u={user}",
            f"s={service}",
            f"t={token}",
        ]

        # The instance is first, so we can match better when revoking permissions
        return f"permissions:{','.join(parts)}"


@dataclass
class PermissionScope:
    _manager: PermissionManager
    _context: PermissionContext

    def has(self, permission: P | str) -> bool:
        return self._manager.has_permission(self._context, permission)

    def require(self, permission: P | str) -> None:
        return self._manager.require_all(self._context, permission)

    def get_permissions(self) -> list[str]:
        return self._manager.get_permissions(self._context)


class PermissionManager:
    userinfo: ACLUserInfo
    default_event: Optional[str] = None

    def __init__(self, userinfo: ACLUserInfo, permission_settings=None):
        self.permission_settings = permission_settings or settings.PERMISSIONS
        self.userinfo = userinfo

    def scoped_for(self, context: PermissionContext) -> PermissionScope:
        """Scope manager to an given context."""

        return PermissionScope(self, context)

    @classmethod
    def for_anonymous(cls) -> "PermissionManager":
        userinfo = ACLUserInfo(user=None, service=None, token=None)
        return cls(userinfo=userinfo)

    @classmethod
    def from_params(
        cls, user=None, service=None, token=None, role=None
    ) -> "PermissionManager":
        userinfo = ACLUserInfo(user=user, service=service, token=token, role=role)
        return cls(userinfo=userinfo)

    @classmethod
    def from_request(cls, request, permission_settings=None) -> "PermissionManager":
        userinfo = ACLUserInfo.from_request(request)
        return cls(userinfo=userinfo, permission_settings=permission_settings)

    def context_from(self, instance, **kwargs):
        if isinstance(instance, PermissionContext):  # pragma: no cover
            # already is a context
            return instance
        if not isinstance(instance, Instance):
            # assume it's a PK
            instance = Instance.objects.get(pk=instance)
        return PermissionContext(instance)

    def get_relevant_acls(self, context):
        return (
            models.InstanceACL.for_current_user(**self.userinfo.to_kwargs())
            # this filter should work regardless of whether `instance`
            # is a model or just an FK reference
            .filter(instance=context.instance)
            .select_related("access_level")
        )

    def _static_permissions_by_level(self):
        collected = defaultdict(list)
        for level, perms in self.permission_settings["ACCESS_LEVELS"].items():
            for perm, check in perms:
                if isinstance(check, Static) or check is Static:
                    collected[level].append(perm)
        return dict(collected)

    def get_static_permission_acl_map(self) -> dict[str, models.InstanceACL.QuerySet]:
        """
        Return a dict that maps every static permission to an ACL queryset.

        For every static permission that is configured, a QS is returned
        that contains every `InstanceACL` where that permission is granted.
        This allows you to build a visibility check that uses these permissions.
        """
        perm_info = self._static_permissions_by_level()

        flipped = defaultdict(set)  # perm -> access level
        for level, perms in perm_info.items():
            for perm in perms:
                flipped[perm].add(level)

        base_qs = models.InstanceACL.for_current_user(**self.userinfo.to_kwargs())

        return {
            perm: base_qs.filter(access_level_id__in=levels)
            for perm, levels in flipped.items()
        }

    def static_permission_expr(self, permission: str, instance_prefix: str = None):
        """
        Return a Q / Exists expression to check for a given static permission.

        If the instance prefix is not given, it is assumed to be an instance
        queryset.
        """
        acls = self.get_acls_for_static_permission(permission)

        instance_ref = f"{instance_prefix}__pk" if instance_prefix else "pk"

        return Exists(acls.filter(instance_id=OuterRef(instance_ref)))

    def get_acls_for_static_permission(self, perm):
        the_map = self.get_static_permission_acl_map()
        if perm not in the_map:  # pragma: no cover
            raise ImproperlyConfigured(f"Static permission '{perm}' is not configured")
        return the_map[perm]

    def get_permissions(
        self,
        context: PermissionContext | Instance,
        check_only: Optional[List[str]] = None,
    ) -> List[str]:
        """
        Return permissions of the user in the current context.

        The permission conditions of the granted acls' access levels are
        evaluated, and all applicable permissions are returned.

        If you pass a list of permissions (as a list of strings) to check_only,
        then only those permissions are queried.
        This can be much faster, but should only be used if you know that no
        (or very few) other permissions will be checked in the same request.
        """
        # We can globally disable the cache. By default, caching is enabled,
        # but during development, it can be disabled so any stale permissions
        # won't be kept around
        enable_cache = self.permission_settings.get("ENABLE_CACHE", True)

        if not isinstance(context, PermissionContext):
            context = self.context_from(context)

        cache_key = self.userinfo.to_cache_key(context)

        cached_result = cache.get(cache_key)
        if enable_cache and cached_result:
            return cached_result

        acls = self.get_relevant_acls(context)

        granted_permissions = set()
        # We try to cache rather long
        expiry = timezone.now() + timedelta(days=10)

        for acl in acls:
            access_level = acl.access_level
            if acl.end_time:
                # shorten expiry for the cache
                expiry = min(expiry, acl.end_time)

            for perm, condition in self._access_level_config(access_level.slug):
                if (check_only is not None) and perm not in check_only:
                    continue

                # Cache gets disabled on the first condition that doesn't
                # allow caching
                enable_cache = enable_cache and condition.allow_caching

                try:
                    if condition.apply(userinfo=self.userinfo, context=context):
                        granted_permissions.add(perm)
                except Exception as e:  # pragma: no cover
                    raise ImproperlyConfigured(
                        f"Failed to evaluate permission condition: {condition}"
                    ) from e

        permissions_sorted = sorted(granted_permissions)
        if enable_cache:
            cache_duration = expiry - timezone.now()
            cache.set(cache_key, permissions_sorted, cache_duration.total_seconds())
        return permissions_sorted

    def has_any(
        self,
        context: Instance | PermissionContext,
        required_permissions: Union[str, List[str]],
        check_only_required: bool = False,
    ):
        """Return True if user has at least one of the required permissions.

        The required_permissions can be either a single permission as a string,
        or a list of permissions (as a list of strings).

        If you pass `check_only_required=True`, then only the required
        permissions are queried.
        This can be much faster, but should only be used if you know that no
        (or very few) other permissions will be checked in the same request.
        """
        if isinstance(required_permissions, str):
            required_permissions = [required_permissions]
        return self.has_permission(
            context, P.any(*required_permissions), check_only_required
        )

    def _referenced_permissions(self, require_expr, check_only_required: bool):
        if check_only_required:
            return list(require_expr._collect_referenced_permissions())

        return None

    def has_permission(
        self,
        context: Instance | PermissionContext,
        require_expr: str | P,
        check_only_required: bool = False,
    ):
        """
        Return True if the user in the current context has the required permissions.

        The require_expr can be either a single permission as a string, or a
        P expression for more complex checks.

        If you pass `check_only_required=True`, then only the required
        permissions are queried.
        This can be much faster, but should only be used if you know that no
        (or very few) other permissions will be checked in the same request.
        """
        if isinstance(require_expr, str):
            require_expr = P(require_expr)

        return require_expr.apply(
            self.get_permissions(
                context,
                check_only=self._referenced_permissions(
                    require_expr, check_only_required
                ),
            )
        )

    def has_all(
        self,
        context: Instance | PermissionContext,
        required_permissions: Union[str, List[str]],
        check_only_required: bool = False,
    ):
        """Return True if user has all required permissions.

        The required_permissions can be either a single permission as a string,
        or a list of permissions (as a list of strings).

        If you pass `check_only_required=True`, then only the required
        permissions are queried.
        This can be much faster, but should only be used if you know that no
        (or very few) other permissions will be checked in the same request.
        """
        if isinstance(required_permissions, str):
            required_permissions = [required_permissions]

        return self.has_permission(
            context, P.all(*required_permissions), check_only_required
        )

    def require_any(
        self,
        context: Instance | PermissionContext,
        required_permissions: Union[str, List[str]],
    ):
        """Enforce presence of at least one of the given permissions."""
        if self.has_any(context, required_permissions):
            return
        raise PermissionDenied(_("You do not have the required permission to do this"))

    def require_all(
        self,
        context: Instance | PermissionContext,
        required_permissions: Union[str, List[str]],
    ):
        """Enforce presence of all of the given the given permissions."""
        if self.has_all(context, required_permissions):
            return
        raise PermissionDenied(_("You do not have the required permission to do this"))

    def _access_level_config(self, access_level_slug):
        """Return the config for the given access level.

        The result is a list of (permission, condition) tuples (see the
        `camac.settings.modules.permissions` module, or the permission module
        documentation for details)
        """
        try:
            return self.permission_settings["ACCESS_LEVELS"][access_level_slug]
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
        service_group: Optional[ServiceGroup] = None,
        role: Optional[Role] = None,
        token: Optional[str] = None,
        starting_at: Optional[datetime] = None,
        ends_at: Optional[datetime] = None,
        event_name: Optional[str] = None,
        **additional_attrs,
    ):
        """Grant permissions by creating a new ACL on the given Instance.

        Depending on the `grant_type` given, the parameters `user`,
        `service`, `service_group`, `role` or `token` may be required or disallowed.

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
            service_group=service_group,
            token=token,
            role=role,
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
            service_group=service_group,
            token=token,
            role=role,
            end_time=ends_at,
            created_by_user=self.userinfo.user,
            created_by_event=event_name,
            created_by_service=self.userinfo.service,
            revoked_by_user=self.userinfo.user if ends_at else None,
            **additional_attrs,
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

    def get_q_object(self, instance_prefix, only_level=None):
        """Return a Q object to only show the entries with active ACL.

        The Q object will filter a queryset such that only entries are returned
        where the current user has an active InstanceACL.

        In contrast to the `filter_queryset()` method above, this is useful if
        you need to invert the filtering mechanism, or combine it with other
        expressions (combine using OR to extend visibilities for example)

        If you pass `only_level="some_access_level"`, only ACLs with the
        given level are considered.
        """

        acl_prefix = f"{instance_prefix}__acls" if instance_prefix else "acls"
        filter = InstanceACL.filter_for_current_user(
            **self.userinfo.to_kwargs(), acl_prefix=acl_prefix
        )

        if only_level:
            filter = filter & Q(**{f"{acl_prefix}__access_level_id": only_level})
        return filter

    def current_access_levels(self, instance=None) -> list[str]:
        """Return a list of access level slugs relevant for the current user.

        The list spans all access levels that the user has in any possible
        situation. Useful for building visibility queries.

        If the `instance` parameter is given, only the access levels that
        are granted on that instance are returned.
        """
        qs = models.InstanceACL.for_current_user(**self.userinfo.to_kwargs())
        if instance:
            qs = qs.filter(instance=instance)

        return list(
            qs.distinct("access_level_id").values_list("access_level_id", flat=True)
        )

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
    service_group,
    role,
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

    # Ensure given grant type is valid
    if grant_type not in models.GRANT_CHOICES:
        raise exceptions.GrantValidationError(f"Unhandled grant type {grant_type}")

    # Anonymous must not have any parameters. All others (parametrized ones)
    # must have exactly one (and the right one as well).
    only_one = {
        "SERVICE": service,
        "SERVICE_GROUP": service_group,
        "TOKEN": token,
        "ROLE": role,
        "USER": user,
    }
    has_required_param = only_one.pop(grant_type, None)
    anonymous_ok = not has_required_param and not any(only_one.values())
    parametrized_ok = has_required_param and not any(only_one.values())

    is_anonymous = grant_type in (
        models.GRANT_CHOICES.ANONYMOUS_PUBLIC.value,
        models.GRANT_CHOICES.AUTHENTICATED_PUBLIC.value,
    )
    is_parametrized = not is_anonymous

    if is_anonymous and not anonymous_ok:
        # ANONYMOUS_* are unparametrized grant types - they are not limiting
        # audience to a specific user group. If we reach this, then there's at
        # least one limiting parameter given that we do not want.
        raise exceptions.GrantValidationError(
            "Anonymous grants must not have user, service, service_group, role or token"
        )
    elif is_parametrized and not parametrized_ok:
        # All "parametrized" grant types must have exactly the matching
        # parameter given for the grant type, and none of the other parameters.
        param = grant_type.lower()
        raise exceptions.GrantValidationError(
            f"Grant type {grant_type} must have only the `{param}` value set"
        )

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
