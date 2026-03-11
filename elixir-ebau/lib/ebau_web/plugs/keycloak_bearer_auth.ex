defmodule EbauWeb.Plugs.KeycloakBearerAuth do
  @moduledoc """
  Plug that authenticates API requests using Keycloak bearer tokens and stores
  the found user in the conn.
  """

  @behaviour Plug

  @impl true
  def init(opts), do: opts

  @impl true
  def call(conn, _opts) do
    with ["Bearer " <> token] <- Plug.Conn.get_req_header(conn, "authorization"),
         {:ok, user} <- EbauWeb.OAuth2.fetch_user(token) do
      Ash.PlugHelpers.set_actor(conn, user)
    else
      _ ->
        conn
    end
  end
end
