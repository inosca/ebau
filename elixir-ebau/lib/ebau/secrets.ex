defmodule Ebau.Secrets do
  @moduledoc """
  Resolves secrets for AshAuthentication (OIDC and token signing).

  Maps secret paths to values from application config (`:ebau, :keycloak`).
  """

  use AshAuthentication.Secret

  alias EbauWeb.Endpoint

  def secret_for([:authentication, :tokens, :signing_secret], Ebau.User.User, _opts, _context) do
    Application.fetch_env(:ebau, :token_signing_secret)
  end

  def secret_for(path, Ebau.User.User, _opts, _context) do
    key = List.last(path)

    if key not in [:client_id, :client_secret, :base_url, :authorization_params, :redirect_uri] do
      raise ArgumentError, "unknown secret path: #{inspect(path)}"
    end

    {:ok, oauth2_secret(key)}
  end

  defp oauth2_secret(:client_id) do
    keycloak_config()
    |> Keyword.fetch!(:client_id)
  end

  defp oauth2_secret(:client_secret) do
    keycloak_config()
    |> Keyword.fetch!(:client_secret)
  end

  defp oauth2_secret(:base_url) do
    keycloak_config = keycloak_config()

    realm = Keyword.fetch!(keycloak_config, :realm)
    url = Keyword.fetch!(keycloak_config, :url)
    String.trim_trailing(url, "/") <> "/realms/#{realm}"
  end

  defp oauth2_secret(:authorization_params) do
    [scope: keycloak_config() |> Keyword.fetch!(:scopes)]
  end

  defp oauth2_secret(:redirect_uri) do
    url_path =
      case get_in(Application.get_env(:ebau, EbauWeb.Endpoint, []), [:url, :path]) do
        nil -> ""
        "/" -> ""
        path -> String.trim_trailing(path, "/")
      end

    Endpoint.url() <> url_path <> "/elixir/auth"
  end

  @doc """
  The issuer Keycloak stamps on tokens for the configured realm.
  """
  @spec issuer() :: String.t()
  def issuer, do: oauth2_secret(:base_url)

  @doc """
  The Keycloak client both this app and the Ember app authenticate through.
  """
  @spec client_id() :: String.t()
  def client_id, do: oauth2_secret(:client_id)

  @doc """
  Keycloak's RP-initiated logout endpoint.
  """
  @spec end_session_url() :: String.t()
  def end_session_url, do: issuer() <> "/protocol/openid-connect/logout"

  @doc """
  Keycloak's JWKS endpoint, used to verify back-channel logout tokens.
  """
  @spec jwks_url() :: String.t()
  def jwks_url, do: issuer() <> "/protocol/openid-connect/certs"

  def keycloak_config, do: Application.fetch_env!(:ebau, :keycloak)
end
