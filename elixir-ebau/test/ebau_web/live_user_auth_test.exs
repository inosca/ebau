defmodule EbauWeb.LiveUserAuthTest do
  use EbauWeb.ConnCase, async: true

  import Phoenix.LiveViewTest

  setup %{conn: conn} do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    %{conn: log_in_actor(conn, actor)}
  end

  # The mount check cannot see a revocation that happens while the socket is
  # already connected, so without the broadcast an open tab stays fully
  # interactive after a back-channel logout until the user navigates.
  test "a connected LiveView is redirected when its session is revoked", %{conn: conn} do
    {:ok, view, _html} = live(conn, ~p"/service-permissions/gis-links")

    {:ok, %{"jti" => jti}} =
      conn |> Plug.Conn.get_session("user_token") |> AshAuthentication.Jwt.peek()

    EbauWeb.SessionRevocation.broadcast(jti)

    assert_redirect(view, ~p"/elixir/sign-in")
  end

  test "a connected LiveView is untouched by another session's revocation", %{conn: conn} do
    {:ok, view, _html} = live(conn, ~p"/service-permissions/gis-links")

    EbauWeb.SessionRevocation.broadcast("some-other-jti")

    refute_redirected(view, ~p"/elixir/sign-in")
  end
end
