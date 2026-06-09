defmodule Ebau.Actor do
  @moduledoc """
  Describes an eBau actor.

  An eBau actor is a struct with fields `:user`, `:group`, `:service`, `:role`.
  This actor struct is passed as `actor:` to Ash actions and is also used by Ash
  policies.

  ## Examples

  Build actor from resolved user/group/service:

  ```elixir
  %Ebau.Actor{
    user: user,
    group: group,
    service: group.service,
    role: group.role
  }
  ```

  Use actor in an Ash action:

  ```elixir
  Ebau.Instances.create_gis_link!(
    %{name: "GIS", placeholder: "https://example.com?x={x}&y={y}"},
    actor: actor
  )
  ```

  Use actor fields in policies:

  ```elixir
  policy action(:read_something) do
    authorize_if relates_to_actor_via(:service, field: :service)
  end

  policy action_type(:read) do
    authorize_if expr(exists(active_instance_acls, user_id == ^actor([:user, :id])))
  end

  policy action_type(:create) do
    authorize_if Ebau.User.Policies.IsAdminRole
  end
  ```
  """

  @type t :: %__MODULE__{
          user: Ebau.User.User.t(),
          group: Ebau.User.Group.t(),
          service: Ebau.User.Service.t(),
          role: Ebau.User.Role.t()
        }

  @enforce_keys [:user, :group, :service, :role]
  defstruct [:user, :group, :service, :role]
end
