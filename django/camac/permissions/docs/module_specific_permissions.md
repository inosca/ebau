# Permissions module - Module-specific implementation

There are some modules where the rules are too complex to map them all in the
global permission module. One reason is that some permissions are dependent on
more fine-grained context that isn't always available.

For such cases, the module can be used to build a module-specific permission
system.

This is a how-to guide to getting a module-specific permission system
implemented.

> [!note]
> If your module-specific permission system does not need any additional context
> and all your permissions can be derived directly from the building permit
> (instance) itself, it's probably better to define your permissions entirely in
> the main permissions module.


## Understanding the structure

The general permissions module works by defining, a set of permissions for
each [access level](data_model.md). Each such permission can be "gated" with
condition to define when a user should actually have it.

The internal API goes through a permission manager, which you instantiate with
some information about *who the user is*. To query the permissions the user
has, you pass in an instance (building permit) as context. There are a few
convenience methods, like `has_any()`, `has_all()`, `require_any()`,
`get_permissions()` and so on.

## Setting up 

Building a module-specific permissions system involves the following steps. Each
of them will be explained in detail further down.

* Build a **permission context** class that contains the required information.
  This must be a subclass of the `PermissionContext` defined in the
  `camac.permissions.api` module. It can contain additional context that is
  then passed on to the permission checks / conditions (see below).

* Implement a custom **permission manager** to define the API. This must be a
  subclass of the `PermissionManager` class defined in the `camac.permissions.api`
  module.

* Define the custom **permissions settings** for your module. Here, you will
  also define custom permission conditions that take advantage of the extended
  context.


### Context and permission manager

To define the API to our customized permissions system, we'll need two new
classes. It is highly recommended that these are defined in the module
`camac.mymodule.permissions`, but there is no strict requirement to do so.

The first dataclass we need defines the context. This contains anything about
the *subject* of the permissions we will need to check. For example in the documents
/ alexandria module, this would be a document model (in addition to the instance,
which is needed for the base permissions module):

> [!note]
> If you don't have any context to add besides the instance, it's very likely
> that you should just define any permissions for your module in the main
> permissions module instead -- there is no use in a specialized implementation
> in that case.


```python
from dataclasses import dataclass
from django.conf import settings

from camac.permissions.api import PermissionManager
from camac.permissions.conditions import PermissionContext


@dataclass
class MyPermissionContext(PermissionContext):
    foo: FooModel

    # you can use the full dataclass infrastructure, for example
    # __post_init__(), to define additional, useful attributes so the
    # check classes won't need to do too much work, or so the meaning
    # can become clearer.

    def as_cache_key(self) -> str:
        """Return a string that can be used to cache permissions data."""
        return str(self.foo.pk)


class AlexandriaPermissionManager(PermissionManager):
    def __init__(self, userinfo, permission_settings=None):
        # This needs to be customized such that the custom permissions
        # settings are passed on. See below for details
        super().__init__(
            userinfo,
            permission_settings or settings.PERMISSIONS_ALEXANDRIA,
        )

    def scoped_for(self, ...) -> PermissionScope:
        """Scope manager to a given object.

        Implement this to gain short-cut access that can simplify accessing
        the permissions API in your module.
        """

        return super().scoped_for(
            MyPermissionContext(...)
        )
```

The `scoped_for()` method should be used as a quick access, so the call sites
don't need to instantiate the permimssion context themselves, then pass it to
the permissions manager.

### Settings

To define our custom permisisons, along with any custom conditions, we'll
define a new settings module. This can be done in two steps:

First, define the settings via the `load_settings_module()` function in the
django settings module:

```python
# In settings/django.py
PERMISSIONS_MYMODULE = load_module_settings("permissions.mymodule")
```

Following this, we create our new module with our settings, as follows:

```python
# camac/settings/modules/permissions/mymodule.py

from camac.permissions.conditions import Check

class SomeCondition(Check):
    def apply(self, context: MyPermissionContext) -> bool
        # check the context for the condition as needed
        if context.has_required_property:
            return True
        return False

class SomeOtherCondition(Check):
    def apply(self, context):
        ...

PERMISSIONS_ALEXANDRIA = {
    "default": {},
    "kt_bern": {
        "ENABLED": True,
        "ACCESS_LEVELS": {
            "geometer": [
                ("context-a": SomeCondition()),
                ("context-b": SomeOtherCondition()),
                ...
            ]
        }
    }
}
```

As you can see, the structure is exactly the same as any other module-specific
settings, and corresponds in semantics exactly the main permissions module.


## Separation of concerns

Also note that the "core" permissions module and any module-specific
implementations do not, by design, talk to each other: Any call site that
requires a module-specific permission should call the local permission
manager, and if a permission from the global permissions module is needed, that
permissions manager must be called as well.

The reason for this is that this allows local permission labels to be used, and
we don't need to fear that another module will define (perhaps in the global
space) the same permission for another purpose.
