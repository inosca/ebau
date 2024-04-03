"""Constants and utilities for referencing permissions."""

GRANT_ANY = "permissions-grant-any"
REVOKE_ANY = "permissions-revoke-any"
LIST_ANY = "permissions-read-any"


def READ_SPECIFIC(name):  # pragma: no cover
    return f"permissions-read-{name}"


def GRANT_SPECIFIC(name):  # pragma: no cover
    return f"permissions-grant-{name}"


def REVOKE_SPECIFIC(name):  # pragma: no cover
    return f"permissions-revoke-{name}"
