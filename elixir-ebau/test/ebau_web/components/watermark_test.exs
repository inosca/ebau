defmodule EbauWeb.Components.WatermarkTest do
  use ExUnit.Case, async: false

  import Phoenix.Component
  import Phoenix.LiveViewTest

  alias EbauWeb.Components.Watermark

  setup do
    original = Application.get_env(:ebau, :watermark)
    on_exit(fn -> Application.put_env(:ebau, :watermark, original) end)
    :ok
  end

  defp render_watermark do
    assigns = %{}
    rendered_to_string(~H"<Watermark.watermark />")
  end

  test "renders nothing when disabled" do
    Application.put_env(:ebau, :watermark, enabled: false, text: "dev")

    refute render_watermark() =~ "watermark"
  end

  test "renders nothing when unconfigured" do
    Application.delete_env(:ebau, :watermark)

    refute render_watermark() =~ "watermark"
  end

  test "renders the configured label when enabled" do
    Application.put_env(:ebau, :watermark, enabled: true, text: "staging")

    html = render_watermark()

    assert html =~ "staging"
    assert html =~ ~s(class="watermark watermark--internal")
  end

  test "falls back to \"dev\" when no label is configured" do
    Application.put_env(:ebau, :watermark, enabled: true)

    assert render_watermark() =~ "dev"
  end
end
