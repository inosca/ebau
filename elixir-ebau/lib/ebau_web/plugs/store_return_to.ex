defmodule EbauWeb.Plugs.StoreReturnTo do
  @moduledoc """
  Remembers the current request path in the session as `:return_to` so that
  after authenticating the user lands back where they started instead of on
  `/`. `AuthController.success/4` reads this key.

  Only plain `GET` navigations are stored, and the auth routes themselves
  (`/elixir/...`) are skipped so they never clobber the remembered path.
  """

  @behaviour Plug

  import Plug.Conn

  @impl true
  def init(opts), do: opts

  @impl true
  def call(%Plug.Conn{method: "GET", request_path: path} = conn, _opts) do
    if store?(path), do: put_session(conn, :return_to, path), else: conn
  end

  def call(conn, _opts), do: conn

  defp store?("/elixir/" <> _), do: false
  defp store?(_), do: true
end
