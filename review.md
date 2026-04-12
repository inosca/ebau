# Code Review: `so_156_gis_links` Branch

**Branch:** `so_156_gis_links` vs `master`  
**Scope:** 120 files changed, ~14,200 lines added across Elixir backend, Ember frontend, nginx proxy, CI pipeline, Docker Compose  
**Date:** 2026-04-12  
**Commits reviewed:** 42 (from `8beb8bd6ad` through `6229025982`)

---

## Executive Summary

This is a large, foundational branch that introduces:

1. **GIS links feature** -- service-scoped URL template management (CRUD + coordinate resolution)
2. **Core Ash infrastructure** -- Actor struct, permissions, Caluma integration, master data DSL
3. **Auth layer** -- Keycloak bearer token verification, user/group/service resolution
4. **Ember frontend** -- GIS links UI under service-permissions
5. **CI/DevOps** -- GitLab Pages for docs, legacy schema bootstrap, config loading

The overall architecture is sound. The Ash resource design, Spark DSL extensions, and testing philosophy are well above average. However, the review found **7 critical issues** (runtime crashes, security gaps), **21 important issues**, and numerous minor items that should be addressed before merge.

**Verdict: Not ready to merge -- requires fixes for critical and important issues.**

---

## Critical Issues (Must Fix)

### C1. Ember template references non-existent `this.edit` task -- runtime crash

**File:** `ember-ebau-core/addon/templates/service-permissions/gis-links.hbs:72`

```hbs
{{on "click" (perform this.edit row)}}
```

The controller (`gis-links.js`) defines `save`, `delete`, and `updateSearch` tasks but no `edit` task. Clicking the pencil icon will throw a runtime error. Additionally, the backend has no `update` action for GIS links (see I1), so even if the task existed, it would have no endpoint to call.

**Fix:** Either (a) remove the edit button entirely if edit is not in scope, or (b) implement the edit task in the controller AND add an `update` action + PATCH route on the backend.

---

### C2. Controller class name is wrong -- copy-paste from static-keywords

**File:** `ember-ebau-core/addon/controllers/service-permissions/gis-links.js:11`

```js
export default class ServicePermissionsStaticKeywordsController extends Controller {
```

Should be `ServicePermissionsGisLinksController`. Ember resolves by file path, so this doesn't crash, but it's misleading for debugging and violates naming conventions. The `delete` task parameter is also named `staticKeyword` (line 76) instead of `gisLink`.

---

### C3. Silent auth failure -- fail-open pattern allows unauthenticated API access

**File:** `elixir-ebau/lib/ebau_web/plugs/keycloak_bearer_auth.ex:25-28`

```elixir
else
  _ ->
    conn
end
```

When authentication fails (missing header, invalid token, user not found, group not found), the plug silently passes `conn` through without an actor. The request reaches AshJsonApi with `actor: nil`. Whether this is denied depends entirely on every Ash resource having correct policies. This is a **fail-open** pattern. Combined with C4, this creates a real security gap.

**Fix:** Either halt with 401 in the `else` branch, or add a "require actor" plug after `KeycloakBearerAuth` in the `:api` pipeline.

---

### C4. Multiple resources lack authorizers -- open CRUD with no policies

**Files:**
- `elixir-ebau/lib/ebau/user/role.ex` -- `defaults [:read, :destroy, update: :*, create: :*]`, no authorizers
- `elixir-ebau/lib/ebau/user/service_group.ex` -- `defaults [:read, :create, update: :*]`, no authorizers
- `elixir-ebau/lib/ebau/user/user_group.ex` -- `defaults [:read, create: :*, update: :*]`, no authorizers

These resources have full CRUD actions with zero authorization. While not directly exposed via JSON:API routes, they are reachable through Ash relationship loading. Combined with C3's fail-open auth, an unauthenticated request could potentially trigger operations on these resources.

**Fix:** Either add `authorizers: [Ash.Policy.Authorizer]` with appropriate policies, or remove the write actions if they're only needed for test setup (use `authorize?: false` in test helpers instead).

---

### C5. `LocalizedField` type declares `:map` storage but database columns are `hstore`

**Files:**
- `elixir-ebau/lib/caluma/types/localized_field.ex:12` -- `storage_type(_), do: :map`
- Affects: `caluma_form_form.name`, `caluma_form_question.label`, `caluma_workflow_workflow.name`

The PostgreSQL `hstore` extension columns store localized strings. `LocalizedField` declares `storage_type :map`, which tells Ecto the column is `jsonb`. Postgrex may auto-detect `hstore` and decode correctly on reads, but writes could fail if the hstore extension encoding isn't properly configured. Since `SyncFormTree` creates forms/questions, this is a correctness risk.

**Fix:** Verify hstore writes work in integration tests. Add an explanatory comment. Consider whether `storage_type` should be `:string` or a custom storage type.

---

### C6. Test uses non-bang `create_gis_link` -- assigns ok-tuple instead of record

**File:** `elixir-ebau/test/ebau/instances/calculations/gis_links_for_instance_test.exs:12-16`

```elixir
gis_link =
  Ebau.Instances.create_gis_link(
    %{name: "test", placeholder: "https://example.com?x={x}&y={y}"},
    actor: actor
  )
```

`create_gis_link/2` returns `{:ok, %GisLink{}}`. The variable gets the tuple, not the record. It's later passed to `Ash.load!/3` (lines 37, 59, 70) which expects a record. Should be `create_gis_link!` (the bang variant).

---

### C7. Portal nginx block still routes all `/api/` to Django

**File:** `proxy/kt_so.conf:47`

```nginx
location ~ ^/(api|graphql|alexandria)/ {
```

The `ebau-portal.localhost` server block was not updated. It still routes all `/api/*` requests to Django. If any portal code hits `/api/v2/`, it will go to Django, not Elixir. This is a latent issue if the portal will ever need Elixir endpoints.

---

## Important Issues (Should Fix)

### I1. No `update` action for GIS links

**File:** `elixir-ebau/lib/ebau/instances/gis_link.ex`

The resource has `create`, `read`, and `destroy` actions but no `update`. The JSON:API routes (`elixir-ebau/lib/ebau/instances.ex:20-26`) have no `patch` route. The frontend has an edit button (which crashes per C1). If this is intentional "delete and recreate," it should be documented. If users need to edit link names/URLs, an update action is missing.

---

### I2. `create_actor!` returns plain map, not `%Ebau.Actor{}` struct

**File:** `elixir-ebau/test/support/ebau/user_helper.ex:128-133`

```elixir
%{user: user, group: group, service: service, role: group.role.slug}
```

Returns a bare map. Production code (`keycloak_bearer_auth.ex:19`) builds `%Ebau.Actor{}`. The typespec on `ConnCase.authenticated_rest_api_conn/2` claims `Ebau.Actor.t()`. This works today because Ash does map-key access, but will break if any code pattern-matches on `%Ebau.Actor{}` or if `@enforce_keys` is added.

**Fix:** `%Ebau.Actor{user: user, group: group, service: service, role: group.role.slug}`

---

### I3. Proxy `/api/` to `/api/v1/` change could break non-versioned Django routes

**File:** `proxy/kt_so.conf:152`

Changed from `^/(api|ech|graphql|...)` to `^/(api\/v1|ech|graphql|...)`. Any Django API path that doesn't use the `/v1/` prefix (e.g., direct `/api/some-resource/`) will no longer route to Django and will fall through to the Ember catch-all.

**Action:** Verify all Django API consumers use the `/api/v1/` prefix. The `/api/v1/dossier-imports` and `/api/swagger/` blocks are fine. Check for any other `/api/` routes.

---

### I4. Token cache uses unverified JWT `exp` for TTL

**File:** `elixir-ebau/lib/ebau_web/token_cache.ex:52-57`

`JOSE.JWT.peek_payload/1` decodes the JWT without verifying the signature. A stolen token could theoretically stay cached beyond its actual revocation if the `exp` claim is far-future. The Keycloak userinfo call validates the token initially, but once cached, revocation is not detected until the unverified `exp` passes.

**Fix:** Either verify the JWT signature locally before trusting `exp`, or use a fixed maximum cache TTL (e.g., 5 minutes) independent of token claims.

---

### I5. ETS token cache table is `:public`

**File:** `elixir-ebau/lib/ebau_web/token_cache.ex:18`

Any process in the VM can read all cached bearer tokens from the ETS table. For a single-app deployment this is typical, but should be documented as a known trade-off. Consider `:protected` access if reads can be routed through the GenServer.

---

### I6. No CORS configuration for the `/api/v2` pipeline

**File:** `elixir-ebau/lib/ebau_web/router.ex:16-20`

If the API is called from browser-based SPAs (which it is -- the Ember app), missing CORS headers will either block requests or require the reverse proxy to handle CORS. If nginx handles CORS, this should be documented. If not, add a CORS plug to the `:api` pipeline.

---

### I7. No unit tests for auth-critical modules

There are no dedicated tests for `EbauWeb.OAuth2`, `EbauWeb.Plugs.KeycloakBearerAuth`, or `EbauWeb.TokenCache`. The test helper bypasses real auth by writing directly to ETS. Missing test scenarios:

- Missing authorization header
- Malformed bearer token
- Valid token but missing `x-camac-group` header
- Valid token but user not found
- Cache expiry and revocation behavior

---

### I8. `Helpers.convert_to_list/1` does not handle `nil`

**File:** `elixir-ebau/lib/ebau/caluma/helpers.ex:61-62`

```elixir
defp convert_to_list(ids) when is_binary(ids), do: [ids]
defp convert_to_list(ids), do: ids
```

If a canton key is missing from `question_ids` and there's no `:default`, `ids` will be `nil`. The catch-all returns `nil`, which would cause an error in the `question_id in ^question_ids` expression downstream.

**Fix:** Add `defp convert_to_list(nil), do: []`

---

### I9. `Document.create_document` explicitly sets `family_id` to `nil`

**File:** `elixir-ebau/lib/caluma/form/document.ex:23-24`

```elixir
# this is only required because the family_id has a DEFAULT of gen_random_uuid() in postgres
change set_attribute(:family_id, nil)
```

This sends `NULL` to the database, overriding the server-side default instead of omitting the column. If downstream code expects `family_id` to be populated, this will cause issues.

**Fix:** Remove the `set_attribute` call to let the DB default kick in, or generate a UUID in Elixir.

---

### I10. `Workflow.Workflow.name` typed as `:map` instead of `LocalizedField`

**File:** `elixir-ebau/lib/caluma/workflow/workflow.ex:25`

```elixir
attribute :name, :map, allow_nil?: false, public?: true
```

All other localized fields (`Form.name`, `Question.label`) use `Caluma.Form.Types.LocalizedField`. This one uses raw `:map`. Inconsistent and misses the string-to-map normalization behavior.

---

### I11. `Mix.Project.project_file/0` in production-available module

**File:** `elixir-ebau/lib/ebau/legacy/config_loader.ex:197`

`ConfigLoader.default_django_root/0` calls `Mix.Project.project_file()`. `Mix` is not available in production releases. While this module is dev/test-only in practice, it ships in production builds under `lib/`.

**Fix:** Raise a clear error if Mix is unavailable, or move the Mix dependency into the calling mix tasks.

---

### I12. Template label `for` attributes are swapped -- accessibility bug

**File:** `ember-ebau-core/addon/templates/service-permissions/gis-links.hbs:3,18-19`

```hbs
<label for="placeholder">{{t "service-permissions.gis-link-name"}}</label>
...
<label for="name">{{t "service-permissions.gis-link-placeholder"}}</label>
```

The `for` attributes point to the wrong input IDs. Clicking either label focuses the wrong field.

---

### I13. Translation strings have extra double spaces

**File:** `ember-ebau-core/translations/service-permissions/de.yaml:67-68`

```yaml
gis-links-save-error: "Der GIS Link  konnte nicht gespeichert werden."
gis-links-delete-confirm: "Möchten Sie den GIS Link  wirklich löschen?"
```

Both have a double space after "Link" that renders visually in the UI.

---

### I14. Missing test coverage for `destroy_gis_link` action

The `GisLink` resource has a `destroy_gis_link` action with a specific policy (admin + service ownership). Neither the unit test file nor the JSON:API test file covers deletion. Minimum tests needed:

- Admin can delete own service's link
- Non-admin cannot delete
- User from different service cannot delete

---

### I15. Missing edge case test: no-plot-data for GIS link calculation

**File:** `elixir-ebau/lib/ebau/instances/calculations/gis_link_for_instance.ex:30-31`

The calculation handles `coordinates(nil)` returning `{"", ""}`. No test covers the case where an instance has no plot data. This is an explicitly coded branch that should be verified.

---

### I16. `InstancesHelper` is dead code

**File:** `elixir-ebau/test/support/ebau/instances_helper.ex`

The module defines `create_instance!/0` but is never referenced in any test file. Remove it.

---

### I17. Stale resource snapshot with wrong type

**Files:**
- `elixir-ebau/priv/resource_snapshots/repo/gis_links/20260330185610.json` -- `service_id` type: `uuid`
- `elixir-ebau/priv/resource_snapshots/repo/gis_links/20260330185733.json` -- `service_id` type: `bigint`

The first snapshot has the wrong type for `service_id`. The migration correctly uses `:bigint`. The stale snapshot should be removed to avoid confusion.

---

### I18. Copy-paste comments in Group and Service policies

**Files:**
- `elixir-ebau/lib/ebau/user/group.ex:25`
- `elixir-ebau/lib/ebau/user/service.ex:21`

Both say `# We don't allow creating users. This is only for testing at the moment` but the resources are Group and Service, not User.

---

### I19. `load_from_bearer` plug may be redundant in API pipeline

**File:** `elixir-ebau/lib/ebau_web/router.ex:18`

The `:api` pipeline has both `:load_from_bearer` (AshAuthentication) and `KeycloakBearerAuth`. These are two different auth mechanisms on the same `Authorization` header. If only Keycloak tokens are expected on `/api/v2`, the AshAuthentication plug is unnecessary overhead.

---

### I20. Authorizers syntax inconsistency: atom vs list

**Files:** `elixir-ebau/lib/ebau/user/group.ex:5`, `elixir-ebau/lib/ebau/user/service.ex:7`

These pass `authorizers: Ash.Policy.Authorizer` (bare atom), while `User` and `Token` pass `authorizers: [Ash.Policy.Authorizer]` (list). Pick one form.

---

### I21. Pagination `hasMore` is fragile with missing metadata

**File:** `ember-ebau-core/addon/resources/paginated.js:91-94`

If `pagination` is `undefined`, the else-branch computes `parseInt(undefined) + parseInt(undefined)` which is `NaN`. The comparison `NaN < undefined` is `false`, which silently reports "no more pages." Add an explicit guard for missing pagination metadata.

---

## Minor Issues (Nice to Have)

### M1. Missing `@moduledoc` on several Caluma modules

Modules without docs: `Caluma.Form`, `Caluma.Form.Answer`, `Caluma.Form.AnswerDocument`, `Caluma.Form.Document`, `Caluma.Workflow`, `Caluma.Workflow.Case`, `Caluma.Form.Changes.CreateRowDocument`, `Caluma.Form.Changes.SetFormQuestionNaturalKey`. Given the onboarding goal, these should follow the pattern of well-documented modules like `SyncFormTree`.

### M2. File path vs module namespace mismatch for types

- `lib/caluma/types/answer_value.ex` defines `Caluma.Form.Types.AnswerValue`
- `lib/caluma/types/localized_field.ex` defines `Caluma.Form.Types.LocalizedField`

Files live under `caluma/types/` but modules are namespaced under `Caluma.Form.Types`. Either move files to `lib/caluma/form/types/` or adjust the module namespace.

### M3. `Ebau.Actor` has no `@enforce_keys`

**File:** `elixir-ebau/lib/ebau/actor.ex:55`

All four fields are optional. A valid actor always needs at least `:user` and `:role`. Adding `@enforce_keys [:user, :role]` would catch construction errors early.

### M4. `GisLink.placeholder` and `GisLink.name` have no length constraints

**File:** `elixir-ebau/lib/ebau/instances/gis_link.ex:36-44`

Both attributes are bare `:string` with no `max_length`. The DB column is `:text` (unlimited). Consider `constraints: [max_length: 2048]` for the URL and `[max_length: 255]` for the name.

### M5. `Secrets` catch-all `secret_for/4` could be more explicit

**File:** `elixir-ebau/lib/ebau/secrets.ex:11-13`

The second clause matches any `path` and dispatches to `oauth2_secret(List.last(path))`. An unexpected path would produce a `FunctionClauseError`. Add a catch-all in `oauth2_secret/1` with a clear error message.

### M6. `load_files!/1` iterates the entries list 6 times

**File:** `elixir-ebau/lib/ebau/legacy/config_loader.ex:155-179`

Inside the transaction, `entries` is filtered 6 times. Use `Enum.group_by(&(&1["model"]))` for a single-pass partition.

### M7. No Erlang version pinned in `.tool-versions`

**File:** `elixir-ebau/.tool-versions`

Only Elixir is pinned. Different developers may get different OTP patch versions.

### M8. `EnsureLegacySchema` unnecessary `List.flatten/1`

**File:** `elixir-ebau/lib/mix/tasks/ebau.ensure_legacy_schema.ex:35`

`Enum.map/2` already returns a flat list. `List.flatten/1` is a no-op.

### M9. Adapter namespace inconsistency

- `ember-ebau-core/addon/adapters/gis-link.js`: `namespace = "/api/v2"` (with leading slash)
- `ember-ebau/app/adapters/gis-link.js`: `namespace = "api/v2"` (without)

The existing convention (e.g., `ApplicationAdapter`) uses no leading slash.

### M10. Missing translations for FR/IT locales

Only `de.yaml` has GIS link translations. While SO canton only uses German, stub entries should be added for consistency if other cantons use this route.

### M11. 6563-line `legacy_structure.sql` committed to git

**File:** `elixir-ebau/priv/repo/legacy_structure.sql`

Large SQL dump in version control. Consider whether this should be generated on-demand rather than committed, similar to `structure.sql` in Rails projects.

### M12. Expression tests use `inspect/1` for assertion -- brittle

**Files:** `test/ebau/caluma/calculations/case_meta_test.exs:42,48,55`, `document_answer_test.exs:44-53`

Tests assert on stringified expression representations (`inspect(expr) =~ "gr-dossier"`). Changes to Ash's expression formatting would break these tests without behavioral change. Prefer structural comparison if possible.

### M13. CI does not pin Elixir to specific patch version

The CI `image: elixir:1.19` doesn't pin to `1.19.5-otp-28` as `.tool-versions` does. CI could use a different patch, leading to subtle divergence.

### M14. `timestamp!/1` accepts `nil` despite bang convention

**File:** `elixir-ebau/lib/ebau/legacy/config_loader.ex:382`

`timestamp!(nil)` returns `nil`. By convention, bang functions raise on invalid input. Minor naming surprise.

### M15. Open TODOs in the codebase

- `lib/ebau/master_data/applicant.ex` -- value_parser not yet supported
- `lib/ebau/master_data/energy_device.ex` -- value_parser not yet supported
- `lib/ebau/master_data/dwelling.ex` -- value_parser not yet supported
- `lib/ebau/master_data/type_of_construction.ex` -- value_mapping not yet supported
- `lib/ebau/instances/instance.ex` -- DSL features not yet supported
- `lib/ebau_web/initialise_scope.ex` -- group not yet added to scope

These are fine as tracked work items, but should be linked to tickets or tracked somewhere to prevent them from going stale.

---

## What Was Done Well

The review agents unanimously noted several strengths:

### Architecture
- **Actor struct design** -- Clean, minimal, well-documented with examples showing policy usage patterns. Serves as a teaching reference.
- **Master Data DSL extension** -- The Spark DSL with a transformer that generates relationships and calculations is elegant. Canton-awareness with `:default` fallback is well-designed.
- **Clean domain separation** -- `Caluma.*` for generic Caluma wrappers, `Ebau.Caluma.*` for app-specific extensions, `Ebau.Instances.*` for business logic. Clear boundaries.
- **DocumentBacked extension** -- Thoughtful bridge between Caluma documents and Ash calculations.

### Code Quality
- **Idiomatic Ash patterns** -- The use of Ash actions, policies, calculations, and relationships follows framework conventions consistently.
- **Policy layering** -- GIS link policies (read scoped to service, destroy requires admin + service, create requires admin with `relate_actor`) are correctly composed.
- **Form-tree sync** -- The `SyncFormTree` change handles both creation and idempotent reapplication of complex nested form structures.
- **Validation modules** -- The `ExistingFormMatchesSpec`, `ExistingQuestionMatchesSpec`, and `ExistingFormQuestionMatchesSpec` validations are thorough and handle edge cases.

### Testing
- **Real database tests** -- No mocking. Tests exercise actual Ash actions against the Ecto sandbox.
- **Test helper documentation** -- `UserHelper`, `CantonFixtures`, and `ConnCase` have thorough `@moduledoc` with usage examples.
- **Canton fixture loading** -- Tests load real Django config fixtures, ensuring parity with production data shapes.
- **Good assertion specificity** -- Tests check actual returned values, not just "no error."

### DevOps
- **GitLab Pages for docs** -- MR preview deployments for documentation are a nice touch.
- **Docker Compose consistency** -- Keycloak env vars added consistently across `kt_so` and `kt_gr`.
- **`.formatter.exs` Quokka exclusions** -- Well-commented with clear rationale for each exclusion.

---

## Recommended Action Plan

### Before Merge (blocking)
1. Fix C1 -- Remove edit button or implement edit functionality end-to-end
2. Fix C2 -- Rename controller class and variable names
3. Fix C3 -- Add 401 response or "require actor" plug for unauthenticated API requests
4. Fix C4 -- Add authorizers/policies to Role, ServiceGroup, UserGroup
5. Verify C5 -- Confirm hstore writes work in integration tests
6. Fix C6 -- Change to `create_gis_link!` (bang variant) in test
7. Address I1-I3 -- Decide on update action, fix actor struct, verify proxy routes

### Shortly After Merge (important but non-blocking)
8. Fix I4-I7 -- Token cache TTL, CORS, auth tests
9. Fix I8-I13 -- nil handling, family_id, accessibility, translations
10. Add missing test coverage (I14-I15)
11. Clean up stale snapshot (I17) and dead code (I16)

### Tech Debt (track in backlog)
12. Address minor issues M1-M15
13. Resolve open TODOs
14. Consider splitting this branch for easier review in the future
