import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List

from camac.utils import call_with_accepted_kwargs

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


class Check(ABC):
    @abstractmethod
    def apply(self, userinfo, instance):  # pragma: no cover
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


class BinaryCheck(Check):
    def __init__(self, left, right, op):
        self._left = left
        self._right = right
        self._op = op

    def apply(self, userinfo, instance):
        return self._op(
            self._left.apply(userinfo=userinfo, instance=instance),
            self._right.apply(userinfo=userinfo, instance=instance),
        )

    def __repr__(self):
        opname = self._op.__name__.strip("_")
        return f"BinaryCheck({opname}, {self._left!r}, {self._right!r})"

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

    def apply(self, userinfo, instance):
        return self._op(self._inner.apply(userinfo=userinfo, instance=instance))

    def __repr__(self):
        opname = self._op.__name__.strip("_")
        return f"UnaryCheck({opname}{self._inner!r})"

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

    def apply(self, userinfo, instance):
        return any(userinfo.role.name == role for role in self.required_roles)

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasRole) and set(other.required_roles) == set(
            self.required_roles
        )

    def __repr__(self):
        return f"HasRole:{sorted(self.required_roles)}"


@dataclass
class Callback(Check):
    check_function: Callable
    allow_caching: bool = field(default=False)

    def apply(self, userinfo, instance):
        return call_with_accepted_kwargs(
            self.check_function, userinfo=userinfo, instance=instance
        )

    def __eq__(self, other):  # pragma: no cover
        return (
            isinstance(other, Callback) and other.check_function == self.check_function
        )


@dataclass
class RequireInstanceState(Check):
    """Permission check: Require instance is in one of the configured states."""

    require_states: List[str]

    def apply(self, userinfo, instance):
        return instance.instance_state.name in self.require_states

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
        return f"RequireInstanceState({sorted(self.require_states)})"


class HasInquiry(Check):
    """Permission check: User is involved in an inquiry."""

    def apply(self, userinfo, instance):
        return instance.has_inquiry(userinfo.service.pk)

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasInquiry)


class IsAppeal(Check):
    """Permission check: Instance (case) has an appeal."""

    def apply(self, userinfo, instance):
        return bool(instance.case.meta.get("is-appeal"))

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsAppeal)


class Always(Check):
    """Always grant the permission."""

    def apply(self, userinfo, instance):
        return True

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, Always)

    def __repr__(self):  # pragma: no cover
        return "PermissionCondition:Always"


class Never(Check):
    """Never grant the permission."""

    def apply(self, userinfo, instance):
        return False

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, Never)

    def __repr__(self):  # pragma: no cover
        return "PermissionCondition:Never"
