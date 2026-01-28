defmodule EbauWeb.LiveUserAuth do
  @moduledoc """
  Helpers for authenticating users in LiveViews.
  """

  use EbauWeb, :verified_routes

  import Phoenix.Component

  def on_mount(:live_user_optional, _params, _session, socket) do
    if socket.assigns[:current_user] do
      {:cont, socket}
    else
      {:cont, assign(socket, :current_user, nil)}
    end
  end

  def on_mount(:live_user_required, _params, _session, socket) do
    if socket.assigns[:current_user] do
      user =
        Ash.load!(
          socket.assigns.current_user,
          [
            :service,
            :full_name,
            group: [:localised_name, role: :resources]
          ],
          scope: socket.assigns.scope
        )

      scope = Map.put(socket.assigns.scope, :current_user, user)

      socket =
        socket
        |> assign(:scope, scope)
        |> assign(:current_user, user)

      {:cont, socket}
    else
      {:halt, Phoenix.LiveView.redirect(socket, to: ~p"/sign-in")}
    end
  end
end
