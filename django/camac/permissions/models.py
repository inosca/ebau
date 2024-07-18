import operator
from functools import reduce

from django.db import models
from django.utils import timezone
from localized_fields.fields import LocalizedTextField

from camac.instance import models as instance_models
from camac.user import models as user_models

from . import exceptions

# Create your models here.


class GRANT_CHOICES(models.TextChoices):
    # Grant type: Service means user must be in the linked
    # service, AND the x-camac-group header refers to a group
    # linked to said service.
    SERVICE = "SERVICE", "Service"

    # Grant type: Role means user must have the linked
    # role, AND the x-camac-group header refers to a group
    # linked to said role.
    ROLE = "ROLE", "Role"

    # User directly linked
    USER = "USER", "User"

    # Public authenticated users are all users, regardless of association
    AUTHENTICATED_PUBLIC = "AUTHENTICATED_PUBLIC", "Authenticated Public"

    # Anonymous public users are those who are not authenticated at all
    ANONYMOUS_PUBLIC = "ANONYMOUS_PUBLIC", "Anonymous Public"

    # Users are able to provide a token
    TOKEN = "TOKEN", "Token"


class APPLICABLE_AREAS(models.TextChoices):
    PUBLIC = "PUBLIC", "Public"
    APPLICANT = "APPLICANT", "Applicant"
    INTERNAL = "INTERNAL", "Internal"
    ANY = "ANY", "Any"


class AccessLevel(models.Model):
    slug = models.SlugField(max_length=100, primary_key=True)

    name = LocalizedTextField()
    description = LocalizedTextField()

    # TODO this may be better of as a list field - some access levels may
    # allow multiple grant types, not just one
    required_grant_type = models.CharField(
        # If set, only the an ACL of the given grant type is allowed to
        # reference this access level. For example: Access level used for
        # internal services MUST be of type SERVICE, it cannot be granted
        # to a single USER, let alone ANONYMOUS_PUBLIC
        max_length=50,
        choices=GRANT_CHOICES.choices,
        null=True,
        blank=True,
    )

    applicable_area = models.CharField(
        max_length=50,
        default=APPLICABLE_AREAS.ANY.value,
        choices=APPLICABLE_AREAS.choices,
    )


class InstanceACL(models.Model):
    instance = models.ForeignKey(
        instance_models.Instance, on_delete=models.CASCADE, related_name="acls"
    )

    access_level = models.ForeignKey(
        AccessLevel, on_delete=models.DO_NOTHING, related_name="acls"
    )

    # One (and exactly one) of user,service,token must be set to identify
    # which users are affected
    user = models.ForeignKey(
        user_models.User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="acls",
    )
    service = models.ForeignKey(
        user_models.Service,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="acls",
    )
    role = models.ForeignKey(
        user_models.Role,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="instance_acls",
    )
    token = models.CharField(max_length=250, null=True, blank=True, default=None)

    # Duration for which the ACL is valid/active: start_time / end_time
    start_time = models.DateTimeField(
        default=timezone.now, help_text="At this time, the ACL becomes valid"
    )
    end_time = models.DateTimeField(
        null=True, default=None, help_text="At this time, the ACL becomes invalid"
    )

    # all "auditing" foreign keys are nullable, and return to NULL if their
    # reference is deleted, so let's apply some DRY
    _audit_fkey_args = dict(
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    created_by_user = models.ForeignKey(user_models.User, **_audit_fkey_args)
    revoked_by_user = models.ForeignKey(user_models.User, **_audit_fkey_args)
    created_by_service = models.ForeignKey(user_models.Service, **_audit_fkey_args)
    revoked_by_service = models.ForeignKey(user_models.Service, **_audit_fkey_args)

    del _audit_fkey_args

    created_by_event = models.CharField(max_length=250, null=True, blank=True)
    revoked_by_event = models.CharField(max_length=250, null=True, blank=True)

    grant_type = models.CharField(max_length=50, choices=GRANT_CHOICES.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    revoked_at = models.DateTimeField(null=True, default=None, blank=True)
    metainfo = models.JSONField(null=True, default=None)

    @classmethod
    def for_current_user(
        cls, user=None, service=None, token=None, area=None, role=None
    ):
        """Return a QS with all the ACLs of the given user."""
        filter = cls.filter_for_current_user(
            user=user,
            service=service,
            token=token,
            acl_prefix="",
            area=area,
            role=role,
        )
        return cls.objects.filter(filter)

    @classmethod
    def filter_for_current_user(
        cls, user=None, service=None, token=None, acl_prefix="", area=None, role=None
    ):
        """Generate a filter for the current user.

        Note that the user at this level is represented by the relevant
        attributes, not a request object.
        """
        # The prefix for our callers should not need ot end with '__':
        # If we're actually filtering ACLs, it's empty, but if it's set,
        # we'll need to separate it, so it becomes foo__acls__the_actual_field
        prefix = f"{acl_prefix}__" if acl_prefix else ""

        # First, figure out which ACLs belong to the user (via one of the
        # applicable paths)
        user_filter_parts = []

        # If anonymous-public access is granted, it's irrelevant if we have
        # a requesting-user or not
        user_filter_parts.append(
            models.Q(**{f"{prefix}grant_type": GRANT_CHOICES.ANONYMOUS_PUBLIC.value})
        )

        if user:
            # We have a user - check for directly-assigned ACLs
            # or "authenticated-public" ones
            user_filter_parts.append(models.Q(**{f"{prefix}user": user}))
            user_filter_parts.append(
                models.Q(
                    **{f"{prefix}grant_type": GRANT_CHOICES.AUTHENTICATED_PUBLIC.value}
                )
            )
        if service:
            user_filter_parts.append(models.Q(**{f"{prefix}service": service}))

            if area is None:
                area = APPLICABLE_AREAS.INTERNAL.value
        if role:
            user_filter_parts.append(models.Q(**{f"{prefix}role": role}))
        elif area is None and not service and not role:  # pragma: no cover
            # No service, and is_portal_user was not explicitly passed.
            # Assume public mode.
            # TODO: this should never happen, but I'm hesitant to raise
            # an exception.
            area = APPLICABLE_AREAS.PUBLIC.value

        if token:
            user_filter_parts.append(models.Q(**{f"{prefix}token": token}))

        # We only consider ACLs with access levels in the user's current
        # area of the application, as well as "any" which applies everywhere
        acceptable_areas = [area, APPLICABLE_AREAS.ANY.value]
        area_filter = models.Q(
            **{f"{prefix}access_level__applicable_area__in": acceptable_areas}
        )

        user_filter = reduce(operator.or_, user_filter_parts)

        return user_filter & cls.filter_active(acl_prefix=acl_prefix) & area_filter

    @classmethod
    def filter_active(cls, acl_prefix):
        prefix = f"{acl_prefix}__" if acl_prefix else ""
        now = timezone.now()

        # ACL is valid if start time is in the past (or right now)
        # AND end time is either unset or in the future
        time_filter = models.Q(**{f"{prefix}start_time__lte": now}) & (
            models.Q(**{f"{prefix}end_time__gt": now})
            | models.Q(**{f"{prefix}end_time__isnull": True})
        )
        return time_filter

    @classmethod
    def currently_active(cls):
        return cls.objects.filter(cls.filter_active(acl_prefix=None))

    def revoke(self, ends_at=None):
        """Revoke this ACL.

        If `ends_at` is given, the ACL will be revoked at that
        time. If it is not given, the ACL is revoked *right now*.

        Note: You still need to save() the ACL
        """
        now = timezone.now()
        if ends_at and ends_at <= now:
            # Logically, we'd need to do `ends_at < now`, but for testability,
            # we assume "exactly now" already as past
            raise exceptions.RevocationRejected(
                "Cannot set end time to past. If you want to revoke "
                "the ACL immediately, call revoke without end time"
            )

        # If ends_at is set to None, it means immediate revocation
        ends_at = ends_at or now

        self.revoked_at = now

        if self.end_time is not None and self.end_time < ends_at:
            raise exceptions.RevocationRejected("Cannot extend ACL's lifetime")
        self.end_time = ends_at

    def is_active(self):
        now = timezone.now()
        has_started = self.start_time <= now
        has_ended = self.end_time and self.end_time < now

        return has_started and not has_ended

    def __str__(self):  # pragma: no cover
        act = "active" if self.is_active() else "inact"
        return (
            f"InstanceACL({self.pk};i={self.instance_id};{self.access_level_id};{act})"
        )
