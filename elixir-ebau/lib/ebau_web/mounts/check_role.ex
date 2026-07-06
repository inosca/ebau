defmodule EbauWeb.Mounts.CheckRole do
  @moduledoc """
  This module can be mounted in a LiveView to check that the current user has a given role.

      defmodule EbauWeb.Live.SomeLiveView do
        on_mount {EbauWeb.Mounts.CheckRole, :admin} # checks that the user has admin role
      end
  """
  import Phoenix.LiveView, only: [redirect: 2]

  @doc """
  Checks if the user has an admin role. If we don't match on any of the checks above we redirect to the root path
  """
  def on_mount(:admin, _params, _session, %{assigns: %{actor: %{role: %{admin_role?: true}}}} = socket) do
    {:cont, socket}
  end

  def on_mount(_opts, _params, _session, socket) do
    socket = redirect(socket, to: "/")
    {:halt, socket}
  end
end
