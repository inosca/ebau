# INOSCA permissions module

## Background & history

The permissions module is intended to replace tons of custom code that is
called at various places, where access to data, or permissions to perform
certain actions, or availability of certain functions is decided.

The current code uses a bunch of trickery, and a Python function decorator
(`@permission_aware`) to do this, leading to complexity, as the permissions
do not only differ from role to role, but also across the cantons.

### Vocabulary

We use the following vocabulary in this document / spec - in the Inosca world,
some words may imply something specific, or may imply some broader term.
We also define some terms that are only used further down in the details of the
specification.

| Expression     | Description                                                    |
|----------------|----------------------------------------------------------------|
| Access level   | A named group of permissons. What users see / refer to         |
| ACL Entry      | DB entry that gives an "access level" to a defined set of users|
| Case           | Caluma representation of building request. 1:1 link to instance|
| Dossier        | Collection of data belonging to a specific building request    |
| Event          | Any significant state change etc Not specific to django signals|
| Group          | Links users with a service and a role                          |
| Instance       | Camac representation of building request. Has 1:1 link to case |
| Permission     | Specific permission (allowed to perform a specific operation)  |
| Role           | Defines functionality of a user in relation to a service       |
| Service        | A department or other governmental service.                    |
| User           | Represents an authenticated human or machine                   |


## New permissions system

Generally, we do not have programmatic rules for visibilities and permissions
anymore. Instead the new system uses explicit access-control lists (ACL).

Any access to a dossier, or a functionality within that dossier, is controlled by
an ACL entry. These are stored in the database and are the "source of truth"
that define what a user can or cannot do.

ACLs are created automatically during certain events, and may be added manually
as well, under certain restrictions.

### General rules and use cases

Each ACL refers to exactly one access level. Users may have multiple active ACLs,
depending on their relationship to services, or even explicit assignments.

The access level in turn defines a set of permissions that come with
it. Each permission may be subject to conditions as well (such as
dossier status).

Before going into further details, we need to consider *when* the
permissions module is involved. Generally, there are only a few distinct
situations:

* (A) Fetching a list of cases / dossiers
* (B) Fetching dossier-related data in global context (across multiple dossiers)
* (C) Fetching dossier-related data in in a dossier-specific context
* (D) Performing an operation on a single dossier

As soon as a user has an active ACL on a dossier, they may *see*
it in a list. This makes querying efficient and simple: There is no
specific "read" operation (A).

When data is read across multiple dossiers, the same filtering applies, followed
by any additional sub-filter rule. Note these filters cannot use the permissions
system and still use "rule-based access control" (B, C). This includes *listing
data* even within a single-dossier context: Otherwise, the filtering code would
need to *magically detect* how the instance is selected (could be filter,
any query parameter or anything else, depending on the code's author)
and use that to select the currently-applicable permissions)

Once a dossier is opened in detail, all relevant ACLs are loaded, cached, and
the resulting permissions are evaluated. Any operation may then query the set of
permissions to see whether it is "allowed" or not (D). An operation may be the
availability of a button, a navigation item, or define the success of an operation.

In other words, we get the following table of usable permission data:

| Operation             | Scope          | Available permission data |
|-----------------------|----------------|---------------------------|
| Listing dossiers (A)  | Global         | Roles                     |
| Listing any data (B)  | Global         | Roles                     |
| Listing any data (C)  | Single-Dossier | Roles                     |
| Writing data (D)      | Single-Dossier | Roles, Permissions        |
| Performing action (D) | Single-Dossier | Roles, Permissions        |
| Showing menu item (D) | Global         | Roles                     |
| Showing menu item (D) | Single-Dossier | Roles, Permissions        |


A collection of use cases is documented in [the Use Cases document](./docs/use-cases.md).

### Data Model

The idea of the new permissions system is to be as stateful as possible: Depending
on DB data instead of code to decide what permissions to apply.

See [Data model](./docs/data_model.md) for further discussion of the data model

### API

There is the REST API, as well as an internal Python API. Both can be
used to query and modify the ACLs and permissions.

| API Type    | Endpoint                   | Use cases                             |
|-------------|----------------------------|---------------------------------------|
| REST        | `/permission-acls`         | list, create ACL entries              |
| REST        | `/permission-acls/:id`     | Modify ACL entries                    |
| REST        | `/permission-info`         | list permissions for specific dossier |
| Python      | `get_permissions(instance)`| list permissions for specific dossier |
| Python      | `grant(...)`               | Create new ACL entry                  |
| Python      | `revoke(acl_entry)`        | Deactivate / expire an ACL entry      |


Further discussion regarding those APIs can be found in [the API document](./docs/api.md).

### Implementation details

Some further implementation details are discussed in [the details document](./docs/details.md)


### Testing

It is vital for the new subsystem to perform exactly as before: The same rules need to
apply, and the same users need to see the same data, and be able to perform the same
operations as before.

We need a good testing system in place which validates as much as possible of the available
REST API and other functionality to ensure noting is left "between the cracks".

Some thoughts about this are found [in the testing document](/django/camac/permissions/docs/validation-testing.md)


## Discusison points

### Open / Pending discussions

* Could the *Checking REST API* benefit from cache/expiry information as well, such
  that the frontend will know for how long a certain entry may be cached (even by using
  the corresponding HTTP headers, so frontend wouldn't even need to know)
* Could/should we extend the roles such that they also gain the ability to grant the
  same permissions as our "normal" permissions? That way, we could get rid of the
  "checking for permission / role" duality. This could be configured in the settings.py
  similar to how the "access levels" are configured.
* Configuration: It may make sense to combine permissions and dossier states such
  that we have a more compact configuration than a list of 1:1 pairings. Not sure
  which grouping would be most efficient at the moment though
* Testing: We need a way to verify that the migration, as well as the
  new permissions code corresponds to the old permissions code. We do
  not want to drop (or worse, create) any permissions or abilities that
  are in violation of the previous tested-and-true system.


### Expired / Past discussions / thoughts

* ~Could we use (and extend) Emeis as base for this? It already supports most of the
  operations we need, and is lacking only rather few of them~
  -> After further thinking about this: Emeis is too far off from what we're
     doing here, so won't be a good fit.
