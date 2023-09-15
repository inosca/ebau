### Data Model

The `InstanceACL` DB model is the base of the new permissions
system. This is where we store the actual access of any user to a
dossier. Since any part of a dossier is linked either directly or
indirectly to a Camac instance, this is our "anchoring point".

An ACL gives permission to a user to (at least) list an instance. Any further
permission is then defined via the configuration of the access level given
using the ACL.


```
           +----------------+ 1         +---------------------+
           | Instance       |-----------| InstanceACL         |
           +----------------+      0..* | - start_time        |
                                        | - end_time          |
           0..1 +-----------+      0..* | - created_by_user   |
      ,---------| Service   |-----------| - revoked_by_user   |
      |         +-----------+ 0..1      | - created_by_event  |
      |                                 | - revoked_by_event  |
      |                                 | - created_by_group  |
      |                                 | - revoked_by_group  |
      |                                 | - grant_type        |
      |                                 | - token             |
      | 0..*                            | - created_at        |
  +--------+   0..* +-------+      0..* | - revoked_at        |
  | Group  |--------| User  |-----------| - metainfo          |
  +--------+ 0..*   +-------+ 0..1      +---------------------+
 0..* |                                          | 0..*
      | 1                                        |
  +--------+     +----------------------+        |
  | Role   |     | AccessLevel          |--------`
  +--------+     | - label              | 1
                 | - require_grant_type |
                 +----------------------+                       ^
                      0..* |                                    | Database
  ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~|~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~ ~
                           |                                    | Configuration
                           |                                    v (settings.py)
                           |         +------------------+
                           `---------| Permission       |
                                1..* | - identifier     |
                                     | - dossier_state  |
                                     | - check_callback |
                                     +------------------+
```

#### Functional attributes

An ACL is considered active under the exact conditions: `start_time` is in the
past, `end_time` is either in the future or `NULL`. This allows for Instance
ACLs to never be deleted. A revocation happens by setting the `end_time` to a
specific time.

Users may either be assigned directly to the ACL, or indirectly via a service
(also see below for ACL types). When assigned via service, the connection is
only considered active if a matching `X-Camac-Group` header is present.

`InstanceACL`s can be of different types, denoted in the `grant_type`
field. Grant types can be either `service`, `user`, `authenticated-public`,
`anonymous-public`, or `token`.

This is done explicitly instead of implicitly for clarity,
even if it could also be done implicitly, by applying certain rules (for
example if it's `service`, a service must be assigned, if it's `user`,
a user must be assigned, if it's public, then all these references must be
`NULL` etc). Making it explicit allows further validation, and accidental
grant to public (by failing to correctly set user or service or token)
becomes more difficult.

Access levels may require a specific grant type: You for example would
not want to be able to (accidentally or willingly) assign "municipality"
access to "anonymous-public" users.


#### Tracking attributes

There are quite a few "tracking" attributes, to analyze why someone
has a permission: For manual permissions, the `created_by_user` /
`revoked_by_user` are used so we know who did the corresponding operation.
For automatic permissions, we use `created_by_event` / `revoked_by_event`
along with the corresponding user (if known).


### Configuration

`AccessLevel`s are global, per-canton entities. They are identified by a slug,
which in turn is referenced in the configuration.

The configuration consists of a table, as follows:

```python
from my_canton.permissions import custom_checks
APPLICATIONS = {
    "my-canton": {
        ...
        "PERMISSIONS": {
            'applicant': [
                # applicant can edit the form (caluma) in "new" and "rejected" states
                ('form', 'new'),
                ('form', 'rejected'),
                # documents can be added in new, rejected, and subsequent requests
                ('document', 'new'),
                ('document', 'rejected'),
                ('document', 'nfd'),
            ],
            'municipality': [
                # Municipality only has access to document category 'foo' under
                # programmable conditions
                ('document-category-foo', custom_checks.has_access_to_foo_docs),
            ]
        }
    }
}
```

A permission has *either* a dossier state, which must match (but may be `*`
to represent any state), or a `check_callback`. The callback will return `True`
or `False` depending on what the function determines - this is how we can
implement complex permissions.

A permission is identified by a *slug*. They are not validated or checked, so
that any code may request it's own domain-specific permission. This way,
further down-the-line permissions/visibilities can be implemented, by querying
possibly canton-specific permissions.

In the configuration, we put `dossier_state` and `check_callback` into
a 2-tuple as callables and (string) states can be easily told apart.


