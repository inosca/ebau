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

    service =
      Ebau.User.create_service!(
        %{
          name: "default-service",
          service_group: %{
            name: "default-service-group"
          },
          groups: [group]
        },
        authorize?: false
      )

    %{
      user: user,
      group: group,
      service: service,
      role: group.role.slug
    }
  end
end
