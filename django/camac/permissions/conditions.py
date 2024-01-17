import operator
from abc import ABC
from dataclasses import dataclass
from typing import List

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
    def __call__(self, userinfo, instance):
        """Compatibility with "pure" functional callback checks."""
        return call_with_accepted_kwargs(
            self.has_permission, userinfo=userinfo, instance=instance
        )

    def __and__(self, other):
        return BinaryCheck(self, other, operator.and_)

    def __or__(self, other):
        return BinaryCheck(self, other, operator.or_)

    def __invert__(self):
        return UnaryCheck(self, operator.not_)


class BinaryCheck(Check):
    def __init__(self, left, right, op):
        self._left = left
        self._right = right
        self._op = op

    def has_permission(self, userinfo, instance):
        return self._op(
            call_with_accepted_kwargs(
                self._left.has_permission, userinfo=userinfo, instance=instance
            ),
            call_with_accepted_kwargs(
                self._right.has_permission, userinfo=userinfo, instance=instance
            ),
        )

    def __repr__(self):
        opname = self._op.__name__.strip("_")
        return f"BinaryCheck({opname}{self._left}, {self._right})"


class UnaryCheck(Check):
    def __init__(self, inner, op):
        self._inner = inner
        self._op = op

    def has_permission(self, userinfo, instance):
        return self._op(
            call_with_accepted_kwargs(
                self._inner, userinfo=userinfo, instance=instance
            ),
        )

    def __repr__(self):
        opname = self._op.__name__.strip("_")
        return f"UnaryCheck({opname}{self._inner})"


@dataclass
class HasRole(Check):
    """Permission check for requiring any role of a given list."""

    required_roles: List[str]

    def has_permission(self, userinfo):
        return any(userinfo.role.name == role for role in self.required_roles)


@dataclass
class InstanceState(Check):
    """Permission check: Require instance is in one of the configured states."""

    require_states: List[str]

    def has_permission(self, instance):
        return any(
            instance.instance_state.name == state for state in self.require_states
        )


class Always(Check):
    """Always grant the permission."""

    def has_permission(self):
        return True


class Never(Check):
    """Never grant the permission."""

    def has_permission(self):
        return False
