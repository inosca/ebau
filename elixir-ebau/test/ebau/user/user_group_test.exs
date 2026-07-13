defmodule Ebau.User.UserGroupTest do
  use Ebau.DataCase, async: true

  alias Ebau.Test.UserHelper

  setup do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    :ok
  end

  describe "set_default_user_group action" do
    test "flips default_group to 1 on target and clears siblings" do
      actor = UserHelper.create_actor!()
      user = Ash.load!(actor.user, [default_user_group: :group], actor: actor)

      second_group =
        Ebau.User.create_group!(
          %{users: [actor.user], role: %{slug: "municipality-admin"}},
          authorize?: false,
          load: [:user_group_for_user],
          actor: actor
        )

      assert actor.group.id == user.default_user_group.group.id

      Ebau.User.set_default_user_group!(second_group.user_group_for_user, actor: actor)
      user = Ash.load!(user, [:default_user_group], actor: actor)
      assert second_group.user_group_for_user.id == user.default_user_group.id
    end

    test "rejects setting default to a group the actor doesn't belong to" do
      owner_actor = UserHelper.create_actor!()
      owner_user = Ash.load!(owner_actor.user, :default_user_group, actor: owner_actor)
      stranger = UserHelper.create_actor!()

      assert_raise Ash.Error.Forbidden, fn ->
        Ebau.User.set_default_user_group!(owner_user.default_user_group, actor: stranger)
      end
    end
  end
end
