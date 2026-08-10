defmodule EbauWeb.Components.Navbar do
  @moduledoc """
  Thin wrappers around UIkit's `uk-navbar-*` primitives.

  Holds no business logic — feed slots from the caller. Once the shape
  stabilises these can graduate into the `elixir_uikit` library.
  """

  use Phoenix.Component

  slot :left
  slot :right

  def navbar(assigns) do
    config = Application.get_env(:ebau, :watermark)

    assigns =
      assigns
      |> assign(:watermark_enabled?, Keyword.get(config, :enabled))
      |> assign(:watermark_text, Keyword.get(config, :text))

    ~H"""
    <script :type={Phoenix.LiveView.ColocatedHook} name=".NavbarSync">
      export default {
        mounted() { this.sync() },
        updated() { this.sync() },

        sync() {
          try {
            localStorage.setItem("ebau-navbar", this.el.outerHTML)
          } catch (_e) {}
        }
      }
    </script>
    <nav id="main-navbar" phx-hook=".NavbarSync" class="main-navigation uk-navbar-container">
      <.watermark text={@watermark_text} enabled?={@watermark_enabled?} />
      <div class="uk-padding-small uk-padding-remove-vertical">
        <div class="uk-navbar">
          <div :if={@left != []} class="uk-navbar-left uk-flex-nowrap">
            {render_slot(@left)}
          </div>
          <div :if={@right != []} class="uk-navbar-right">
            {render_slot(@right)}
          </div>
        </div>
      </div>
    </nav>
    """
  end

  attr :class, :string, default: nil
  slot :inner_block, required: true

  def navbar_nav(assigns) do
    ~H"""
    <ul class={["uk-navbar-nav", @class]}>
      {render_slot(@inner_block)}
    </ul>
    """
  end

  attr :resources, :list, required: true
  attr :current_path, :string, required: true

  def resource_navigation(assigns) do
    ~H"""
    <.navbar_nav class="uk-margin-right">
      <.navbar_item :for={resource <- @resources} current_path={@current_path} resource={resource}>
        <a href={resource.link}><span>{resource.name}</span></a>
      </.navbar_item>
    </.navbar_nav>
    """
  end

  attr :href, :string, default: "/"
  attr :src, :string, required: true
  attr :alt, :string, default: "Logo"

  def navbar_logo(assigns) do
    ~H"""
    <a class="uk-navbar-item uk-logo" href={@href}>
      <img alt={@alt} src={@src} />
    </a>
    """
  end

  attr :current_path, :string, default: ""
  attr :resource, Ebau.Core.Resource, default: nil
  attr :rest, :global
  slot :inner_block, required: true

  def navbar_item(assigns) do
    uri = URI.parse(assigns.current_path)

    active? =
      if assigns.resource do
        String.contains?(uri.path, assigns.resource.link)
      else
        false
      end

    assigns = assign(assigns, :active?, active?)

    ~H"""
    <li class={@active? && "uk-active"} {@rest}>
      {render_slot(@inner_block)}
    </li>
    """
  end

  slot :inner_block, required: true

  def navbar_subtitle(assigns) do
    ~H"""
    <div class="uk-navbar-subtitle">{render_slot(@inner_block)}</div>
    """
  end

  def drop_parent_icon(assigns) do
    ~H"""
    <span uk-drop-parent-icon=""></span>
    """
  end

  attr :text, :string
  attr :enabled?, :boolean
  attr :rest, :global

  def watermark(assigns) do
    ~H"""
    <header :if={@enabled?} class="watermark watermark--internal" {@rest}>
      {@text}
    </header>
    """
  end
end
