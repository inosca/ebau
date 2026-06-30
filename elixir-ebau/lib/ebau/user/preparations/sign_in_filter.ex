defmodule Ebau.User.Preparations.SignInFilter do
  @moduledoc """
  Preparation for the `sign_in_with_ebau` action.

  Extracts the email value from the `user_info` OIDC claims map using the
  claim key configured via `DJANGO_OIDC_EMAIL_CLAIM` (default: `"email"`), then
  applies a filter so only the matching user record is returned.

  Two failure modes are handled explicitly:
  - Missing or non-string claim → auth error (prevents nil matching all null-email rows)
  - Nil / empty string → auth error (same protection)
  """

  use Ash.Resource.Preparation

  @impl true
  def prepare(query, _opts, _context) do
    email_claim =
      :ebau
      |> Application.get_env(:keycloak, [])
      |> Keyword.get(:email_claim, "email")

    user_info = Ash.Query.get_argument(query, :user_info) || %{}

    case Map.fetch(user_info, email_claim) do
      {:ok, email} when is_binary(email) and email != "" ->
        Ash.Query.filter(query, email == ^email)

      {:ok, _other} ->
        Ash.Query.add_error(
          query,
          Ash.Error.Query.InvalidArgument.exception(
            field: :user_info,
            message: "email claim #{inspect(email_claim)} is not a non-empty string"
          )
        )

      :error ->
        Ash.Query.add_error(
          query,
          Ash.Error.Query.InvalidArgument.exception(
            field: :user_info,
            message: "email claim #{inspect(email_claim)} is missing from user_info"
          )
        )
    end
  end
end
