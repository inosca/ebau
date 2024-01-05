# Permissions module - APIs

## Internal API

The internal API consists of a few simple parts:

* The filtering mechanism
* Permissions checking and listing
* Granting and revoking
* Reacting to events in the system (for granting and revoking)

The filtering mechanism allows filtering of any queryset that belongs to
a dossier (either directly, or indirectly). It will return a filtered queryset
that only contains dossiers where the user has at least one active ACL.

The permissions checking/listing API allows code to query whether a
user is allowed to perform any given operation (identified by a slug)
in the context of a dossier.

Some permissions may also depend on a user's *role*, and not on the
explicitly-granted permissions.

Note that the checking API explicitly only exposes checking for permissions, not
for access levels / ACLs directly.

The low-level internal API supports the use cases as follows:

To avoid big argument lists, everything is done via a permission manager
object. This encapsulates the lower details, so you do not have to pass
tons of arguments.

### Filtering querysets

```python
from camac.permissions import api as permissions_api

# context of a viewset for example
def get_queryset(self):
    qs = super().get_queryset()
    manager = permissions_api.PermissionManager.from_request(self.context['request'])
    return manager.filter_queryset(
        qs,
        # Pass instance prefix, so the query can be filtered corectly.
        instance_prefix='instance',
    )

```

### Checking permissions

```python
# in the context of an operation
@action(...)
def do_stuff(self, request):
    instance = self.get_object().instance
    manager = permissions_api.PermissionManager.from_request(request)

    if 'do-stuff' not in manager.get_permissions(instance):
        raise Error("You are not allowed to do stuff")

```

### Granting and revoking permissions

```python
# during a "significant" event that updates permissions..
def deal_with_some_event(request, ...):
    manager = permissions_api.PermissionManager.from_request(request)

    # permission starts *now* and has no end date..
    manager.grant(
        instance=some_instance,
        grant_type='SERVICE',
        service=some_service,
        access_level='leitbehoerde'
    )

    # permission starts *now* until the end of 2023
    manager.grant(
        instance=some_instance,
        grant_type='AUTHENTICATED_PUBLIC',
        access_type='auflage',
        until='2024-01-01T00:00:00Z'
    )

    # Revoke some access *now*.
    manager.revoke(acl=the_acl_in_question)
```

### Events API

Ideally, most of the permission granting and revoking code is triggered
via the Events API. This is a way to configure granting and revoking ACLs
when certain events happen in Camac.

See [configuration](configuration.md) to see how to configure the module.

Each canton needs to implement it's own `PermissionEventHandler` subclass, and
implement the required methods to grant / revoke permissions as needed.

A simple handler may look like this:

```python
from camac.permissions import events

class ExamplePermissionEventHandler(events.PermissionEventHandler):
    def instance_post_state_transition(self, instance):
        new_state = instance.instance_state.get_name().lower()
        if new_state == 'subm':
            municipality = instance.fields.all().get(name="municipality").value
            self.manager.grant(
                instance,
                grant_type="SERVICE",
                access_level="service",
                service=user_models.Service.objects.get(pk=municipality),
            )
```


## REST API

The regular REST representation of the ACL entries is available under
`/instance-acls` and works just as any other REST endpoint. It
represents the data model as defined in [the models document](./data_model.md).

The same rules apply for allowing users to read and  modify the ACL entries;
they are governed by (yet-to-be-defined) permission rules.

In addition to this, there is a representation of all permissions a user has on
any given instance. This is a short-hand for the frontend to fetch the actually
available permissions for each specific dossier ("instance"). The endpoint
requires a filter that accepts multiple instance identifiers - allowing the
frontend to fetch permissions already on a list view. It lives at `/instance-
permissions` and accepts the same filters as the main instances endpoint (`/
instances`) takes. It will only list instances the user has some (active) ACLs on.

This works similarly as the `prefetch_related` mechanism in Django, but due to
the fact that we have dynamic permissions, we cannot use a purely django-based
approach, without adding serializer method fields all over the place.
