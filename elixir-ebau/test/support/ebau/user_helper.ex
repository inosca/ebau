defmodule Ebau.Test.UserHelper do
  @moduledoc """
  Test helper for building an eBau actor with all required user-side records.

  `create_actor!/1` creates:

  - a user
  - a group for that user
  - a service for that group
  - a service group when needed

  Returns an `%Ebau.Actor{}` struct matching the production shape built by
  `EbauWeb.Plugs.KeycloakBearerAuth`.

  Defaults:

  - role slug: `"municipality-admin"`
  - service group slug: `"municipality"`

  If requested service group already exists, helper reuses it. Otherwise it
  creates it first.

  Examples:

  ```elixir
  actor = Ebau.Test.UserHelper.create_actor!()

  municipality_admin_actor =
    Ebau.Test.UserHelper.create_actor!(%{
      role: %{slug: "municipality-admin"}
    })

  coordination_actor =
    Ebau.Test.UserHelper.create_actor!(%{
      role: %{slug: "service"},
      service_group: %{slug: "coordination"}
    })
  ```
  """

  @doc """
  Creates a test actor and returns user, group, service, and role data.

  Supported overrides:

  - `role.slug`
  - `service_group.slug`

  This helper bypasses authorization for record creation and is intended only
  for tests.

  ## Examples

  ```elixir
  actor = Ebau.Test.UserHelper.create_actor!()
  actor.role
  #=> "municipality-admin"

  actor =
    Ebau.Test.UserHelper.create_actor!(%{
      role: %{slug: "municipality"},
      service_group: %{slug: "municipality"}
    })

  actor.role
  #=> "municipality"
  ```
  """
  @spec create_actor!(map()) :: Ebau.Actor.t()
  def create_actor!(args \\ %{}) do
    user =
      Ebau.User.create_user!(
        %{
          username: "user-#{System.unique_integer()}",
          name: "user",
          surname: "user",
          language: :de
        },
        authorize?: false
      )

    group =
      Ebau.User.create_group!(
        %{
          users: [user],
          role: %{slug: get_in(args, [:role, :slug]) || "municipality-admin"}
        },
        authorize?: false
      )

    service_group_slug = get_in(args, [:service_group, :slug]) || "municipality"

    service_attrs =
      case Ebau.User.get_service_group_by_slug(service_group_slug, authorize?: false) do
        {:error, _error} ->
          %{
            name: "default-service",
            service_group: %{
              name: service_group_slug,
              slug: service_group_slug
            },
            groups: [group]
          }

        {:ok, service_group} ->
          %{
            name: "default-service",
            service_group_id: service_group.id,
            groups: [group]
          }
      end

    service = Ebau.User.create_service!(service_attrs, authorize?: false)

    %Ebau.Actor{
      user: user,
      group: group,
      service: service,
      role: group.role.slug
    }
  end
end
