import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List

from camac.utils import call_with_accepted_kwargs

"""
Provide some useful conditionals to build complex permissions checks.

See the docs (configuration.md) for examples and explanation.
The conditionals here are composable, so for example:
`HasRole(["municipality"]) & InstanceState(["redacting"])`
will only evaluate to True if the instance state's name is "redacting"
and the user has the role named "municipality". (The role needs to be
active via the X-CAMAC-GROUP HTTP header)
"""


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
        return f"BinaryCheck({opname}, {self._left}, {self._right})"

    @property
    def allow_caching(self):  # pragma: no cover
        return self._left.allow_caching and self._right.allow_caching


class UnaryCheck(Check):
    def __init__(self, inner, op):
        self._inner = inner
        self._op = op

    def apply(self, userinfo, instance):
        return self._op(self._inner.apply(userinfo=userinfo, instance=instance))

    def __repr__(self):
        opname = self._op.__name__.strip("_")
        return f"UnaryCheck({opname}{self._inner})"

    @property
    def allow_caching(self):  # pragma: no cover
        return self._inner.allow_caching


@dataclass
class HasRole(Check):
    """Permission check for requiring any role of a given list."""

    required_roles: List[str]

    def apply(self, userinfo, instance):
        return any(userinfo.role.name == role for role in self.required_roles)

    @property
    def allow_caching(self):  # pragma: no cover
        return True


@dataclass
class Callback(Check):
    check_function: Callable
    allow_caching: bool = field(default=False)

    def apply(self, userinfo, instance):
        return call_with_accepted_kwargs(
            self.check_function, userinfo=userinfo, instance=instance
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


class Always(Check):
    """Always grant the permission."""

    def apply(self, userinfo, instance):
        return True

    @property
    def allow_caching(self):  # pragma: no cover
        return True


class Never(Check):
    """Never grant the permission."""

    def apply(self, userinfo, instance):
        return False

    @property
    def allow_caching(self):  # pragma: no cover
        return True
