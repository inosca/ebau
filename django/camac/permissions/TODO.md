# TODO - next steps

## Phase 2:

* [x] Permission switching / comparison
* [x] Migration tooling
  - [x] Applicants
  - [x] (Lead) municipalities
  - [x] Services
      - map from (sent) inquiries

* [ ] Convert access role-by-role
  - [x] Applicants
  - [x] (Lead) municipalities
  - [x] Services
      - inquiry sent

* Validation and testing
  - Migration tooling: ensure events and migration tool generate the same
    instance acls in the same states/events
* Specification update: Design / Purpose:
  Currently, in addition to the permission module's view, many modules have custom
  rules to decide whether a functionality is available or not. The long-term
  goal should be to get rid of all these custom rules and make these decisions
  in the permissions module. This extends the scope of the module by querying
  business logic state, but it reduced the complexity of the entire code base,
  as one will now only need to look in one place, not many (permissions module,
  backend code, frontend code, ...)
