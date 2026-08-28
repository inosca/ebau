defmodule Ebau.User.TokenLifetimeTest do
  use Ebau.DataCase, async: true

  # Keycloak only sends a back-channel logout token on an explicit logout,
  # never when a session expires (keycloak#25171). The session here therefore
  # has to expire on its own, close to when the Keycloak session it was
  # created from would, rather than living for AshAuthentication's default of
  # 14 days.
  test "a session token expires with the Keycloak SSO session, not 14 days later" do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    {:ok, token, _claims} = AshAuthentication.Jwt.token_for_user(actor.user)
    {:ok, %{"exp" => exp, "iat" => iat}} = AshAuthentication.Jwt.peek(token)

    assert exp - iat == 10 * 60 * 60
  end
end
