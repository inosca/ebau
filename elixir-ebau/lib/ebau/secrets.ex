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

    if key not in [:client_id, :base_url, :authorization_params, :redirect_uri] do
      raise ArgumentError, "unknown secret path: #{inspect(path)}"
    end

    {:ok, oauth2_secret(key)}
  end

  defp oauth2_secret(:client_id) do
    keycloak_config()
    |> Keyword.fetch!(:client_id)
  end

  defp oauth2_secret(:base_url) do
    keycloak_config = keycloak_config()

    "#{Keyword.fetch!(keycloak_config, :url)}realms/#{Keyword.fetch!(keycloak_config, :realm)}"
  end

  defp oauth2_secret(:authorization_params) do
    [scope: keycloak_config() |> Keyword.fetch!(:scopes)]
  end

  defp oauth2_secret(:redirect_uri) do
    Endpoint.url() <> "/auth"
  end

  defp keycloak_config, do: Application.fetch_env!(:ebau, :keycloak)
end
