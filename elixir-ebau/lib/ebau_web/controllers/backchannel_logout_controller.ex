defmodule EbauWeb.BackchannelLogoutController do
  @moduledoc """
  Receives OIDC back-channel logout tokens from Keycloak.

  Keycloak posts here server-to-server whenever an SSO session ends, whichever
  app initiated it. Every Phoenix session recorded against that Keycloak `sid`
  is revoked, which is what makes logging out in the Ember app also end the
  Phoenix session.

  Unauthenticated by design: the request carries no cookie and no CSRF token.
  Its only credential is the signature on the logout token, which
  `EbauWeb.LogoutToken` verifies against Keycloak's JWKS.
  """
  use EbauWeb, :controller

  require Logger

  @doc """
  Revokes every Phoenix session belonging to the Keycloak session being ended.
  """
  @spec create(Plug.Conn.t(), map()) :: Plug.Conn.t()
  def create(conn, %{"logout_token" => logout_token}) do
    case EbauWeb.LogoutToken.verify(logout_token) do
      {:ok, %{sid: sid}} when is_binary(sid) ->
        revoke_sessions(sid)
        send_resp(conn, 200, "")

      # Keycloak only omits the `sid` when `backchannel.logout.session.required`
      # is off. Falling back to `sub` would end the user's sessions on their
      # other devices, which the Ember app never does.
      {:ok, %{sid: nil}} ->
        Logger.warning("Ignoring logout token without a sid; sub-wide logout is not supported")
        send_resp(conn, 200, "")

      # Not a bad token: we could not reach Keycloak to check it. Keycloak does
      # not retry, so this is reported as our failure rather than the sender's
      # so it shows up as such in monitoring.
      {:error, reason} when reason in [:jwks_unavailable, :unknown_kid] ->
        Logger.error("Could not verify a back-channel logout token: #{inspect(reason)}")
        send_resp(conn, 503, "")

      {:error, reason} ->
        Logger.warning("Rejected back-channel logout token: #{inspect(reason)}")
        send_resp(conn, 400, "")
    end
  end

  def create(conn, _params), do: send_resp(conn, 400, "")

  # Revoking upserts the token row to `purpose: "revocation"`, so the
  # `get_token(jti, purpose: "user")` lookup that authenticates every request
  # stops matching and the session is dead on its next use.
  @spec revoke_sessions(String.t()) :: :ok
  defp revoke_sessions(sid) do
    tokens = Ebau.User.session_tokens_by_keycloak_sid!(sid, scope: %Ebau.Scope.System{})

    Logger.info("Back-channel logout for sid #{sid}: revoking #{length(tokens)} session(s)")

    Enum.each(tokens, &revoke_session/1)
  end

  # One failure must not abandon the sessions after it: Keycloak does not retry,
  # so anything skipped here stays signed in for the rest of its lifetime.
  #
  # The `id_token` is dropped from the row first: the revocation record it
  # becomes is never expunged.
  @spec revoke_session(Ash.Resource.record()) :: :ok
  defp revoke_session(token) do
    with {:ok, _token} <-
           Ebau.User.set_keycloak_session(token, %{extra_data: nil}, scope: %Ebau.Scope.System{}),
         :ok <-
           AshAuthentication.TokenResource.Actions.revoke_jti(
             Ebau.User.Token,
             token.jti,
             token.subject
           ) do
      EbauWeb.SessionRevocation.broadcast(token.jti)
    else
      error -> Logger.error("Could not revoke session #{token.jti}: #{inspect(error)}")
    end

    :ok
  end
end
