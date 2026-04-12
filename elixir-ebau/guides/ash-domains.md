# Ash Domains

Ash organizes resources into **domains**, modules that act as the public API
for a group of related resources. In eBau we have four domains:

| Domain | Purpose |
|---|---|
| `Ebau.User` | Users, roles, groups, services |
| `Ebau.Instances` | Building permit instances and GIS links |
| `Ebau.Permissions` | Instance-level access control (ACLs) |
| `Ebau.MasterData` | Read-only form-derived master data (applicants, plots, dwellings, ...) |

Additionally, two Caluma domains mirror the upstream Django schema:

| Domain | Purpose |
|---|---|
| `Caluma.Form` | Forms, questions, documents, answers |
| `Caluma.Workflow` | Workflows and cases |

## How domains work

A domain defines code interface functions for its resources. These are the
functions you call from application code. Never call `Ash.create!` or
`Ash.read!` directly.

```elixir
# Good: use the domain function
Ebau.User.create_user!(%{username: "alice", ...}, authorize?: false)

# Bad: bypasses the domain
Ash.create!(Ebau.User.User, %{username: "alice", ...})
```

Each `define` in the domain maps to an action on the resource:

```elixir
defmodule Ebau.User do
  use Ash.Domain

  resources do
    resource Ebau.User.User do
      define :create_user, action: :create
      define :get_user_by_email, get_by: :email, action: :read
    end
  end
end
```

## JSON:API routing

Domains that expose HTTP endpoints use the `AshJsonApi.Domain` extension.
Routes are declared inside a `json_api` block:

```elixir
defmodule Ebau.Instances do
  use Ash.Domain, extensions: [AshJsonApi.Domain]

  json_api do
    routes do
      base_route "/gis-links", Ebau.Instances.GisLink do
        index :read_gis_links
        post :create_gis_link
        delete :destroy_gis_link
      end
    end
  end
end
```

These routes are mounted via `AshJsonApi.Router` in the Phoenix router under
the `/api/v2` prefix.

## Further reading

- [Ash Domains guide](https://hexdocs.pm/ash/domains.html)
- [Ash code interface](https://hexdocs.pm/ash/code-interface.html)
- [AshJsonApi routing](https://hexdocs.pm/ash_json_api/route-resource-usage.html)
