defmodule Ebau.User.Preparations.SignInFilter do
  @moduledoc """
  Preparation for the `sign_in_with_ebau` action.

  Extracts the username value from the `user_info` OIDC claims map using the
  claim key configured via `OIDC_USERNAME_CLAIM` (default: `"sub"`), then
  applies a filter so only the matching user record is returned.

  Username is the key Django matches on. `_get_existing_user/1` in
  `django/camac/user/authentication.py:135` looks the user up by username.
  These implementations must be kept in sync.

  Django's `OIDC_BOOTSTRAP_BY_EMAIL_FALLBACK` is not implemented here.
  It defaults to `false` and only kt_uri enables it. So if another canton
  turns it on or uri runs elixir, this needs to be implemented.

  Two failure modes are handled explicitly:
  - Missing or non-string claim → auth error (prevents nil matching all null-username rows)
  - Nil / empty string → auth error (same protection)
  """

  use Ash.Resource.Preparation

  @impl true
  def prepare(query, _opts, _context) do
    username_claim =
      :ebau
      |> Application.get_env(:keycloak, [])
      |> Keyword.get(:username_claim, "sub")

    user_info = Ash.Query.get_argument(query, :user_info) || %{}

    case Map.fetch(user_info, username_claim) do
      {:ok, username} when is_binary(username) and username != "" ->
        Ash.Query.filter(query, username == ^username)

      {:ok, _other} ->
        Ash.Query.add_error(
          query,
          Ash.Error.Query.InvalidArgument.exception(
            field: :user_info,
            message: "username claim #{inspect(username_claim)} is not a non-empty string"
          )
        )

      :error ->
        Ash.Query.add_error(
          query,
          Ash.Error.Query.InvalidArgument.exception(
            field: :user_info,
            message: "username claim #{inspect(username_claim)} is missing from user_info"
          )
        )
    end
  end
end
