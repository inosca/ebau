defmodule EbauWeb.BackchannelLogoutControllerTest do
  use EbauWeb.ConnCase, async: false

  alias Ebau.Test.{KeycloakHelper, UserHelper}

  setup %{conn: conn} do
    KeycloakHelper.stub_jwks()
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    actor = UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    authed = log_in_actor(conn, actor)
    KeycloakHelper.attach_session(authed, %{sid: "test-sid", id_token: "the.id.token"})

    %{conn: conn, authed: authed}
  end

  defp post_logout_token(conn, token) do
    conn
    |> put_req_header("content-type", "application/x-www-form-urlencoded")
    |> post(~p"/elixir/backchannel-logout", "logout_token=#{token}")
  end

  test "a valid logout token ends the matching phoenix session", %{conn: conn, authed: authed} do
    assert get(authed, ~p"/service-permissions/gis-links").status == 200

    logout_token = KeycloakHelper.sign_logout_token(KeycloakHelper.logout_token_claims())

    assert post_logout_token(conn, logout_token).status == 200

    assert redirected_to(get(authed, ~p"/service-permissions/gis-links")) == ~p"/elixir/sign-in"
  end

  test "the id_token is dropped from the revoked row so it is not kept forever", %{conn: conn} do
    logout_token = KeycloakHelper.sign_logout_token(KeycloakHelper.logout_token_claims())

    assert post_logout_token(conn, logout_token).status == 200

    assert Ebau.User.session_tokens_by_keycloak_sid!("test-sid", scope: %Ebau.Scope.System{}) ==
             []

    assert [%{purpose: "revocation", extra_data: nil}] =
             Ash.read!(Ebau.User.Token, authorize?: false, actor: nil)
  end

  test "a logout token for another session leaves this one alone", %{
    conn: conn,
    authed: authed
  } do
    logout_token =
      KeycloakHelper.sign_logout_token(
        KeycloakHelper.logout_token_claims(%{"sid" => "other-sid"})
      )

    assert post_logout_token(conn, logout_token).status == 200
    assert get(authed, ~p"/service-permissions/gis-links").status == 200
  end

  # Keycloak only sends `sub` when `backchannel.logout.session.required` is
  # off. Acting on it would end the user's sessions on their other devices,
  # which the Ember app never does, so it is acknowledged but ignored.
  test "a token identifying only a subject is acknowledged but changes nothing", %{
    conn: conn,
    authed: authed
  } do
    claims = KeycloakHelper.logout_token_claims() |> Map.delete("sid")

    assert post_logout_token(conn, KeycloakHelper.sign_logout_token(claims)).status == 200
    assert get(authed, ~p"/service-permissions/gis-links").status == 200
  end

  test "an unsigned token is rejected and changes nothing", %{conn: conn, authed: authed} do
    assert post_logout_token(conn, "not-a-jwt").status == 400
    assert get(authed, ~p"/service-permissions/gis-links").status == 200
  end

  # Keycloak does not retry, so an outage on our side must not look like a
  # bad token to whoever reads the logs.
  test "answers 503 when Keycloak's JWKS cannot be fetched", %{conn: conn, authed: authed} do
    Req.Test.stub(EbauWeb.LogoutToken, &Req.Test.transport_error(&1, :econnrefused))
    logout_token = KeycloakHelper.sign_logout_token(KeycloakHelper.logout_token_claims())

    assert post_logout_token(conn, logout_token).status == 503
    assert get(authed, ~p"/service-permissions/gis-links").status == 200
  end

  test "a missing logout_token parameter is rejected", %{conn: conn} do
    response =
      conn
      |> put_req_header("content-type", "application/x-www-form-urlencoded")
      |> post(~p"/elixir/backchannel-logout", "")

    assert response.status == 400
  end

  # Keycloak posts server-to-server with no cookie and no CSRF token, so the
  # route must sit outside the :browser pipeline.
  test "the endpoint requires no CSRF token", %{conn: conn} do
    logout_token = KeycloakHelper.sign_logout_token(KeycloakHelper.logout_token_claims())

    refute post_logout_token(conn, logout_token).status == 403
  end
end
