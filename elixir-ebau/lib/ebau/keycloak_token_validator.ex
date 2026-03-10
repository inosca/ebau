defmodule Ebau.KeycloakTokenValidator do
  @moduledoc """
  Validates JWT access tokens issued by Keycloak.

  Uses Assent for JWKS fetching and JWT signature verification.
  HTTP responses are cached via `Ebau.Keycloak.CachingHTTPAdapter`.
  """

  alias Assent.HTTPAdapter.HTTPResponse

  @http_opts [http_adapter: Ebau.Keycloak.CachingHTTPAdapter]

  def validate_token(token) when is_binary(token) do
    with {:ok, header} <- Joken.peek_header(token),
         {:ok, key} <- fetch_key(header),
         {:ok, jwt} <- Assent.Strategy.verify_jwt(token, key, @http_opts),
         :ok <- validate_claims(jwt.claims) do
      {:ok, jwt.claims}
    else
      {:error, :key_not_found} ->
        Ebau.Keycloak.CachingHTTPAdapter.invalidate()

        with {:ok, header} <- Joken.peek_header(token),
             {:ok, key} <- fetch_key(header),
             {:ok, jwt} <- Assent.Strategy.verify_jwt(token, key, @http_opts),
             :ok <- validate_claims(jwt.claims) do
          {:ok, jwt.claims}
        end

      error ->
        error
    end
  end

  def validate_and_get_user(token) when is_binary(token) do
    with {:ok, claims} <- validate_token(token) do
      {:ok, claims, claims}
    end
  end

  defp fetch_key(%{"kid" => kid}) do
    base_url = base_url()

    with {:ok, jwks_uri} <- fetch_jwks_uri(base_url),
         {:ok, keys} <- fetch_jwks(jwks_uri) do
      case Enum.find(keys, &(&1["kid"] == kid)) do
        nil -> {:error, :key_not_found}
        key -> {:ok, key}
      end
    end
  end

  defp fetch_key(_header), do: {:error, "No kid in JWT header"}

  defp fetch_jwks_uri(base_url) do
    url = "#{base_url}/.well-known/openid-configuration"

    case Assent.Strategy.http_request(:get, url, nil, [], @http_opts) do
      {:ok, %HTTPResponse{status: 200, body: %{"jwks_uri" => jwks_uri}}} ->
        {:ok, jwks_uri}

      {:ok, %HTTPResponse{status: status}} ->
        {:error, "Failed to fetch OpenID configuration: HTTP #{status}"}

      {:error, reason} ->
        {:error, reason}
    end
  end

  defp fetch_jwks(jwks_uri) do
    case Assent.Strategy.http_request(:get, jwks_uri, nil, [], @http_opts) do
      {:ok, %HTTPResponse{status: 200, body: %{"keys" => keys}}} ->
        {:ok, keys}

      {:ok, %HTTPResponse{status: status}} ->
        {:error, "Failed to fetch JWKS: HTTP #{status}"}

      {:error, reason} ->
        {:error, reason}
    end
  end

  defp validate_claims(claims) do
    cond do
      !claims["exp"] || claims["exp"] < System.os_time(:second) ->
        {:error, "Token expired"}

      claims["iss"] != base_url() ->
        {:error, "Invalid issuer \"#{claims["iss"]}\""}

      claims["azp"] != client_id() ->
        {:error, "Invalid authorized party \"#{claims["azp"]}\""}

      true ->
        :ok
    end
  end

  defp base_url,
    do:
      Application.get_env(
        :ebau,
        :keycloak_base_url,
        "http://ebau-keycloak.localhost/auth/realms/ebau"
      )

  defp client_id, do: Application.get_env(:ebau, :keycloak_client_id, "camac")
end
