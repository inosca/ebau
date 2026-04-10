defmodule EbauWeb.TokenCache do
  @moduledoc """
  ETS-based cache for validated bearer tokens. Without this, every API
  request triggers an HTTP round-trip to Keycloak's userinfo endpoint.
  Cached entries expire based on the token's `exp` claim, with a
  periodic sweep every 5 minutes.
  """

  use GenServer

  @table :token_cache
  @cleanup_interval :timer.minutes(5)

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

  defp token_exp(token) do
    case JOSE.JWT.peek_payload(token) do
      %JOSE.JWT{fields: %{"exp" => exp}} when is_integer(exp) -> exp
      _ -> System.system_time(:second) + 300
    end
  end
end
