defmodule EbauWeb.OAuth2 do
  @moduledoc """
  Keycloak bearer-token user lookup.

  This module resolves a bearer token via the configured Keycloak userinfo
  endpoint, extracts the configured email claim, and maps that claim to an
  existing [`Ebau.User.User`](./../../lib/ebau/user/user.ex)
  record.

  It reads the Keycloak settings from the `:ebau, :keycloak` application
  config and caches successful lookups through `EbauWeb.TokenCache`.
  """

  alias Assent.Strategy.OAuth2

  defp config do
    keycloak_config = Ebau.Secrets.keycloak_config()
    auth_url = Keyword.fetch!(keycloak_config, :url)
    realm = Keyword.fetch!(keycloak_config, :realm)

    [
      base_url: auth_url,
      user_url:
        String.trim_trailing(auth_url, "/") <> "/realms/#{realm}/protocol/openid-connect/userinfo"
    ]
  end

  @spec fetch_user(binary()) :: {:ok, Ebau.User.User.t()} | {:error, term()}
  @doc """
  Fetches the local user for a Keycloak bearer token.

  The token is sent to the Keycloak userinfo endpoint. The configured email
  claim is then used to look up the matching local user.
  """
  def fetch_user(token) do
    EbauWeb.TokenCache.fetch(token, fn ->
      email_claim = Ebau.Secrets.keycloak_config() |> Keyword.get(:email_claim, "email")

      with {:ok, userinfo} <- OAuth2.fetch_user(config(), %{"access_token" => token}),
           {:ok, email} <- Map.fetch(userinfo, email_claim) do
        Ebau.User.get_user_by_email(email, authorize?: false, actor: nil)
      else
        :error -> {:error, {:missing_claim, email_claim}}
        {:error, _reason} = error -> error
      end
    end)
  end
end
