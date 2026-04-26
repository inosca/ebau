defmodule EbauWeb.LiveTest do
  use EbauWeb, :live_view

  @impl true
  def render(assigns) do
    ~H"""
    <h1>asdfasdf</h1>
    """
  end

  @impl true
  def mount(_, _, socket) do
    {:ok, socket}
  end
end
