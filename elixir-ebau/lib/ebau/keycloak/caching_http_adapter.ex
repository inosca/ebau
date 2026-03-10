defmodule Ebau.Keycloak.CachingHTTPAdapter do
  @moduledoc """
  Caching HTTP adapter for Assent that stores GET responses in ETS.

  Used to avoid fetching the OpenID configuration and JWKS on every
  token validation request.
  """

  @behaviour Assent.HTTPAdapter

  @table __MODULE__
  @cache_ttl :timer.minutes(60)

  def create_table do
    :ets.new(@table, [:set, :public, :named_table, read_concurrency: true])
    :ok
  end

  def invalidate do
    :ets.delete_all_objects(@table)
    :ok
  end

  @impl true
  def request(:get, url, body, headers, opts) do
    now = System.monotonic_time(:millisecond)

    case :ets.lookup(@table, url) do
      [{_, response, cached_at}] when now - cached_at < @cache_ttl ->
        {:ok, response}

      _ ->
        case Assent.HTTPAdapter.Req.request(:get, url, body, headers, opts) do
          {:ok, response} ->
            :ets.insert(@table, {url, response, now})
            {:ok, response}

          error ->
            error
        end
    end
  end

  def request(method, url, body, headers, opts) do
    Assent.HTTPAdapter.Req.request(method, url, body, headers, opts)
  end
end
