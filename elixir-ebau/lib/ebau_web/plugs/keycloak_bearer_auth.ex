defmodule EbauWeb.Plugs.KeycloakBearerAuth do
  @moduledoc """
  Plug that authenticates API requests using Keycloak bearer tokens.

  Validates the token, looks up the user by email, and sets the Ash actor.
  Passes through silently if no bearer token is present or if
  `load_from_bearer` already set an actor (AshAuthentication tokens).
  """

  @behaviour Plug

  require Logger

  @impl true
  def init(opts), do: opts

  @impl true
  def call(conn, _opts) do
    with ["Bearer " <> token] <- Plug.Conn.get_req_header(conn, "authorization"),
         {:ok, claims} <- Ebau.KeycloakTokenValidator.validate_token(token),
         {:ok, user} <- Ebau.User.get_user_by_email(claims["email"], authorize?: false) do
      Ash.PlugHelpers.set_actor(conn, user)
    else
      [] ->
        conn

      {:error, reason} ->
        Logger.warning("Keycloak bearer auth failed: #{inspect(reason)}")
        conn
    end
  end
end
