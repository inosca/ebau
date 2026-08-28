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
    if socket.assigns[:current_user] do
      {:cont, watch_for_revocation(socket, session)}
    else
      {:halt, Phoenix.LiveView.redirect(socket, to: ~p"/elixir/sign-in")}
    end
  end

  # The mount check above cannot see a revocation that happens while the socket
  # is already connected, so listen for one and end the session when it lands.
  defp watch_for_revocation(socket, session) do
    with true <- Phoenix.LiveView.connected?(socket),
         token when is_binary(token) <- session["user_token"],
         {:ok, %{"jti" => jti}} <- AshAuthentication.Jwt.peek(token) do
      :ok = EbauWeb.SessionRevocation.subscribe(jti)

      Phoenix.LiveView.attach_hook(socket, :session_revoked, :handle_info, &handle_revocation/2)
    else
      _ -> socket
    end
  end

  defp handle_revocation(:session_revoked, socket) do
    {:halt, Phoenix.LiveView.redirect(socket, to: ~p"/elixir/sign-in")}
  end

  defp handle_revocation(_message, socket), do: {:cont, socket}
end
