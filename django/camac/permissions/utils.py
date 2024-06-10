from dataclasses import dataclass
from functools import singledispatch
from typing import List

from camac.instance.models import InstanceState
from camac.permissions.conditions import (
    Always,
    BinaryCheck,
    Check,
    Never,
    RequireInstanceState,
    UnaryCheck,
)


class IncompatibleCheck(Exception): ...


@singledispatch
def _validate_cond_for_extracting_allowed_states(c):
    raise IncompatibleCheck(f"given condition {c} is of incompatible type")


@_validate_cond_for_extracting_allowed_states.register
def _(c: RequireInstanceState):
    # This is the "base" that's easily compatible
    pass


@_validate_cond_for_extracting_allowed_states.register
def _(c: UnaryCheck):
    _validate_cond_for_extracting_allowed_states(c._inner)


@_validate_cond_for_extracting_allowed_states.register
def _(c: BinaryCheck):
    _validate_cond_for_extracting_allowed_states(c._left)
    _validate_cond_for_extracting_allowed_states(c._right)


# Always and Never can be accepted as well
@_validate_cond_for_extracting_allowed_states.register
def _(c: Always): ...
@_validate_cond_for_extracting_allowed_states.register
def _(c: Never): ...


def extract_allowed_states(cond: Check) -> List[str]:
    """List all instance states (untranslated names) that the condition allows.

    Note: This really only works with `RequireInstanceState` conditions
    as well as combinations (&, |, ~) of them.
    """

    # Any other check has something to do with other aspects of an instance
    # and thus we cannot extract allowed states from it
    _validate_cond_for_extracting_allowed_states(cond)

    @dataclass
    class FakeInstance:
        instance_state: InstanceState

    try:
        return [
            is_.name
            for is_ in InstanceState.objects.all()
            if cond.apply(None, FakeInstance(is_))
        ]
    except AttributeError:  # pragma: no cover
        return []
