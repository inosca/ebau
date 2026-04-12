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
  role: "municipality-admin"
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

For instance-level access, we check ACLs:

```elixir
policy action(:list_instances) do
  authorize_if expr(
    exists(active_instance_acls, user_id == ^actor([:user, :id]))
  )
end
```

### Role-based access

Admin-only actions use the `IsAdminRole` simple check:

```elixir
policy action_type(:create) do
  authorize_if Ebau.User.Policies.IsAdminRole
end
```

This checks `String.ends_with?(actor.role, "-admin")`.

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

For custom logic, implement `Ash.Policy.SimpleCheck`:

```elixir
defmodule Ebau.User.Policies.IsAdminRole do
  use Ash.Policy.SimpleCheck

  @impl true
  def describe(_opts), do: "actor role ends with -admin"

  @impl true
  def match?(%{role: role}, _context, _opts) when is_binary(role) do
    String.ends_with?(role, "-admin")
  end

  def match?(_, _, _), do: false
end
```

## Further reading

- [Ash policies guide](https://hexdocs.pm/ash/policies.html)
- [Ash policy checks](https://hexdocs.pm/ash/policy-checks.html)
- [Ash.Policy.SimpleCheck](https://hexdocs.pm/ash/Ash.Policy.SimpleCheck.html)
