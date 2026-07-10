defmodule EbauWeb.Layouts do
  @moduledoc """
  This module holds layouts and related functionality
  used by your application.
  """
  use EbauWeb, :html

  # Embed all files in layouts/* within this module.
  # The default root.html.heex file contains the HTML
  # skeleton of your application, namely HTML headers
  # and other static content.
  embed_templates "layouts/*"

  def user_display_name(%{user: %{name: name, surname: surname}}), do: "#{name} #{surname}"

  # The demo canton has no logo asset of its own yet.
  defp logo_src do
    case Application.get_env(:ebau, :canton) do
      :demo -> "/assets/images/ebau-so-logo.svg"
      canton -> "/assets/images/ebau-#{canton}-logo.svg"
    end
  end

  @doc """
  Renders your app layout: UIkit navbar (logo, resource navigation,
  group switcher, sign-out), main content, and flash messages.

  ## Examples

      <Layouts.app flash={@flash} scope={@scope} resources={@resources} current_path={@current_path}>
        <h1>Content</h1>
      </Layouts.app>

  """
  attr :flash, :map, required: true, doc: "the map of flash messages"
  attr :scope, :any, required: true
  attr :resources, :list, default: []
  attr :current_path, :string, default: "/"
  slot :inner_block, required: true

  def app(assigns) do
    ~H"""
    <.navbar>
      <:left>
        <.navbar_logo src={logo_src()} alt="eBau by inosca Logo" />
        <.resource_navigation resources={@resources} current_path={@current_path} />
      </:left>
      <:right>
        <.navbar_nav>
          <.navbar_item :if={@scope.actor}>
            <.group_dropdown scope={@scope} current_path={@current_path} />
          </.navbar_item>
          <.navbar_item>
            <.language_switcher current_path={@current_path} />
          </.navbar_item>
          <.navbar_item>
            <a href={~p"/sign-out"} title={gettext("Sign out")}>
              <span uk-icon="icon: sign-out"></span>
              <span class="uk-hidden">{gettext("Sign out")}</span>
            </a>
          </.navbar_item>
        </.navbar_nav>
      </:right>
    </.navbar>

    <main class="main-content">
      {render_slot(@inner_block)}
    </main>

    <.flash_group flash={@flash} />
    """
  end

  @doc """
  Shows the flash group with standard titles and content.

  ## Examples

      <.flash_group flash={@flash} />
  """
  attr :flash, :map, required: true, doc: "the map of flash messages"
  attr :id, :string, default: "flash-group", doc: "the optional id of flash container"

  def flash_group(assigns) do
    ~H"""
    <div id={@id} aria-live="polite">
      <.flash kind={:info} flash={@flash} />
      <.flash kind={:error} flash={@flash} />

      <.flash
        id="client-error"
        kind={:error}
        title={gettext("We can't find the internet")}
        phx-disconnected={show(".phx-client-error #client-error") |> JS.remove_attribute("hidden")}
        phx-connected={hide("#client-error") |> JS.set_attribute({"hidden", ""})}
        hidden
      >
        {gettext("Attempting to reconnect")}
        <.icon name="hero-arrow-path" class="ml-1 size-3 motion-safe:animate-spin" />
      </.flash>

      <.flash
        id="server-error"
        kind={:error}
        title={gettext("Something went wrong!")}
        phx-disconnected={show(".phx-server-error #server-error") |> JS.remove_attribute("hidden")}
        phx-connected={hide("#server-error") |> JS.set_attribute({"hidden", ""})}
        hidden
      >
        {gettext("Attempting to reconnect")}
        <.icon name="hero-arrow-path" class="ml-1 size-3 motion-safe:animate-spin" />
      </.flash>
    </div>
    """
  end

  defp group_dropdown(assigns) do
    ~H"""
    <a href="#">
      <div>
        <span class="uk-text-bold">
          {user_display_name(@scope.actor)}
        </span>
        <.navbar_subtitle>{@scope.actor.group.name}</.navbar_subtitle>
      </div>
      <.drop_parent_icon />
    </a>
    <.uk_dropdown
      id="group-dropdown"
      animation="uk-animation-slide-top-small"
      duration={300}
      mode="click"
      pos="bottom-right"
      offset={-10}
    >
      <ul class="uk-nav uk-dropdown-nav">
        <li :for={group <- @scope.actor.user.groups}>
          <.form for={%{}} action={~p"/switch-group/#{group.id}"} method="post">
            <input type="hidden" name="return_to" value={@current_path} />
            <.uk_button
              type="submit"
              variant="link"
              class={[
                "uk-button uk-button-link",
                @scope.actor.group.id == group.id && "active-group"
              ]}
            >
              {group.name}
            </.uk_button>
          </.form>
        </li>
      </ul>
    </.uk_dropdown>
    """
  end

  defp language_switcher(assigns) do
    current_language = Gettext.get_locale(EbauWeb.Gettext)
    supported_langauges = EbauWeb.Gettext.supported_languages()
    dbg(Gettext.get_locale(EbauWeb.Gettext))

    assigns =
      assign(assigns,
        current_language: current_language,
        supported_languages: supported_langauges
      )

    ~H"""
    <%= if Enum.count(@supported_languages) > 1 do %>
      <a href="#" role="button">
        <span :if={@current_language === "de"}>{gettext("German")}</span>
        <span :if={@current_language === "fr"}>{gettext("French")}</span>
        <span :if={@current_language === "it"}>{gettext("Italian")}</span>
        <.drop_parent_icon />
      </a>
      <.uk_dropdown
        id="locale-dropdown"
        animation="uk-animation-slide-top-small"
        duration={300}
        mode="click"
        pos="bottom-right"
        offset={-10}
      >
        <ul class="uk-nav uk-dropdown-nav">
          <li :for={language <- @supported_languages}>
            <.form for={%{}} action={~p"/switch-language/#{language}"} method="post">
              <input type="hidden" name="return_to" value={@current_path} />
              <.uk_button
                type="submit"
                variant="link"
                class="uk-button uk-button-link"
              >
                <span :if={language === "de"}>{gettext("German")}</span>
                <span :if={language === "fr"}>{gettext("French")}</span>
                <span :if={language === "it"}>{gettext("Italian")}</span>
              </.uk_button>
            </.form>
          </li>
        </ul>
      </.uk_dropdown>
    <% end %>
    """
  end
end
