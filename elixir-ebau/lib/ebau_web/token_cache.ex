defmodule EbauWeb.TokenCache do
  @moduledoc """
  ETS-based cache for validated bearer tokens. Without this, every API
  request triggers an HTTP round-trip to Keycloak's userinfo endpoint.
  Cached entries expire after a fixed TTL with a periodic sweep every
  5 minutes.

  The cache is in-memory and will be lost on service restart.
  """

  use GenServer

  @table :token_cache
  # TODO Cached tokens are valid for 5 minutes even if revoked.
  # This is known and also implemented the same way in django.
  @cleanup_interval to_timeout(minute: 5)
  @max_cache_ttl 300

  def start_link(_), do: GenServer.start_link(__MODULE__, [], name: __MODULE__)

  @impl true
  def init(_) do
    :ets.new(@table, [:named_table, :public, read_concurrency: true])
    schedule_cleanup()
    {:ok, []}
  end

  def fetch(token, fallback) do
    now = System.system_time(:second)

    case :ets.lookup(@table, token) do
      [{_, result, exp}] when exp > now ->
        result

      _ ->
        case fallback.() do
          {:ok, _} = result ->
            :ets.insert(@table, {token, result, cache_expiry()})
            result

          other ->
            other
        end
    end
  end

  @impl true
  def handle_info(:cleanup, state) do
    now = System.system_time(:second)
    :ets.select_delete(@table, [{{:_, :_, :"$1"}, [{:<, :"$1", now}], [true]}])
    schedule_cleanup()
    {:noreply, state}
  end

  defp schedule_cleanup, do: Process.send_after(self(), :cleanup, @cleanup_interval)

  defp cache_expiry do
    System.system_time(:second) + @max_cache_ttl
  end
end
