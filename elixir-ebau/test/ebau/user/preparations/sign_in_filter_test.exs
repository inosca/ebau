defmodule Ebau.User.Preparations.SignInFilterTest do
  @moduledoc """
  Sign-in resolves a user by the OIDC username claim, matching Django's
  `_get_existing_user/1`. `USER.EMAIL` has no unique constraint and in kt_so a
  token-exchange user and an internal user legitimately share one address, so
  email cannot identify a user.
  """
  use Ebau.DataCase, async: false

  alias Ebau.User.Preparations.SignInFilter

  defp seed_user(username, email) do
    Ash.Seed.seed!(Ebau.User.User, %{
      username: username,
      name: "test",
      surname: "user",
      language: :de,
      email: email
    })
  end

  defp prepared(user_info) do
    Ebau.User.User
    |> Ash.Query.new()
    |> Ash.Query.set_argument(:user_info, user_info)
    |> SignInFilter.prepare([], %{})
  end

  defp sign_in_candidates(user_info), do: user_info |> prepared() |> Ash.read!(authorize?: false)

  test "resolves the internal user when a token exchange user shares the email" do
    internal = seed_user("462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")
    seed_user("egov:462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")

    assert [%{id: id}] = sign_in_candidates(%{"sub" => internal.username})
    assert id == internal.id
  end

  test "resolves the token exchange user by its prefixed username" do
    seed_user("462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")
    egov = seed_user("egov:462afaba-aeb7-494a-8596-3497b81ed701", "shared@example.com")

    assert [%{id: id}] = sign_in_candidates(%{"sub" => egov.username})
    assert id == egov.id
  end

  test "resolves nothing for an unknown username" do
    seed_user("known-user", "known@example.com")

    assert [] == sign_in_candidates(%{"sub" => "stranger"})
  end

  test "ignores email entirely, even when it matches another user" do
    seed_user("some-other-sub", "known@example.com")

    assert [] == sign_in_candidates(%{"sub" => "stranger", "email" => "known@example.com"})
  end

  test "errors when the username claim is missing" do
    refute prepared(%{"email" => "no-sub@example.com"}).valid?
  end

  test "errors when the username claim is not a non-empty string" do
    refute prepared(%{"sub" => ""}).valid?
  end
end
