# AST-Grep rules

This directory contains rules for `ast-grep` to maintain code quality and
perform automated refactorings.

The rules here are meant for things that are specific to our own code base,
where there may not be ready-made `ruff` rules for it.

Rules live in `rules/`, reusable [utility
rules](https://ast-grep.github.io/guide/rule-config/utility-rule.html) that are
shared between them live in `utils/`. Both directories are registered in
`sgconfig.yml` in the project root.

## Rules Overview

### Pytest Django DB Migration

These rules automatically replace the `db` and `transactional_db` pytest
fixtures with the corresponding `@pytest.mark.django_db` decorators.

- `db` fixture is replaced by `@pytest.mark.django_db`
- `transactional_db` fixture is replaced by `@pytest.mark.django_db(transaction=True)`

Using decorators is preferred over fixtures as function arguments for database
access in tests.

### Module enabled checks

These rules enforce using `is_module_enabled("MODULE")` for checking whether a
module is enabled, instead of reaching into the config directly. The helper
handles both pydantic (`.enabled`) and dict (`["ENABLED"]` or empty dict checks)
module configs.

- `settings.MODULE.enabled` is replaced by `is_module_enabled("MODULE")`
- `settings.MODULE["ENABLED"]` is replaced by `is_module_enabled("MODULE")`
- `settings.MODULE.get("ENABLED")` / `settings.MODULE.get("ENABLED", False)` is
  replaced by `is_module_enabled("MODULE")`
- a bare `settings.MODULE` truthiness check (in `if` / `elif` / `while`
  conditions, `not settings.MODULE`, or `bool(settings.MODULE)`) is replaced by
  `is_module_enabled("MODULE")`

The autofix does not add the import, you have to add it yourself:

```python
from camac.settings.utils import is_module_enabled
```

These rules only match the modules registered via `load_module_settings(...)` in
`camac/settings/django.py`, which are enumerated in the `module-settings-name`
util rule in `utils/module_settings.yaml`. `ast-grep` can't read that list from
the Django settings, so a third rule (`register-module-settings-name`) makes
sure we don't forget to update it: it fails the linting for every
`load_module_settings(...)` call in `camac/settings/django.py` whose settings
name is missing from the util rule.

### Application name checks (frontend)

These rules enforce using `isApplication("xy")` for checking which canton the
frontend runs as, instead of comparing the name by hand.

- `=== "xy"` is replaced by `isApplication("xy")`
- `!== "xy"` is replaced by `!isApplication("xy")`

Both apply whether or not the comparison is wrapped in a `macroCondition(...)`,
which is dropped along the way.

Which reads count as the application name is defined by the `application-name`
util rule in `utils/application_name.yaml`: the `@embroider/macros` own config
and `ember-ebau-core/config/main`, the two sources `isApplication` itself
resolves. Reads of an app's own `config/environment` are left alone, since that
is a different configuration object: `ember-caluma-portal/tests/helpers/test-if.js`
deliberately checks `config.APPLICATION.name`.

`macroCondition` on the application is still legitimate in
`ember-ebau-core/addon/config` and in
`ember-ebau-core/addon/caluma-query/models/case.js`, where it pairs with
`importSync` to pick a single canton config module at build time. Converting
those would bundle every canton into every build, so both paths are ignored by
the rules.

The autofix does not add the import, you have to add it yourself:

```js
import { isApplication } from "ember-ebau-core/helpers/is-application";
```

In templates, use the `is-application` helper instead. The rules only cover
`.js` files, `ast-grep` cannot parse `.hbs`.

### Response assertions in tests

This rule forbids asserting on the `.data` attribute of a response in tests.

[`.data`][drf-data] is DRF's "unrendered, serialized data of the response": it
never passes through the renderer, whereas [`.json()`][django-json] is Django's
test client method that parses the bytes the response actually sent.

On a JSON:API endpoint `.data` therefore lacks the
`data`/`attributes`/`relationships` envelope and the dasherized field names the
frontend receives, error responses are a bare `ErrorDetail` list instead of
`{"errors": [...]}`, and values can still be `datetime` or `Decimal` objects.
Asserting on it silently skips the layer most likely to break.

[drf-data]: https://www.django-rest-framework.org/api-guide/responses/#data
[django-json]: https://docs.djangoproject.com/en/5.2/topics/testing/tools/#django.test.Response.json

Use `response.json()` instead. The rule has no autofix, because the two are not
interchangeable, the assertion has to be adjusted to the rendered shape:

```python
# JSON:API list
assert len(response.json()["data"]) == 2
# JSON:API detail
assert response.json()["data"]["attributes"]["some-field"] == "foo"
# errors
assert response.json()["errors"][0]["detail"] == "Nope"
```

## Running the fixes

If CI reports violations of these rules, you can automatically apply the
suggested fixes by running:

```bash
ast-grep scan --update-all
```

## Post-fix formatting

Since `ast-grep` may introduce formatting changes that don't match the project's
style exactly, you should always run `ruff format` after applying fixes:

```bash
# From the project root
make format
# Or specifically for django
cd django && ruff format
```
