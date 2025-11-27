from __future__ import annotations

import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Callable, List, Optional

from django.conf import ImproperlyConfigured

from camac.utils import call_with_accepted_kwargs, get_unversioned_slug

if TYPE_CHECKING:  # pragma: no cover
    from camac.instance.models import Instance

"""
Provide some useful conditionals to build complex permissions checks.

See the docs (configuration.md) for examples and explanation.
The conditionals here are composable, so for example:
`HasRole(["municipality"]) & RequireInstanceState(["redacting"])`
will only evaluate to True if the instance state's name is "redacting"
and the user has the role named "municipality". (The role needs to be
active via the X-CAMAC-GROUP HTTP header)
"""

# Note: The __eq__ and __repr__ methods are mostly used only for
# debugging and in a test that's currently marked `xfail`.
# Therefore they're not explicitly covered

OP_SYMBOLS = {
    operator.and_: "&",
    operator.or_: "|",
    operator.not_: "~",
}


@dataclass()
class PermissionContext:
    instance: Instance

    def as_cache_key(self) -> str | None:
        return None


class Check(ABC):
    @classmethod
    def composable(cls):
        return True

    @abstractmethod
    def apply(self, userinfo, context: PermissionContext):  # pragma: no cover
        ...

    def __and__(self, other):
        return BinaryCheck(self, other, operator.and_)

    def __or__(self, other):
        return BinaryCheck(self, other, operator.or_)

    def __invert__(self):
        return UnaryCheck(self, operator.not_)

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def enforce_composable(self, operand, label):
        if not operand.composable():
            raise ImproperlyConfigured(
                f"In {self!r}: {label} operand is not composable"
            )

    def __repr__(self):  # pragma: no cover
        return self.__class__.__name__


class BinaryCheck(Check):
    def __init__(self, left, right, op):
        self._left = left
        self._right = right
        self._op = op
        self.enforce_composable(left, "left")
        self.enforce_composable(right, "right")

    def apply(self, userinfo, context: PermissionContext):
        return self._op(
            self._left.apply(userinfo=userinfo, context=context),
            self._right.apply(userinfo=userinfo, context=context),
        )

    def __repr__(self):
        return f"{self._left!r} {OP_SYMBOLS[self._op]} {self._right!r}"

    @property
    def allow_caching(self):  # pragma: no cover
        return self._left.allow_caching and self._right.allow_caching

    def __eq__(self, other):  # pragma: no cover
        return (
            isinstance(other, BinaryCheck)
            and self._op == other._op
            and self._left == other._left
            and self._right == other._right
        )


class UnaryCheck(Check):
    def __init__(self, inner, op):
        self._inner = inner
        self._op = op
        self.enforce_composable(inner, "inner")

    def apply(self, userinfo, context: PermissionContext):
        return self._op(self._inner.apply(userinfo=userinfo, context=context))

    def __repr__(self):
        return f"{OP_SYMBOLS[self._op]}{self._inner!r}"

    @property
    def allow_caching(self):  # pragma: no cover
        return self._inner.allow_caching

    def __eq__(self, other):  # pragma: no cover
        return (
            isinstance(other, UnaryCheck)
            and self._op == other._op
            and self._inner == other._inner
        )


@dataclass
class HasRole(Check):
    """Permission check for requiring any role of a given list."""

    required_roles: List[str]

    def apply(self, userinfo, context: PermissionContext):
        return userinfo.role.name in self.required_roles

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasRole) and set(other.required_roles) == set(
            self.required_roles
        )

    def __repr__(self):
        return f"HasRole({', '.join(sorted(self.required_roles))})"


@dataclass
class Callback(Check):
    check_function: Callable
    allow_caching: bool = field(default=False)
    name: str = ""  # only used for logging

    def apply(self, userinfo, context: PermissionContext):
        return call_with_accepted_kwargs(
            self.check_function, userinfo=userinfo, instance=context.instance
        )

    def __eq__(self, other):  # pragma: no cover
        return (
            isinstance(other, Callback) and other.check_function == self.check_function
        )

    def __repr__(self):  # pragma: no cover
        return f"Callback({self.name})"


@dataclass
class RequireInstanceState(Check):
    """Permission check: Require instance is in one of the configured states."""

    require_states: List[str]
    condition_name: str | None = None

    def apply(self, userinfo, context: PermissionContext):
        return context.instance.instance_state.name in self.require_states

    @property
    def allow_caching(self):  # pragma: no cover
        # Instance state checks cannot allow caching, as state transitions
        # (currently) have no code to evict the relevant cache entries.
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, RequireInstanceState) and set(
            other.require_states
        ) == set(self.require_states)

    def __repr__(self):  # pragma: no cover
        if self.condition_name:
            return self.condition_name

        return f"RequireInstanceState({', '.join(sorted(self.require_states))})"


class HasInquiry(Check):
    """Permission check: User is involved in an inquiry."""

    def apply(self, userinfo, context: PermissionContext):
        return context.instance.has_inquiry(userinfo.service.pk)

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasInquiry)


class IsAppeal(Check):
    """Permission check: Instance (case) has an appeal."""

    def apply(self, userinfo, context: PermissionContext):
        return bool(context.instance.case.meta.get("is-appeal"))

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsAppeal)


class Always(Check):
    """Always grant the permission."""

    def apply(self, userinfo, context: PermissionContext):
        return True

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, Always)


class Static(Always):
    """
    Static permission is always granted, even globally.

    This should not be used in combination with other permissions, it needs
    to be granted top-level. This is used to define global permissions (on all
    instances where a corresponding ACL exists, of course) and therefore can
    be used in visibility rules.
    """

    @classmethod
    def composable(cls):
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, Static)


class Never(Check):
    """Never grant the permission."""

    def apply(self, userinfo, context: PermissionContext):
        return False

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, Never)


@dataclass
class IsForm(Check):
    """Permission check for requiring any form of a given list."""

    forms: List[str]

    def apply(self, userinfo, context: PermissionContext):
        return context.instance.case.document.form_id in self.forms

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsForm) and set(other.forms) == set(self.forms)

    def __repr__(self):
        return f"IsForm({', '.join(sorted(self.forms))})"


@dataclass
class IsUnversionedForm(IsForm):
    """Permission check for requiring any form of a given list ignoring versioned slugs."""

    def apply(self, userinfo, context: PermissionContext):
        return (
            get_unversioned_slug(context.instance.case.document.form_id) in self.forms
        )


@dataclass
class HasApplicantRole(Check):
    """Permission check for requiring any applicant role of a given list."""

    roles: List[str]

    def apply(self, userinfo, context: PermissionContext):
        applicant = context.instance.involved_applicants.filter(
            invitee=userinfo.user
        ).first()

        if not applicant:
            return False

        return applicant.role in self.roles

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasApplicantRole) and set(other.roles) == set(
            self.roles
        )

    def __repr__(self):
        return f"HasApplicantRole({', '.join(sorted(self.roles))})"


class IsPaper(Check):
    """Permission check: Instance (case) is a paper instance."""

    def apply(self, userinfo, context: PermissionContext):
        from camac.caluma.api import CalumaApi

        return CalumaApi().is_paper(context.instance)

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsPaper)


@dataclass
class RequireWorkItem(Check):
    """Require instance to have a work item of a given task."""

    task_id: str
    status: Optional[str] = None
    addressed_to_current_service: Optional[bool] = False
    condition_name: str | None = None

    def apply(self, userinfo, context: PermissionContext):
        from caluma.caluma_workflow.models import WorkItem

        work_items = WorkItem.objects.filter(
            case__family=context.instance.case, task_id=self.task_id
        )

        if self.status:
            work_items = work_items.filter(status=self.status)

        if self.addressed_to_current_service:
            work_items = work_items.filter(
                addressed_groups__contains=[str(userinfo.service.pk)]
            )

        return work_items.exists()

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, RequireInstanceState) and other.task_id == self.task_id

    def __repr__(self):  # pragma: no cover
        if self.condition_name:
            return self.condition_name

        return f"RequireWorkItem({self.task_id})"


@dataclass
class IsServiceGroup(Check):
    """Permission check for requiring any service group of a given list."""

    required_service_groups: List[str]
    allow_caching: bool = True

    def apply(self, userinfo, context: PermissionContext):
        if not userinfo.service:
            return False

        return userinfo.service.service_group.name in self.required_service_groups

    def __eq__(self, other: Check):  # pragma: no cover
        return isinstance(other, IsServiceGroup) and set(
            other.required_service_groups
        ) == set(self.required_service_groups)

    def __repr__(self):
        return f"IsServiceGroup({', '.join(sorted(self.required_service_groups))})"


@dataclass
class RequireDeadline(Check):
    """Permission check for requiring a instance deadline for the service."""

    def apply(self, userinfo, context: PermissionContext):
        return context.instance.deadlines.for_service(userinfo.service).exists()

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, RequireDeadline)

    def __repr__(self):
        return "RequireDeadline()"
