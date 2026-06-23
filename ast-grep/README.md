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
