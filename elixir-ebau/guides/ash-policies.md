# Ash Policies in eBau

eBau uses [Ash policies](https://hexdocs.pm/ash/policies.html) for
authorization. Every resource that needs access control declares
`authorizers: Ash.Policy.Authorizer` and a `policies` block.

## The Actor

All authorized actions receive an `actor:` option. In eBau, the actor is an
`%Ebau.Actor{}` struct with four fields:

```elixir
%Ebau.Actor{
  user: %Ebau.User.User{},
  group: %Ebau.User.Group{},
  service: %Ebau.User.Service{},
  role: String.t() # example: "municipality-admin"
}
```

The actor is built by `EbauWeb.Plugs.KeycloakBearerAuth` from the bearer
token and the `x-camac-group` header on every API request.

## Policy patterns

### Relationship-based access

The most common pattern checks whether the actor is related to the resource
through a relationship:

```elixir
policy action_type(:read) do
  authorize_if relates_to_actor_via(:service, field: :service)
end
```

This authorizes reads when `resource.service_id == actor.service.id`.

For instance-level access, use `Ebau.Policies.Checks.HasActiveInstanceACL`. It is a
`FilterCheck` that checks whether the actor matches any active instance ACL (by user,
role, service, or service group) reachable through a given relationship path:

```elixir
# Resource is the instance (or has instance.active_instance_acls directly)
policy action_type(:read) do
  authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: []}
end

# Resource relates to a case through a single relationship
policy action_type(:read) do
  authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:case]}
end

# Multi-hop: row document → root document → case
policy action_type(:read) do
  authorize_if {Ebau.Policies.Checks.HasActiveInstanceACL, via: [:family, :case]}
end
```

The `via:` option names the relationship steps from the current resource to a
`Caluma.Workflow.Case`. The check then traverses `case.instance.active_instance_acls`
and matches the actor's user id, role id, service id, and service group id.

### Reference data (allow reads, forbid writes)

Resources that are managed by Django or the config loader (roles, service
groups, the user-group join table) allow reads but forbid all writes:

```elixir
policies do
  policy action_type(:read) do
    authorize_if always()
  end

  policy action_type([:create, :update, :destroy]) do
    forbid_if always()
  end
end
```

Tests bypass this with `authorize?: false`.

### Group membership

Groups are readable only by their own members:

```elixir
policy action(:get_group_for_actor) do
  authorize_if relates_to_actor_via(:users, field: :user)
end
```

## Bypassing authorization in tests

Test helpers use `authorize?: false` to skip policies:

```elixir
Ebau.User.create_role!(%{slug: "admin"}, authorize?: false)
actor = Ebau.Test.UserHelper.create_actor!()
```

The `create_actor!` helper passes `authorize?: false` internally for all
record creation.

## Writing a new policy check

Ash provides two main types of custom policy checks:

- `Ash.Policy.SimpleCheck` — for checks based on the actor/context (evaluated in Elixir)
- `Ash.Policy.FilterCheck` — for checks that can be expressed as a data-layer filter (pushed to SQL)

See the [Ash policy checks documentation](https://hexdocs.pm/ash/policy-checks.html) for details.

Example `SimpleCheck`:

```elixir
defmodule Ebau.User.Policies.IsAdminRole do
  use Ash.Policy.SimpleCheck

  @impl true
  def describe(_opts), do: "actor role ends with -admin"

  @impl true
  def match?(%{role: %{slug: slug}}, _context, _options) do
    String.ends_with?(slug, "-admin")
  end

  def match?(_, _, _), do: false
end
```

## Further reading

- [Ash policies guide](https://hexdocs.pm/ash/policies.html)
- [Ash policy checks](https://hexdocs.pm/ash/policy-checks.html)
- [Ash.Policy.SimpleCheck](https://hexdocs.pm/ash/Ash.Policy.SimpleCheck.html)
- [Ash.Policy.FilterCheck](https://hexdocs.pm/ash/Ash.Policy.FilterCheck.html)
