# Permissions module - configuration

The configuration can be found in the module-specific settings
file under `(project-root)/django/camac/settings_permissions.py`.

There are two aspects of configuration you need to look into:
First, there are the **access level** configs. These
define, for each access level, which permissions are granted.
Remember, ACLs refer to access levels, not permissions directly.

For each access level, we have a list of permissions, and each permission
is conditional: Either depending on an instance's state, or it may be dynamic.

Second, the event handler defines when to grant and when to revoke ACLs.

## Permission naming schema

The permissions granted in the permission module are technically quite freestyle:
There is no requirement for a specific naming pattern.

However, to make things easy to understand, we define the
general permission naming pattern as follows: `(module)-(function)-(detail)`
whereas the `(detail)` is optional and module-specific.

For each module, there should be at least a `(module)-read` permission to
denote that a user may see the module. Further actions (such as access to
specific module data, or to perform certain actions) can be named freely. The
following example gives a few possible permission names; however these do not
neccessarily match what is available in the application.


## Instance resource permissions

The Camac instance resources have a field `require_permission`. If that field is
configured, then Camac (PHP) checks against the permission module to see if the
current user has the permission.

## Example configuration

```python
from camac.permissions.conditions import InstanceState
def toss_a_coin(instance):
    import random
    return random.choice([True, False])

PERMISSIONS = {
    "default": {},
    "demo": {
        "ACCESS_LEVELS": {
            "applicant": [
                # editing only in new and in "nachforderung"
                ("form-edit", InstanceState(["new", "nfd"])),
                # viewing is always allowed for applicants
                ("form-read", InstanceState(["*"])),
            ],
            "service": [
                # view form in submitted and "correcting" state
                ("form-read", InstanceState(["subm", "corr"])),

                # editing the form only in correction state
                ("form-edit", InstanceState(["corr"])),

                # Be lucky: Only allowed if a coin toss says so
                ("be-lucky", toss_a_coin)
            ]
        },
        # For details on the event handler, see below
        "EVENT_HANDLER": "camac.my_canton.permissions.PermissionEventHandler",
        "ENABLED": True,
        "PERMISSION_MODE": PERMISSION_MODE.OFF
    },
```

### Dynamic permissions

The permissions each have a condition attached, which is a callback, returning
True or False depending on whether the permission shall be granted.

In the example above, the `"be-lucky"` permission is granted based a random
event. For serious dynamic permissions, the interface is as such:

```python
def my_dynamic_permission(userinfo, instance):
    # instance is the affected instance
    # userinfo provides the following (all values are optional, keep that in mind!):
    #  - userinfo.user: the requesting user
    #  - userinfo.service: currently-active service of the requesting user
    #  - userinfo.role: currently-active role of the requesting user
    #  - userinfo.token: token for publicly-accessing users
    ...
```

If you don't need a parameter, you don't have to take it (see for example the
`toss_a_coin()` method above, it doesn't take the `userinfo` parameter)

There are a couple of predefined checks that you can use. They are fully
composable using the operators `&` (and), `|` (or) and `~` (negation). Some
examples:

```python
from camac.permissions.conditions import InstanceState, Always, HasRole
PERMISSIONS = {
    "default": {},
    "demo": {
        "ACCESS_LEVELS": {
            "special-service": [
                ("form-edit", InstanceState(["redacting"])),
                ("form-read", HasRole(["municipality"]) & InstanceState(["redacting"])),
                ("workitems-edit", HasRole(["municipality"]))
            ],
            ...
        }
    }
}
```

The currently available checks are:

* `InstanceState`: Require instance state to be one of the given instance state names
* `HasRole`: Require user to have one of a list of given roles
* `Always`: Will always grant the permission
* `Never`: Will never grant the permission. This may be useful for specifying exclusions


## Permission switcher

During the transition, where the permissions module is integrated all over the
place, we need a way to switch between old mode and new mode permissions:
Maybe we want the old (and tested) code in production, but want to have a log message
each time the new permission code does something different.

You can configure the permissions mode switcher as follows:

```python
from camac.permissions.conditions import InstanceState, Always, HasRole
from camac.permissions.switcher import PERMISSION_MODE
PERMISSIONS = {
    "demo": {
        "PERMISSION_MODE": PERMISSION_MODE.AUTO_ON,
        "ACCESS_LEVELS": {
            ...
        }
    }
}
```

The available permission modes are these:

* In `FULL` mode, the permissions switcher will *only* use the permissions
  module, the "traditional" permissions are not checked at all. This will
  be the default once the transition is complete and we are sure everything
  is correct.

* In `CHECKING` mode, both backends are checked, and any difference is treated as
  an error. This should be used during development of the transition.

* In `LOGGING` mode, the same thing happens as in `CHECKING`, but any difference
  is only logged as warning, but not treated as an error (so it won't trigger
  HTTP/500 errors, for example).

* In `OFF` mode, only the old permissions code is used. This can be used for
  production while parts of the transition are already merged, but not
  considered stable enough to activate. *This is the default!*

These are the "main modes". In addition, there are the following as well:

* `AUTO_ON`: Automatic **on** mode will be in `CHECKING` mode in the development
  environment, and in `LOGGING` mode in production (including CI, stage, test
  etc)
* `AUTO_OFF`: Automatic **off** mode is using `OFF` in production, stage, etc,
  and `LOGGING` in development mode.
* `CLEANUP_AFTER_MIGRATION`: Cleanup mode is used as a marker to find all call
  sites and remove the old code (as well as the switcher) once we are done with
  the migration.


## Permission event handlers

Each canton needs to implement it's own `PermissionEventHandler` subclass, and
implement the required methods to grant / revoke permissions as needed.

Note: The actual available event handlers are still work-in-progress, so take
the following as a *structural* example, not a blueprint for something that will
actually work. (The parameters passed to the handlers are as-documented however)

A simple handler may look like this:

```python
from camac.permissions import events

class ExamplePermissionEventHandler(events.PermissionEventHandler):

    # See below for explanation of the decision_dispatch_method
    @events.decision_dispatch_method
    def instance_post_state_transition(self, instance):
        return instance.instance_state.get_name().lower()

    @instance_post_state_transition.register("subm")
    def instance_submitted(self, instance):
        municipality = instance.fields.all().get(name="municipality").value
        # When submitted, grant responsible service / municipality
        # the "service" access level
        self.manager.grant(
            instance,
            grant_type="SERVICE",
            access_level="service",
            service=user_models.Service.objects.get(pk=municipality),
            event_name="instance-submitted",
        )

    @instance_post_state_transition.register("new")
    def instance_created(self, instance):
        # On creation, grant "applicant" permissions to the user
        self.manager.grant(
            instance,
            grant_type="USER",
            access_level="applicant",
            user=instance.user
        )

```

### Decision dispatch method

Often, you will need to run separate code depending on a certain situation.
For example, when an instance transitions from one state to the next,
you need to grant/revoke depending on the new state.

For this, you may use the `@decision_dispatch_method` decorator.

The decorated method is expected to return a string, identifying a "decision".
Then, there needs to be an implementation method registered for each possible
such decision.

Looking at the example above, the decorated method returns the instance state's name.

Then, there may be a number of methods, each reacting to a state transition
into a given state.

The event handler object has a property `manager`, which allows easy access to
granting/revoking permissions. When used in the context of an event handler, it
will also set the `created_by_event` / `revoked_by_event` accordingly.

### Extending event handlers

When the need arises to react to a new event, you should extend the
`permissions.events.Trigger` class and add a new `EventTrigger`
to it.

Then, you can call that trigger from the code:

```python
from camac.permissions import events as permission_events
# ...
permissions_events.Trigger.your_new_event(
    request, instance
)
```

The events code automatically validates the configured event handlers
and ensures that all possible events are implemented.
