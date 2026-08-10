defmodule EbauWeb.Components.NavbarTest do
  use ExUnit.Case, async: true

  import Phoenix.Component
  import Phoenix.LiveViewTest

  alias EbauWeb.Components.Navbar

  defp render_watermark(text, enabled?) do
    render_component(&Navbar.watermark/1, text: text, enabled?: enabled?)
  end

  test "renders nothing when disabled" do
    refute render_watermark("dev", false) =~ "dev"
  end

  test "renders the configured label when enabled" do
    html = render_watermark("staging", true)

    assert html =~ "staging"
    assert html =~ ~s(class="watermark watermark--internal")
  end
end
