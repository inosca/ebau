defmodule Ebau.Test.UserHelper do
  def create_actor!(args \\ %{}) do
    # todo: pre-seed test database with fixtures that we have in user.json etc.
    # so things like the roles are always fixed
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

    %{
      user: user,
      group: group,
      service: service,
      role: group.role.slug
    }
  end
end
