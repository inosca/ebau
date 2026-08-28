defmodule EbauWeb.AuthControllerTest do
  use EbauWeb.ConnCase, async: true

  alias Ebau.Test.UserHelper

  setup %{conn: conn} do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    actor = UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    %{conn: log_in_actor(conn, actor), actor: actor}
  end

  describe "session revocation" do
    test "a revoked token stops authenticating the session", %{conn: conn} do
      assert get(conn, ~p"/service-permissions/gis-links").status == 200

      token = Plug.Conn.get_session(conn, "user_token")
      {:ok, %{"jti" => jti, "sub" => subject}} = AshAuthentication.Jwt.peek(token)

      :ok =
        AshAuthentication.TokenResource.Actions.revoke_jti(
          Ebau.User.Token,
          jti,
          subject
        )

      assert redirected_to(get(conn, ~p"/service-permissions/gis-links")) ==
               ~p"/elixir/sign-in"
    end
  end

  describe "sign_out/2" do
    test "sends the id_token as id_token_hint so Keycloak skips its confirmation screen", %{
      conn: conn
    } do
      Ebau.Test.KeycloakHelper.attach_session(conn, %{
        sid: "sid-for-hint",
        id_token: "the.id.token"
      })

      params =
        conn
        |> get(~p"/elixir/sign-out")
        |> redirected_to(302)
        |> URI.parse()
        |> Map.get(:query)
        |> URI.decode_query()

      assert params["id_token_hint"] == "the.id.token"
      assert params["post_logout_redirect_uri"] =~ "/elixir/sign-in"
      refute Map.has_key?(params, "client_id")
    end

    # `clear_session/2` turns the token row into a revocation record that is
    # never expunged, so the 1-2KB id_token must not ride along on it.
    test "drops the id_token from the row it revokes", %{conn: conn} do
      Ebau.Test.KeycloakHelper.attach_session(conn, %{sid: "sid", id_token: "the.id.token"})

      get(conn, ~p"/elixir/sign-out")

      assert [%{purpose: "revocation", extra_data: nil}] =
               Ash.read!(Ebau.User.Token, authorize?: false, actor: nil)
    end

    test "redirects to Keycloak's end-session endpoint", %{conn: conn} do
      uri = conn |> get(~p"/elixir/sign-out") |> redirected_to(302) |> URI.parse()
      params = URI.decode_query(uri.query || "")

      assert String.ends_with?(uri.path, "/protocol/openid-connect/logout")
      assert params["post_logout_redirect_uri"] =~ "/elixir/sign-in"
    end

    # Clearing the cookie is not enough on its own: a copy taken before
    # sign-out must stop authenticating too, which only revocation achieves.
    test "revokes the session so a captured cookie no longer authenticates", %{conn: conn} do
      captured = conn

      assert get(captured, ~p"/service-permissions/gis-links").status == 200

      _signed_out = get(conn, ~p"/elixir/sign-out")

      assert redirected_to(get(captured, ~p"/service-permissions/gis-links")) ==
               ~p"/elixir/sign-in"
    end

    test "falls back to client_id when no id_token was received", %{conn: conn} do
      params =
        conn
        |> get(~p"/elixir/sign-out")
        |> redirected_to(302)
        |> URI.parse()
        |> Map.get(:query)
        |> URI.decode_query()

      assert params["client_id"] == "camac"
      refute Map.has_key?(params, "id_token_hint")
    end
  end
end
