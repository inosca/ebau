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

  def on_mount(:live_user_required, _params, session, socket) do
    # Try to load user from session if not already assigned
    socket =
      if socket.assigns[:current_user] do
        socket
      else
        case session["user"] do
          nil ->
            socket

          subject when is_binary(subject) ->
            case AshAuthentication.subject_to_user(subject, Ebau.User.User) do
              {:ok, user} -> assign(socket, :current_user, user)
              {:error, _} -> socket
            end
        end
      end

    if socket.assigns[:current_user] do
      scope = %Ebau.Scope{
        current_user: socket.assigns.current_user,
        canton: :gr
      }

      socket =
        socket
        |> assign(:scope, scope)

      {:cont, socket}
    else
      {:halt, Phoenix.LiveView.redirect(socket, to: ~p"/sign-in")}
    end
  end
end
