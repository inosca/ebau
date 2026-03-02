from collections import defaultdict

import pytest

from camac.permissions.conditions import Check
from camac.permissions.utils import IncompatibleCheck, extract_allowed_states


@pytest.mark.xfail(
    reason=(
        "Complaining about all the duplicate configs, but this is not an actual problem"
    )
)
def test_duplicate_conditionals(db, try_get_fixture, any_application):
    seen_checks = defaultdict(list)
    seen_perms = defaultdict(list)

    permissions_settings = try_get_fixture(
        f"{any_application['SHORT_NAME']}_permissions_settings"
    )
    if not permissions_settings:
        # "test" Canton - skip
        assert any_application["SHORT_NAME"] == "test"
        return

    access_levels = permissions_settings.get("ACCESS_LEVELS", {})
    for access_level, permissions in access_levels.items():
        for perm, check in permissions:
            try:
                key = ",".join(sorted((extract_allowed_states(check))))
            except IncompatibleCheck:
                # not plain combination of instance state checks
                key = repr(check)

            seen_perms[key].append(f"{access_level} / {perm}")
            seen_checks[key].append(check)

    for key, checks in seen_checks.items():
        if len(checks) <= 2:  # pragma: no cover
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


def test_conditional_types(db, try_get_fixture, any_application):
    """Ensure all permisison conditionals are of the correct type."""

    permissions_settings = try_get_fixture(
        f"{any_application['SHORT_NAME']}_permissions_settings"
    )
    if not permissions_settings:
        # this is the "test" canton, and there's no config to test
        # there. All others have permissions settings
        assert any_application["SHORT_NAME"] == "test"
        return

    access_levels = permissions_settings.get("ACCESS_LEVELS", {})

    for access_level, permissions_settings in access_levels.items():
        for perm, check in permissions_settings:
            assert isinstance(check, Check), (
                f"{perm} conditional {check} must be Check instance. "
                "Callbacks and raw string permission (state) conditionals "
                "are not allowed anymore"
            )
