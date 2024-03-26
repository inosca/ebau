from collections import defaultdict
from dataclasses import dataclass
from typing import List

import pytest
from django.conf import settings

from camac.instance.models import InstanceState
from camac.permissions.conditions import Check, RequireInstanceState


@pytest.mark.xfail(
    reason=(
        "Complaining about all the duplicate configs, but "
        "this is not an actual problem"
    )
)
def test_duplicate_conditionals(db, any_application):
    seen_checks = defaultdict(list)
    seen_perms = defaultdict(list)

    access_levels = settings.PERMISSIONS.get("ACCESS_LEVELS", {})
    for access_level, permissions in access_levels.items():
        for perm, check in permissions:
            key = ",".join(sorted((_extract_allowed_states(check))))

            seen_perms[key].append(f"{access_level} / {perm}")
            seen_checks[key].append(check)

    for key, checks in seen_checks.items():
        if len(checks) <= 2:
            # no dupes here
            continue

        perms = seen_perms[key]
        perms_and_checks = zip(perms, checks)

        # Ok, we have multiple checks. Verify if they are actually the
        # same or just equal
        first_check = checks[0]
        first_perm = perms[0]
        errors = []
        for perm, check in perms_and_checks:
            # TODO: consider only reporting error if duplication count is
            # over a certain number
            if check is not first_check:  # pragma: no cover
                # Same check, different object instance
                errors.append(
                    f"Permission {perm} is equal to {first_perm}, but "
                    "is separate expression. Could be refactored"
                )

        assert errors == []


def test_conditional_types(db, any_application):
    """Ensure all permisison conditionals are of the correct type."""
    seen_checks = defaultdict(list)
    seen_perms = defaultdict(list)

    access_levels = settings.PERMISSIONS.get("ACCESS_LEVELS", {})

    for access_level, permissions in access_levels.items():
        for perm, check in permissions:
            key = ",".join(sorted((_extract_allowed_states(check))))

            seen_perms[key].append(f"{access_level} / {perm}")
            seen_checks[key].append(check)

    for key, checks in seen_checks.items():
        if len(checks) <= 2:
            # no dupes here
            continue

        perms = seen_perms[key]
        perms_and_checks = zip(perms, checks)

        for perm, check in perms_and_checks:
            assert isinstance(check, Check), (
                f"{perm} conditional {check} must be Check instance. "
                "Callbacks and raw string permission (state) conditionals "
                "are not allowed anymore"
            )


def _extract_allowed_states(cond: RequireInstanceState) -> List[str]:
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
