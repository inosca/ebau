"""Permission module mode switching utilities.

During the transition, where the permissions module is integrated all over the
place, we need a way to switch between old mode and new mode permissions.

This module provides the instruments to do so. Depending on the settings
(See PERMISSION_MODE in `camac.settings.modules.permissions`), we can run in
different modes. From fully enabled, to fully disabled, and some modes in-between
that are useful for checking / validation of the permissions code.

See the docs for a full explanation of the modes (or the enum below for a very
short hint regarding the behaviour).
"""

from enum import Enum
from logging import getLogger

from django.conf import settings

log = getLogger(__name__)


class PERMISSION_MODE(Enum):
    """Permissions modes."""

    # Full on = old permission code is not used anymore
    FULL = "FULL"
    # Checking runs both old and new code, raises an exception on difference
    CHECKING = "CHECKING"
    # Logging is equal to checking, but only a warning is logged instead of
    # raising an exception
    LOGGING = "LOGGING"
    # Off mode means only the old permission code is run
    OFF = "OFF"
    # Cleanup mode is used as a marker to find all call sites and remove
    # the old code (as well as the switcher) once we are done with the migration
    CLEANUP_AFTER_MIGRATION = "CLEANUP_AFTER_MIGRATION"

    # Auto on mode uses "checking" mode in dev env, but logging mode in production
    AUTO_ON = "AUTO_ON"
    # Auto off mode uses logging mode in dev, but "off" in production.
    AUTO_OFF = "AUTO_OFF"


def get_permission_mode():
    if not settings.PERMISSIONS:  # pragma: no cover
        # Cantons that don't have the permissions module activated at all won't
        # even have the setting
        return PERMISSION_MODE.OFF
    set_mode = (
        settings.PERMISSIONS.get("PERMISSION_MODE", PERMISSION_MODE.OFF)
        or PERMISSION_MODE.OFF
    )
    if set_mode == PERMISSION_MODE.AUTO_ON:
        return (
            PERMISSION_MODE.LOGGING
            if settings.ENV == "production"
            else PERMISSION_MODE.CHECKING
        )
    elif set_mode == PERMISSION_MODE.AUTO_OFF:  # pragma: no cover
        # no cover, because we want to test either *both* or *new* mode,
        # "OFF" mode does less than AUTO_ON or CHECKING, so we don't
        # lose anything here
        return (
            PERMISSION_MODE.OFF
            if settings.ENV == "production"
            else PERMISSION_MODE.LOGGING
        )
    else:
        return set_mode


class PermissionMethod:
    def __init__(self, old_method=None, new_method=None):
        self._old_method = old_method
        self._new_method = new_method
        self._name = None
        self._owner = None

    class BoundPermissionMethod:
        def __init__(self, method, instance):
            self._method = method
            self._instance = instance

        def __call__(self, *args, **kwargs):
            assert self._method._new_method, f"{self}: new method not registered yet!"
            assert self._method._old_method, f"{self}: old method not registered yet!"

            mode = get_permission_mode()
            if mode == PERMISSION_MODE.FULL:
                # Only "new"
                return self._method._new_method(self._instance, *args, **kwargs)
            elif mode == PERMISSION_MODE.OFF:
                # Only "old"
                return self._method._old_method(self._instance, *args, **kwargs)
            else:
                old = self._method._old_method(self._instance, *args, **kwargs)
                new = self._method._new_method(self._instance, *args, **kwargs)
                # TODO: we'll likely have to be a bit more creative with the
                # comparison here: We need to investigate QS equality checks for
                # example (different query, same result should be acceptable)
                if old == new:
                    return old
                elif mode == PERMISSION_MODE.CHECKING:
                    raise RuntimeError(
                        f"Permissions module discrepancy in `{self}`: OLD "
                        f"says {old}, NEW says {new}"
                    )
                elif mode == PERMISSION_MODE.LOGGING:
                    log.error(
                        f"Permissions module discrepancy in `{self}`: OLD "
                        f"says {old}, NEW says {new}. Returning NEW"
                    )
                    return new

        def __str__(self):
            return str(self._method)

    def _error_method(self, name):
        def _err(*args, **kwargs):
            raise RuntimeError(
                f"`{self._owner}.{name}` is a permission switcher method. "
                f"Call `{self}` instead"
            )

        return _err

    def __set_name__(self, owner, name):
        self._name = name
        self._owner = owner.__name__

    def register_old(self, fn):
        self._old_method = fn
        if (
            get_permission_mode() == PERMISSION_MODE.CLEANUP_AFTER_MIGRATION
        ):  # pragma: no cover
            raise DeprecationWarning(
                f"You can delete {fn.__name__} from {self._owner} now, remove "
                f"the `permission_switching_method.register_new` "
                f"decorator from {self._new_method.__name__} "
                f"and rename it to {self}"
            )

        return self._error_method(fn.__name__)

    def register_new(self, fn):
        self._new_method = fn
        return self._error_method(fn.__name__)

    def __str__(self):
        return f"{self._owner}.{self._name}"

    def __get__(self, inst, inst_type):
        return PermissionMethod.BoundPermissionMethod(self, inst)


def permission_switching_method(new_method=None, old_method=None):
    """Create a new permission method.

    Permission methods can switch between RBAC and Permission Module modes
    depending on the configuration.

    You can use it in two ways:

    >>> class Foo:
    ...     # Register both variants explicitly
    ...     do_thing = permisson_method()
    ...     @do_thing.register_old
    ...     def do_thing_old(self):
    ...         ...
    ...     @do_thing.register_new
    ...     def do_thing_new(self):
    ...         ...

    >>> class Bar:
    ...     # Register the "new" method directly as a decorator
    ...     @permisson_method
    ...     def do_thing(self):
    ...         ...
    ...     @do_thing.register_old
    ...     def do_thing_old(self):
    ...         ...
    """
    method = PermissionMethod(old_method, new_method)
    return method
