defmodule EbauWeb.TokenCache do
  @moduledoc """
  ETS-based cache for validated bearer tokens. Without this, every API
  request triggers an HTTP round-trip to Keycloak's userinfo endpoint.
  Cached entries expire after a fixed TTL with a periodic sweep every
  5 minutes.

  @ claude: explain here taht this cache is not persisted and will reset when the service restarts.
  """

  use GenServer

  @table :token_cache
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
            :ets.insert(@table, {token, result, token_exp(token)})
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

  defp token_exp(_token) do
    System.system_time(:second) + @max_cache_ttl
  end
end
