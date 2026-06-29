# AST-Grep rules

This directory contains rules for `ast-grep` to maintain code quality and
perform automated refactorings.

The rules here are meant for things that are specific to our own code base,
where there may not be ready-made `ruff` rules for it.

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

The bare-truthiness rule only matches the modules registered via
`load_module_settings(...)` in `camac/settings/django.py`; keep its `MODULE`
list in sync when adding a module.

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
