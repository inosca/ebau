defmodule Ebau.User.UserLookupTest do
  @moduledoc """
  Users are resolved by username, never by email.

  `USER.EMAIL` carries no unique constraint and duplicates are legitimate — a
  token-exchange user (username prefixed `egov:`) shares an address with its
  internal user. Both authentication paths depend on this: `EbauWeb.OAuth2`
  for bearer tokens and `Ebau.User.Preparations.SignInFilter` for OIDC sign-in.
  """
  use Ebau.DataCase, async: false

  defp seed_user(username, email) do
    Ash.Seed.seed!(Ebau.User.User, %{
      username: username,
      name: "test",
      surname: "user",
      language: :de,
      email: email
    })
  end

  test "resolves a user by username when another user shares the email" do
    internal = seed_user("462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")
    egov = seed_user("egov:462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")

    assert {:ok, found} =
             Ebau.User.get_user_by_username(internal.username, authorize?: false, actor: nil)

    assert found.id == internal.id

    assert {:ok, found_egov} =
             Ebau.User.get_user_by_username(egov.username, authorize?: false, actor: nil)

    assert found_egov.id == egov.id
  end

  test "an email lookup on the same data fails, which is why username is used" do
    seed_user("462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")
    seed_user("egov:462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")

    assert {:error, %Ash.Error.Invalid{errors: [%Ash.Error.Invalid.MultipleResults{}]}} =
             Ebau.User.get_user_by_email("shared@example.com", authorize?: false, actor: nil)
  end

  test "resolves nothing for an unknown username" do
    seed_user("known-user", "known@example.com")

    assert {:error, %Ash.Error.Invalid{errors: [%Ash.Error.Query.NotFound{}]}} =
             Ebau.User.get_user_by_username("stranger", authorize?: false, actor: nil)
  end
end
