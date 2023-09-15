# Permissions module - APIs

## Internal API

The internal API consists of a few simple parts:

* The filtering mechanism
* Permissions checking and listing

The filtering mechanism allows filtering of any queryset that belongs to
a dossier (either directly, or indirectly). It will return a filtered queryset
that only contains dossiers where the user has at least one active ACL.

The permissions checking/listing API allows code to query whether a
user is allowed to perform any given operation (identified by a slug)
in the context of a dossier.

Some permissions may also depend on a user's *role*, and not on the
explicitly-granted permissions.

Note that the API explicitly only exposes checking for permissions, not for
access levels / ACLs directly.

A rough outline of the API could look like this:

```python

from ... import permissions

# context of a viewset for example
def get_queryset(self):
    qs = super().get_queryset()
    return permissions.filter_queryset(qs, user=self.context.user)


# in the context of an operation
@action(...)
def do_stuff(self, request):
    case = self.get_object().case
    if 'do-stuff' not in permissions.get_permissions(case=case, user=request.user):
        raise Error("You are not allowed to do stuff")

# alternative, if no control over error condition is required
@action(...)
def do_more_stuff(self, request):
    case = self.get_object().case
    permissions.enforce_permission(
        case=case,
        user=request.user,
        operation='do-more-stuff')



# during a "significant" event that updates permissions..
def handle_event(..):
    # permission starts *now* and has no end date..
    permissions.grant(case=case, service=some_service, access=access_level_foo)

    # permission starts *now* until the end of 2023
    permissions.grant(case=case, service=some_service, access=access_level_foo,
        until='2024-01-01T00:00:00Z'
    )

    # Revoke some access *now*.
    # Note this means users in this service may still have access to the
    # case via some other ACL - it does not remove all access, just access granted
    # via the specific ACL
    permissions.revoke(case=case, service=some_service, access=access_level_foo)
```


## REST API

The regular REST representation of the ACL entries is available under `/permission-acls`
and works just as any other REST endpoint. It represents the data model as defined
in [the models document](./data_model.md).

The same rules apply for allowing users to read and  modify the ACL entries;
they are governed by (to-be-defined) permission rules.

In addition to this, there is a representation of all permissions a user has on any
given instance. This is a short-hand for the frontend to fetch the actually available
permissions for each specific dossier ("instance"). The endpoint requires a filter
that accepts multiple instance identifiers - allowing the frontend to fetch permissions
already on a list view.

This works similarly as the `prefetch_related` mechanism in Django, but due to the fact
that we have dynamic permissions, we cannot use a purely django-based approach, without
adding serializer method fields all over the place.
