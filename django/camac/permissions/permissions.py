"""Constants and utilities for referencing permissions."""

GRANT_ANY = "permission-grant-any"
REVOKE_ANY = "permission-revoke-any"
LIST_ANY = "permission-read-any"


def READ_SPECIFIC(name):  # pragma: no cover
    return f"permission-read-{name}"


def GRANT_SPECIFIC(name):  # pragma: no cover
    return f"permission-grant-{name}"


def REVOKE_SPECIFIC(name):  # pragma: no cover
    return f"permission-revoke-{name}"
