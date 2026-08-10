defmodule EbauWeb.OAuth2 do
  @moduledoc """
  Keycloak bearer-token user lookup.

  This module resolves a bearer token via the configured Keycloak userinfo
  endpoint, extracts the configured username claim, and maps that claim to an
  existing [`Ebau.User.User`](./../../lib/ebau/user/user.ex)
  record.

  It reads the Keycloak settings from the `:ebau, :keycloak` application
  config and caches successful lookups through `EbauWeb.TokenCache`.
  """
  @behaviour EbauWeb.Behaviours.OAuth2

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

  @doc """
  Fetches the local user for a Keycloak bearer token.

  The token is sent to the Keycloak userinfo endpoint. The configured username
  claim is then used to look up the matching local user.
  """
  @impl EbauWeb.Behaviours.OAuth2
  def fetch_user(token) do
    EbauWeb.TokenCache.fetch(token, fn ->
      username_claim = Ebau.Secrets.keycloak_config() |> Keyword.get(:username_claim, "sub")

      with {:ok, userinfo} <- OAuth2.fetch_user(config(), %{"access_token" => token}),
           {:ok, username} <- Map.fetch(userinfo, username_claim) do
        Ebau.User.get_user_by_username(username, authorize?: false, actor: nil)
      else
        :error -> {:error, {:missing_claim, username_claim}}
        {:error, _reason} = error -> error
      end
    end)
  end
end
