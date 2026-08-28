defmodule Ebau.Test.KeycloakHelper do
  @moduledoc """
  Mints RS256 logout tokens signed by a throwaway key pair and serves the
  matching JWKS, so back-channel logout can be tested without a live Keycloak.
  """

  @kid "test-key"

  @doc """
  The private JWK used to sign test tokens.

  Generated once per VM: a 2048-bit RSA keygen is slow enough to notice if
  every test does it.
  """
  @spec signing_jwk() :: JOSE.JWK.t()
  def signing_jwk do
    case :persistent_term.get({__MODULE__, :jwk}, nil) do
      nil ->
        jwk = JOSE.JWK.generate_key({:rsa, 2048})
        :persistent_term.put({__MODULE__, :jwk}, jwk)
        jwk

      jwk ->
        jwk
    end
  end

  @doc """
  The public JWKS document matching `signing_jwk/0`.
  """
  @spec jwks() :: map()
  def jwks do
    {_meta, public} =
      signing_jwk()
      |> JOSE.JWK.to_public()
      |> JOSE.JWK.to_map()

    %{"keys" => [Map.merge(public, %{"kid" => @kid, "use" => "sig", "alg" => "RS256"})]}
  end

  @doc """
  Signs `claims` as an RS256 JWT with the test key.
  """
  @spec sign_logout_token(map()) :: String.t()
  def sign_logout_token(claims) do
    {_meta, token} =
      signing_jwk()
      |> JOSE.JWT.sign(%{"alg" => "RS256", "kid" => @kid, "typ" => "JWT"}, claims)
      |> JOSE.JWS.compact()

    token
  end

  @doc """
  The claims Keycloak puts in a back-channel logout token, with `overrides`
  merged over them.
  """
  @spec logout_token_claims(map()) :: map()
  def logout_token_claims(overrides \\ %{}) do
    Map.merge(
      %{
        "iss" => issuer(),
        "aud" => Ebau.Secrets.keycloak_config() |> Keyword.fetch!(:client_id),
        "iat" => System.system_time(:second),
        "jti" => Ecto.UUID.generate(),
        "sub" => "keycloak-sub",
        "sid" => "test-sid",
        "events" => %{"http://schemas.openid.net/event/backchannel-logout" => %{}}
      },
      overrides
    )
  end

  @doc """
  The issuer Keycloak stamps on tokens for the configured realm.
  """
  @spec issuer() :: String.t()
  def issuer do
    keycloak = Ebau.Secrets.keycloak_config()
    url = Keyword.fetch!(keycloak, :url)
    realm = Keyword.fetch!(keycloak, :realm)

    String.trim_trailing(url, "/") <> "/realms/#{realm}"
  end

  @doc """
  Serves `jwks/0` to `EbauWeb.LogoutToken` in place of Keycloak.
  """
  @spec stub_jwks() :: :ok
  def stub_jwks do
    jwks = jwks()
    Req.Test.stub(EbauWeb.LogoutToken, &Req.Test.json(&1, jwks))
  end

  @doc """
  Stores `extra_data` on the session token held by the signed-in `conn`, the
  way `Ebau.User.Preparations.RecordKeycloakSession` does at sign-in.
  """
  @spec attach_session(Plug.Conn.t(), map()) :: Ash.Resource.record()
  def attach_session(conn, extra_data) do
    {:ok, %{"jti" => jti}} =
      conn |> Plug.Conn.get_session("user_token") |> AshAuthentication.Jwt.peek()

    jti
    |> Ebau.User.get_token!("user", scope: %Ebau.Scope.System{})
    |> Ebau.User.set_keycloak_session!(%{extra_data: extra_data}, scope: %Ebau.Scope.System{})
  end
end
