import operator
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Callable, List, Optional

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
        return f"UnaryCheck({opname}, {self._inner!r})"

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
        return f"HasRole({', '.join(sorted(self.required_roles))})"


@dataclass
class Callback(Check):
    check_function: Callable
    allow_caching: bool = field(default=False)
    name: str = ""  # only used for logging

    def apply(self, userinfo, instance):
        return call_with_accepted_kwargs(
            self.check_function, userinfo=userinfo, instance=instance
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
        return f"RequireInstanceState({', '.join(sorted(self.require_states))})"


class HasInquiry(Check):
    """Permission check: User is involved in an inquiry."""

    def apply(self, userinfo, instance):
        return instance.has_inquiry(userinfo.service.pk)

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, HasInquiry)

    def __repr__(self):  # pragma: no cover
        return "HasInquiry()"


class IsAppeal(Check):
    """Permission check: Instance (case) has an appeal."""

    def apply(self, userinfo, instance):
        return bool(instance.case.meta.get("is-appeal"))

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsAppeal)

    def __repr__(self):  # pragma: no cover
        return "IsAppeal()"


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
        return "Always()"


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
        return "Never()"


@dataclass
class IsForm(Check):
    """Permission check for requiring any form of a given list."""

    forms: List[str]

    def apply(self, userinfo, instance):
        return any(instance.case.document.form_id == form for form in self.forms)

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsForm) and set(other.forms) == set(self.forms)

    def __repr__(self):
        return f"IsForm({', '.join(sorted(self.forms))})"


@dataclass
class HasApplicantRole(Check):
    """Permission check for requiring any applicant role of a given list."""

    roles: List[str]

    def apply(self, userinfo, instance):
        applicant = instance.involved_applicants.filter(invitee=userinfo.user).first()

        if not applicant:
            return False

        return any(applicant.role == role for role in self.roles)

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

    def apply(self, userinfo, instance):
        from camac.caluma.api import CalumaApi

        return CalumaApi().is_paper(instance)

    @property
    def allow_caching(self):  # pragma: no cover
        return True

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, IsPaper)

    def __repr__(self):  # pragma: no cover
        return "IsPaper()"


@dataclass
class RequireWorkItem(Check):
    """Require instance to have a work item of a given task."""

    task_id: str
    status: Optional[str] = None

    def apply(self, userinfo, instance):
        from caluma.caluma_workflow.models import WorkItem

        work_items = WorkItem.objects.filter(
            case__family=instance.case, task_id=self.task_id
        )

        if self.status:
            work_items = work_items.filter(status=self.status)

        return work_items.exists()

    @property
    def allow_caching(self):  # pragma: no cover
        return False

    def __eq__(self, other):  # pragma: no cover
        return isinstance(other, RequireInstanceState) and other.task_id == self.task_id

    def __repr__(self):  # pragma: no cover
        return f"RequireWorkItem({self.task_id})"
