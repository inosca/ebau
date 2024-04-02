# TODO - next steps

## Phase 2:

* [x] Permission switching / comparison
* [ ] Migration tooling
  - [x] Applicants
  - [x] (Lead) municipalities
  - [ ] Services
      - map from (sent) inquiries

* [ ] Convert access role-by-role
  - [x] Applicants
  - [x] (Lead) municipalities
  - [ ] Services
      - inquiry sent


## Phase 1

* [x] Backend: Configuration "new style" - ask Jimmy
* [x] Backend: Permissions for permissions module (to allow manual grants)
  -> Use "old way" to check for LB, until LB is migrated
  -> I'm LB IF: `instance.responsible_service(...) == request.group.service`
* [x] Includes: InstanceACL -> Instance and -> User
* [x]  MERGE in `master`
* [x] Geometer access:
  - instance queryset mixin: has new role. `_for_geometer()` will directly
    call new permission module, no fallback
  - Define events and event handlers to grant/revoke permissions as needed
    -> spec in offer for kt bern "geometer" feature
  - Note: Geometers won't receive automatic access to existing instances, no
    migration required
* [x] MERGE in `master`
* [x] InstanceResource API: Query permissions module in addition
* [x] Modify PHP code to use InstanceResource API instead of direct DB access
  * Figure out special cases in PHP code


## Further TODOs - before merge into base branch

* [x] merge migrations
* [x] [created|revoked]_by_service resource related fields in API, not just models (incl includes)
* [x] s/Service/Municipality/ in the tests and the `@permission_aware` methods
* [x] InstanceACLViewset.get_queryset() needs to be `@permission_aware`
      to only show ACLs to `Municipality` users (not all service users).
      all other users must get `qs.none()`
* [x] InstancePermissionViewset: Should probably not include the instances - caller
      should already have them, and include_serializer might circumvent the visibilities

Future TODO:

* [x] access levels: attributes for marking them "user-assignable" or "system-assignable"
      -> metainfo?
      -> who may grant which access levels? -> DGAP?
      done by the permissions system itself (user requires
      permissions-add-foobar or permissions-add-any to grant ACL)
