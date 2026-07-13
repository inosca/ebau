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
    %{name: "GIS", placeholder: "https://example.com/map"},
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

  @group_load [:name, :role, service: [:service_group]]

  @doc """
  Builds an `%Ebau.Actor{}` from a user and its active group. The group
  must have `:service` and `:role` loaded.
  """
  @spec new(Ebau.User.User.t(), Ebau.User.Group.t()) :: t()
  def new(user, group) do
    %__MODULE__{
      user: user,
      group: group,
      service: group.service,
      role: group.role
    }
  end

  @doc """
  Assembles an `%Ebau.Actor{}` from the authenticated user, using the
  user's persisted default group as the active group. Users without a
  default group fall back to their first group, so they can still act
  (and persist a default via the group switcher).

  `locale` is passed as Ash context so localised calculations (group
  names shown in the navbar) resolve in the user's language.

  Returns `{:error, reason}` when:

    * `user` is nil (unauthenticated)
    * the user belongs to no groups at all
    * the load fails (forbidden / not found)

  Kept minimal on purpose — only loads what the actor itself needs
  (`group.service`, `group.role`) and the user's groups (used by the
  navbar group switcher).
  """
  @spec build(Ebau.User.User.t() | nil, String.t() | nil) :: {:ok, t()} | {:error, term()}
  def build(user, locale \\ nil)

  def build(nil, _locale), do: {:error, "user is nil"}

  def build(user, locale) do
    opts = [actor: %{user: user}, context: %{locale: locale}]

    with {:ok, user} <- Ash.load(user, [groups: [:name], default_group: @group_load], opts),
         {:ok, group} <- active_group(user, opts) do
      {:ok, new(user, group)}
    end
  end

  defp active_group(%{default_group: %Ebau.User.Group{} = group}, _opts), do: {:ok, group}
  defp active_group(%{groups: [group | _]}, opts), do: Ash.load(group, @group_load, opts)
  defp active_group(_user, _opts), do: {:error, "user has no groups"}
end
