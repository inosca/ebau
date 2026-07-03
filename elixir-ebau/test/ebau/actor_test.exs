defmodule Ebau.ActorTest do
  use Ebau.DataCase, async: true

  alias Ebau.Test.UserHelper

  setup do
    Ebau.User.create_role!(%{slug: "municipality-admin"}, authorize?: false, actor: nil)
    :ok
  end

  describe "build/2" do
    test "uses the persisted default group" do
      actor = UserHelper.create_actor!()

      assert {:ok, built} = Ebau.Actor.build(actor.user)
      assert built.group.id == actor.group.id
      assert built.service.id == actor.service.id
      assert built.role.id == actor.role.id
    end

    test "falls back to the first group when no default is set" do
      actor = UserHelper.create_actor!()
      user = Ash.load!(actor.user, :default_user_group, actor: actor)
      Ebau.User.clear_default_user_group!(user.default_user_group, actor: actor)

      assert {:ok, built} = Ebau.Actor.build(actor.user)
      assert built.group.id == actor.group.id
      assert built.service.id == actor.service.id
    end

    test "returns an error for a user without groups" do
      user =
        Ebau.User.create_user!(
          %{
            username: "groupless-#{System.unique_integer()}",
            name: "user",
            surname: "user",
            language: :de
          },
          authorize?: false,
          actor: nil
        )

      assert {:error, "user has no groups"} = Ebau.Actor.build(user)
    end

    test "returns an error for a nil user" do
      assert {:error, "user is nil"} = Ebau.Actor.build(nil)
    end
  end
end
