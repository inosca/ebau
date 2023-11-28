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
def toss_a_coin(instance):
    import random
    return random.choice([True, False])

PERMISSIONS = {
    "default": {},
    "demo": {
        "ACCESS_LEVELS": {
            "applicant": [
                # editing only in new and in "nachforderung"
                ("form-edit", "new"),
                ("form-edit", "nfd"),

                # viewing is always allowed for applicants
                ("form-read", "*"),
            ],
            "service": [
                # view form in submitted state
                ("form-read", "subm"),

                # editing and viewing the form in correction state
                ("form-edit", "corr"),
                ("form-read", "corr"),

                # Be lucky: Only allowed if a coin toss says so 
                ("be-lucky", toss_a_coin)
            ]
        },
        # For details on the event handler, see below
        "EVENT_HANDLER": "camac.my_canton.permissions.PermissionEventHandler",
        "ENABLED": True,
    },
```

## Permission event handlers

Each canton needs to implement it's own `PermissionEventHandler` subclass, and
implement the required methods to grant / revoke permissions as needed.

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
