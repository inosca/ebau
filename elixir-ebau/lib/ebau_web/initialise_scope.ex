defmodule EbauWeb.InitialiseScope do
  @moduledoc """
  Initialises the scope of the application.

  The "scope" is a struct (a map with predefined keys) that holds information such as:
  - current_user (the user who is doing something)
  - current_tenant (the canton the applicatioon is running in, ex: :gr)
  - locale (the current locale that the user is using)

  The scope is then subsequently passed around through the entire application.

  See: https://hexdocs.pm/ash/Ash.Scope.html
  """
  import Phoenix.Component, only: [assign: 3]

  def on_mount(_action, _params, _session, socket) do
    scope = %Ebau.Scope{
      current_user: nil,
      # TODO: load from env
      current_tenant: :gr,
      locale: nil
    }

    {:cont, assign(socket, :scope, scope)}
  end
end
