# Statistics XLSX Templates

Templates live in `django/camac/statistics/config/<canton>/` and follow the pattern:

```
{type}_{identifier}.xlsx
```

**type**: `dossier`, `work-items`, `billings`, `rpg2`
**identifier**: service slug, service-group slug or role slug

## Resolution order (first existing file wins)

1. `{type}_{service}.xlsx`
2. `{type}_{service_group}.xlsx`
3. `{type}_{role}.xlsx`
4. `{type}_export.xlsx`

No template found → data-only export without extra sheets.

## Template structure

- **Sheet 1**: overwritten with exported data
- **Sheet 2+**: preserved as-is (pivot tables, charts, etc.)
