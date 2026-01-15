defmodule EbauWeb.PageController do
  use EbauWeb, :controller

  def home(conn, _params) do
    render(conn, :home)
  end
end
