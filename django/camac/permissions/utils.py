from dataclasses import dataclass
from typing import List

from camac.instance.models import InstanceState
from camac.permissions.conditions import RequireInstanceState


def extract_allowed_states(cond: RequireInstanceState) -> List[str]:
    """List all instance states (untranslated names) that the condition allows.

    Note: This really only works with `RequireInstanceState` conditions
    as well as combinations (&, |, ~) of them.
    """

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
