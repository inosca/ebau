defmodule EbauWeb.Components.Watermark do
  @moduledoc """
  Diagonal environment banner across the top-left corner of the navbar, marking
  a non-production deployment.

  Port of `ember-ebau-core/addon/components/watermark.{js,hbs}`.
  """

  use Phoenix.Component

  attr :rest, :global

  def watermark(assigns) do
    config = Application.get_env(:ebau, :watermark, [])

    assigns =
      assigns
      |> assign(:enabled?, Keyword.get(config, :enabled, false))
      |> assign(:text, Keyword.get(config, :text, "dev"))

    ~H"""
    <header :if={@enabled?} class="watermark watermark--internal" {@rest}>
      {@text}
    </header>
    """
  end
end
