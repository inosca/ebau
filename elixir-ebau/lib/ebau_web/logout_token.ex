defmodule EbauWeb.LogoutToken do
  @moduledoc """
  Verifies OIDC back-channel logout tokens issued by Keycloak.

  Implements the validation rules from OpenID Connect Back-Channel Logout 1.0.
  `Assent.Strategy.OIDC.validate_id_token/2` cannot be reused: it requires an
  `exp` claim, which logout tokens do not carry.
  """

  require Logger

  @logout_event "http://schemas.openid.net/event/backchannel-logout"
  @request_timeout to_timeout(second: 5)

  # Logout tokens carry no `exp`, so freshness comes from `iat`. Tolerated in
  # both directions to allow for clock skew between Keycloak and this host.
  @clock_skew_tolerance div(to_timeout(minute: 2), 1000)

  @type session :: %{sid: String.t() | nil, sub: String.t() | nil}
  @type error ::
          :malformed
          | :unknown_kid
          | :jwks_unavailable
          | :invalid_signature
          | :invalid_issuer
          | :invalid_audience
          | :invalid_authorized_party
          | :not_a_logout_token
          | :nonce_present
          | :stale
          | :expired
          | :no_subject_or_sid

  @doc """
  Verifies a logout token and returns the session it identifies.
  """
  @spec verify(String.t() | nil) :: {:ok, session()} | {:error, error()}
  def verify(token) when is_binary(token) do
    with {:ok, kid} <- peek_kid(token),
         {:ok, jwk} <- fetch_key(kid),
         {:ok, claims} <- verify_signature(token, jwk),
         :ok <- validate_issuer(claims),
         :ok <- validate_audience(claims),
         :ok <- validate_authorized_party(claims),
         :ok <- validate_events(claims),
         :ok <- validate_nonce_absent(claims),
         :ok <- validate_freshness(claims),
         :ok <- validate_not_expired(claims) do
      identify(claims)
    end
  end

  def verify(_token), do: {:error, :malformed}

  defp peek_kid(token) do
    case Joken.peek_header(token) do
      {:ok, header} -> {:ok, Map.get(header, "kid")}
      {:error, _reason} -> {:error, :malformed}
    end
  end

  # Fetched from Keycloak on every logout token rather than cached. Logouts
  # are rare and Keycloak is on the same infrastructure, so one extra GET per
  # logout costs less than a cache that can go stale across a key rotation.
  # Verification cannot start before this, so nothing reaches Keycloak for a
  # request that is not even JWT-shaped.
  #
  # `:keycloak_jwks_req` lets tests route the request through `Req.Test`.
  defp fetch_key(kid) do
    options =
      Keyword.merge(
        [retry: false, receive_timeout: @request_timeout],
        Application.get_env(:ebau, :keycloak_jwks_req, [])
      )

    case Req.get(Ebau.Secrets.jwks_url(), options) do
      {:ok, %Req.Response{status: 200, body: %{"keys" => keys}}} ->
        find_key(keys, kid)

      other ->
        Logger.warning("Could not fetch Keycloak JWKS: #{inspect(other)}")
        {:error, :jwks_unavailable}
    end
  end

  defp find_key([key], nil), do: {:ok, key}

  defp find_key(keys, kid) do
    case Enum.find(keys, &(&1["kid"] == kid)) do
      nil -> {:error, :unknown_kid}
      key -> {:ok, key}
    end
  end

  defp verify_signature(token, jwk) do
    case JOSE.JWT.verify_strict(JOSE.JWK.from_map(jwk), ["RS256"], token) do
      {true, %JOSE.JWT{fields: claims}, _jws} -> {:ok, claims}
      _ -> {:error, :invalid_signature}
    end
  end

  defp validate_issuer(%{"iss" => iss}) do
    if iss == Ebau.Secrets.issuer(), do: :ok, else: {:error, :invalid_issuer}
  end

  defp validate_issuer(_claims), do: {:error, :invalid_issuer}

  defp validate_audience(%{"aud" => aud}) do
    if Ebau.Secrets.client_id() in List.wrap(aud), do: :ok, else: {:error, :invalid_audience}
  end

  defp validate_audience(_claims), do: {:error, :invalid_audience}

  # Only meaningful for a multi-valued `aud`, but the spec requires it whenever
  # the claim is present.
  defp validate_authorized_party(%{"azp" => azp}) do
    if azp == Ebau.Secrets.client_id(), do: :ok, else: {:error, :invalid_authorized_party}
  end

  defp validate_authorized_party(_claims), do: :ok

  # The event value must be a JSON object. This is the claim that stops an ID
  # or access token for the same client being replayed here as a logout token.
  defp validate_events(%{"events" => %{@logout_event => value}}) when is_map(value), do: :ok
  defp validate_events(_claims), do: {:error, :not_a_logout_token}

  # A logout token must not carry a nonce; one that does is a replayed ID
  # token rather than a logout notification.
  defp validate_nonce_absent(claims) do
    if Map.has_key?(claims, "nonce"), do: {:error, :nonce_present}, else: :ok
  end

  defp validate_freshness(%{"iat" => iat}) when is_integer(iat) do
    if abs(System.system_time(:second) - iat) <= @clock_skew_tolerance do
      :ok
    else
      {:error, :stale}
    end
  end

  defp validate_freshness(_claims), do: {:error, :stale}

  # Optional for logout tokens, but honoured when Keycloak sends it.
  defp validate_not_expired(%{"exp" => exp}) when is_integer(exp) do
    if System.system_time(:second) - exp <= @clock_skew_tolerance do
      :ok
    else
      {:error, :expired}
    end
  end

  defp validate_not_expired(_claims), do: :ok

  # No `jti` replay cache on purpose. The spec suggests one, but revocation is
  # idempotent, so replaying a token within the freshness window only re-revokes
  # an already-revoked session. A cache would add a failure mode worse than the
  # thing it prevents: if it were unavailable, real logouts would be rejected.

  defp identify(%{"sid" => sid} = claims) when is_binary(sid),
    do: {:ok, %{sid: sid, sub: Map.get(claims, "sub")}}

  defp identify(%{"sub" => sub}) when is_binary(sub), do: {:ok, %{sid: nil, sub: sub}}
  defp identify(_claims), do: {:error, :no_subject_or_sid}
end
