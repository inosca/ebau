defmodule EbauWeb.Mounts.CheckRoleTest do
  use EbauWeb.ConnCase, async: true

  setup do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    Ebau.User.create_role!(%{slug: "municipality"}, authorize?: false, actor: nil)

    admin_actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality-admin"}})
    regular_actor = Ebau.Test.UserHelper.create_actor!(%{role: %{slug: "municipality"}})

    %{admin_actor: admin_actor, regular_actor: regular_actor}
  end

  test ":admin check halts for regular users", %{regular_actor: regular_actor} do
    should_halt =
      EbauWeb.Mounts.CheckRole.on_mount(:admin, nil, nil, %Phoenix.LiveView.Socket{
        assigns: %{actor: regular_actor}
      })

    assert {:halt, _socket} = should_halt
  end

  test ":admin check continues for admin users", %{admin_actor: admin_actor} do
    should_continue =
      EbauWeb.Mounts.CheckRole.on_mount(:admin, nil, nil, %Phoenix.LiveView.Socket{
        assigns: %{actor: admin_actor}
      })

    assert {:cont, _socket} = should_continue
  end
end
