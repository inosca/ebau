# Docker Compose Setup

We heavily rely on docker-compose to manage our customer-specific dev, ci, stage
and production environments. The goal of the current docker-compose setup is a
fast feedback loop and simplicity.

The GitLab CI build and deploy stages should only build/deploy containers which
a customer actually requires. We DONT want to build a superset of all containers
for every customer release.

## Shared services

Services that several cantons run identically live in `compose/services/` and
are pulled into a canton's file with `include`, rather than being copied:

```yaml
include:
  - path: services/elixir-dev.yml
```

The including file is merged on top, so anything canton-specific stays in the
canton's own file. Only cantons that list the include get the container, which
keeps the "don't build a superset for every customer" rule above intact.
