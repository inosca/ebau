from typing import Callable, Dict, List, Tuple, TypedDict, Union

"""
Configuration for the permissions module.

Note: Full documentation for the configuration can be found here:

  -> ./permissions/docs/configuration.md

We provide type hints here. They should help your IDE with completion
and checks, and also serve as a documentation on what's allowed.
"""

# Actually Instance -> bool, but we can't import instance here
# so this is a slight inaccuracy
PermissionCallback = Callable[[object], bool]
PermissionCallback.__doc__ = """
With a Camac Instance, decide whether user has permission.

The callback takes a Camac instance object, and dynamically
decides whether the user may have the permission in question.

This can be used for more complex decisions, if the condition
is more than the instance's state.
"""

# (permission, condition)
PermissionLine = Tuple[str, Union[str, PermissionCallback]]
PermissionLine.__doc__ = """
A tuple that maps a given permission (str) to a condition.

The condition may be either a string, in which case it refers
to an instance state's name, or "*" if the permission shall
be granted in all instance states.
Alternatively, it may be a callback to dynamically make
the decision.
"""

PermissionConfigEntry = TypedDict(
    "PermissionConfigEntry",
    {
        "ENABLED": bool,
        "EVENT_HANDLER": str,
        # each access level entry here must refer to an existing
        # access level model.
        "ACCESS_LEVELS": Dict[str, List[PermissionLine]],
    },
)

PermissionsConfig = Dict[str, PermissionConfigEntry]


PERMISSIONS: PermissionsConfig = {
    "default": {},
    "demo": {
        "ACCESS_LEVELS": {
            "service": [
                # (permission, instance-state or "*" for any)
                # (permission, (lambda instance -> True/False))
                ("foo", "*"),
                ("edit-form", "new"),
            ]
        },
        "EVENT_HANDLER": "camac.permissions.events.EmptyEventHandler",
        "ENABLED": True,
    },
}
