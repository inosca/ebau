defmodule EbauWeb.GroupControllerTest do
  use EbauWeb.ConnCase, async: true

  alias Ebau.Test.UserHelper

  setup %{conn: conn} do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)

    actor = UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

    second_group =
      Ebau.User.create_group!(
        %{users: [actor.user], role: %{slug: "municipality-admin"}},
        authorize?: false,
        load: [:user_group_for_user],
        actor: actor
      )

    %{conn: log_in_actor(conn, actor), actor: actor, second_group: second_group}
  end

  describe "switch/2" do
    test "persists the picked group as default and redirects back", %{
      conn: conn,
      actor: actor,
      second_group: second_group
    } do
      conn =
        post(conn, ~p"/switch-group/#{second_group.id}", %{
          "return_to" => "/service-permissions/gis-links"
        })

      assert redirected_to(conn) == "/service-permissions/gis-links"
      assert conn.resp_cookies["camac_group"].value == Integer.to_string(second_group.id)

      user = Ash.load!(actor.user, :default_group, actor: actor)
      assert user.default_group.id == second_group.id
    end

    test "falls back to a safe path when return_to is missing", %{
      conn: conn,
      second_group: second_group
    } do
      conn = post(conn, ~p"/switch-group/#{second_group.id}", %{})

      assert redirected_to(conn) == "/"
    end

    test "rejects open-redirect return_to values", %{conn: conn, second_group: second_group} do
      conn = post(conn, ~p"/switch-group/#{second_group.id}", %{"return_to" => "//evil.com"})

      assert redirected_to(conn) == "/"
    end

    test "refuses to switch to a group the user does not belong to", %{conn: conn} do
      other_actor = UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})

      conn = post(conn, ~p"/switch-group/#{other_actor.group.id}", %{"return_to" => "/foo"})

      assert redirected_to(conn) == "/foo"
      refute Map.has_key?(conn.resp_cookies, "camac_group")
    end
  end
end
