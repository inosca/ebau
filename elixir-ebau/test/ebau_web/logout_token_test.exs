defmodule EbauWeb.LogoutTokenTest do
  use ExUnit.Case, async: false

  alias Ebau.Test.KeycloakHelper
  alias EbauWeb.LogoutToken

  setup do
    KeycloakHelper.stub_jwks()
    :ok
  end

  defp signed(overrides \\ %{}) do
    KeycloakHelper.sign_logout_token(KeycloakHelper.logout_token_claims(overrides))
  end

  test "accepts a well-formed logout token" do
    assert {:ok, %{sid: "test-sid", sub: "keycloak-sub"}} = LogoutToken.verify(signed())
  end

  test "accepts a token identified only by sub" do
    claims = KeycloakHelper.logout_token_claims() |> Map.delete("sid")

    assert {:ok, %{sid: nil, sub: "keycloak-sub"}} =
             LogoutToken.verify(KeycloakHelper.sign_logout_token(claims))
  end

  test "rejects a token signed by an unknown key" do
    {_meta, token} =
      {:rsa, 2048}
      |> JOSE.JWK.generate_key()
      |> JOSE.JWT.sign(
        %{"alg" => "RS256", "kid" => "test-key", "typ" => "JWT"},
        KeycloakHelper.logout_token_claims()
      )
      |> JOSE.JWS.compact()

    assert {:error, :invalid_signature} = LogoutToken.verify(token)
  end

  test "rejects a token from the wrong issuer" do
    assert {:error, :invalid_issuer} =
             LogoutToken.verify(signed(%{"iss" => "https://evil.example/realms/ebau"}))
  end

  test "rejects a token for a different audience" do
    assert {:error, :invalid_audience} = LogoutToken.verify(signed(%{"aud" => "other-client"}))
  end

  test "rejects a token without the backchannel-logout event" do
    assert {:error, :not_a_logout_token} = LogoutToken.verify(signed(%{"events" => %{}}))
  end

  test "rejects a token carrying a nonce" do
    assert {:error, :nonce_present} = LogoutToken.verify(signed(%{"nonce" => "abc"}))
  end

  test "rejects a stale token" do
    stale = System.system_time(:second) - 600

    assert {:error, :stale} = LogoutToken.verify(signed(%{"iat" => stale}))
  end

  test "rejects a token identifying neither a session nor a subject" do
    claims = KeycloakHelper.logout_token_claims() |> Map.drop(["sid", "sub"])

    assert {:error, :no_subject_or_sid} =
             LogoutToken.verify(KeycloakHelper.sign_logout_token(claims))
  end

  test "rejects something that is not a JWT" do
    assert {:error, :malformed} = LogoutToken.verify("not-a-jwt")
    assert {:error, :malformed} = LogoutToken.verify(nil)
  end

  test "rejects a token authorized for a different party" do
    assert {:error, :invalid_authorized_party} =
             LogoutToken.verify(signed(%{"azp" => "other-client"}))
  end

  test "rejects a token whose exp has passed" do
    expired = System.system_time(:second) - 600

    assert {:error, :expired} = LogoutToken.verify(signed(%{"exp" => expired}))
  end

  test "accepts a token whose exp is still in the future" do
    future = System.system_time(:second) + 600

    assert {:ok, _} = LogoutToken.verify(signed(%{"exp" => future}))
  end

  # The events claim is what stops an ID or access token for this same client
  # being replayed here as a logout notification, so its shape matters.
  test "rejects a token whose logout event is not an object" do
    claims = %{"events" => %{"http://schemas.openid.net/event/backchannel-logout" => "yes"}}

    assert {:error, :not_a_logout_token} = LogoutToken.verify(signed(claims))
  end

  test "rejects a token signed with an algorithm we do not accept" do
    unsigned =
      %{"alg" => "none", "typ" => "JWT"}
      |> then(&(&1 |> JSON.encode!() |> Base.url_encode64(padding: false)))
      |> then(fn header ->
        claims =
          KeycloakHelper.logout_token_claims()
          |> JSON.encode!()
          |> Base.url_encode64(padding: false)

        "#{header}.#{claims}."
      end)

    assert {:error, :invalid_signature} = LogoutToken.verify(unsigned)
  end
end
