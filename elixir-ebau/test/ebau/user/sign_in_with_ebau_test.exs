defmodule Ebau.User.SignInWithEbauTest do
  use Ebau.DataCase, async: true

  # Drives the real `sign_in_with_ebau` action rather than hand-building
  # `__metadata__`. Without this, neither `RecordKeycloakSession.prepare/3`
  # nor the `oauth_tokens` argument name is exercised anywhere — and both fail
  # silently, leaving back-channel logout permanently inert.

  defp id_token(claims) do
    encode = fn map -> map |> JSON.encode!() |> Base.url_encode64(padding: false) end

    "#{encode.(%{"alg" => "RS256", "typ" => "JWT"})}.#{encode.(claims)}.signature"
  end

  defp sign_in(user, oauth_tokens) do
    user_info = %{
      "sub" => user.username,
      "email" => user.email,
      "email_verified" => true
    }

    # Same entry point the OAuth2 callback plug uses.
    strategy = AshAuthentication.Info.strategy!(Ebau.User.User, :ebau)

    {:ok, user} =
      AshAuthentication.Strategy.action(strategy, :sign_in, %{
        "user_info" => user_info,
        "oauth_tokens" => oauth_tokens
      })

    user
  end

  defp session_token(user) do
    {:ok, %{"jti" => jti}} = AshAuthentication.Jwt.peek(user.__metadata__.token)
    Ebau.User.get_token!(jti, "user", scope: %Ebau.Scope.System{})
  end

  setup do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    %{user: actor.user}
  end

  test "records the Keycloak sid and id_token on the session token", %{user: user} do
    token = id_token(%{"sid" => "sid-from-real-sign-in", "sub" => "keycloak-sub"})

    signed_in = sign_in(user, %{"id_token" => token})

    assert %{extra_data: %{"sid" => "sid-from-real-sign-in", "id_token" => ^token}} =
             session_token(signed_in)
  end

  test "falls back to session_state when the id_token has no sid", %{user: user} do
    token = id_token(%{"session_state" => "legacy-sid", "sub" => "keycloak-sub"})

    signed_in = sign_in(user, %{"id_token" => token})

    assert %{extra_data: %{"sid" => "legacy-sid"}} = session_token(signed_in)
  end

  test "signs in without session data when Keycloak returns no id_token", %{user: user} do
    signed_in = sign_in(user, %{})

    assert %{extra_data: nil} = session_token(signed_in)
  end

  test "signs in without session data when the id_token carries no sid", %{user: user} do
    token = id_token(%{"sub" => "keycloak-sub"})

    signed_in = sign_in(user, %{"id_token" => token})

    assert %{extra_data: nil} = session_token(signed_in)
  end
end
