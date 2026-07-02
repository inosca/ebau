defmodule EbauWeb.Plugs.KeycloakBearerAuthTest do
  use EbauWeb.ConnCase, async: true

  alias EbauWeb.Plugs.KeycloakBearerAuth

  @moduletag capture_log: true

  describe "call/2" do
    test "returns 401 when no authorization header is present", %{conn: conn} do
      conn = KeycloakBearerAuth.call(conn, [])

      assert conn.halted
      assert conn.status == 401
    end

    test "returns 401 when authorization header is invalid", %{conn: conn} do
      conn =
        conn
        |> put_req_header("authorization", "Bearer invalid-token")
        |> put_req_header("x-camac-group", "1")
        |> KeycloakBearerAuth.call([])

      assert conn.halted
      assert conn.status == 401
    end

    test "returns 401 when x-camac-group header is missing", %{conn: conn} do
      conn =
        conn
        |> put_req_header("authorization", "Bearer some-token")
        |> KeycloakBearerAuth.call([])

      assert conn.halted
      assert conn.status == 401
    end

    test "sets actor on conn when authentication succeeds", %{conn: conn} do
      Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
      actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

      conn = authenticated_rest_api_conn(conn, actor)
      conn = KeycloakBearerAuth.call(conn, [])

      refute conn.halted
      assert %Ebau.Actor{} = Ash.PlugHelpers.get_actor(conn)
    end
  end
end
