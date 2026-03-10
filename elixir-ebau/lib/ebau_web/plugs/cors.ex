defmodule EbauWeb.Plugs.CORS do
  @moduledoc """
  Simple CORS plug that allows all origins.
  """

  @behaviour Plug

  @impl true
  def init(opts), do: opts

  @impl true
  def call(conn, _opts) do
    conn
    |> Plug.Conn.put_resp_header("access-control-allow-origin", "*")
    |> Plug.Conn.put_resp_header(
      "access-control-allow-methods",
      "GET, POST, PATCH, PUT, DELETE, OPTIONS"
    )
    |> Plug.Conn.put_resp_header("access-control-allow-headers", "*")
    |> Plug.Conn.put_resp_header("access-control-max-age", "86400")
    |> maybe_preflight()
  end

  defp maybe_preflight(%{method: "OPTIONS"} = conn) do
    conn
    |> Plug.Conn.send_resp(204, "")
    |> Plug.Conn.halt()
  end

  defp maybe_preflight(conn), do: conn
end
