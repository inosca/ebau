defmodule EbauWeb.Live.ServicePermissions.GisLinks do
  @moduledoc """
  LiveView twin of the ember service-permissions GIS links page.

  Lists the GIS link templates of the actor's service, supports live
  search by name, and lets service admins create and delete links.
  """

  use EbauWeb, :live_view

  on_mount {EbauWeb.Mounts.CheckRole, :admin}

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} scope={@scope} resources={@resources} current_path={@current_path}>
      <.uk_container>
        <%!-- TODO: replace with a uk_tab component once elixir_uikit provides one --%>
        <ul class="uk-tab">
          <li>
            <a href="/service-permissions/permissions">{dgettext("instances", "Permissions")}</a>
          </li>
          <li>
            <a href="/service-permissions/invitations">{dgettext("instances", "Invitations")}</a>
          </li>
          <li>
            <a href="/service-permissions/organisation">{dgettext("instances", "Master data")}</a>
          </li>
          <li>
            <a href="/service-permissions/sub-services">{dgettext("instances", "Sub-services")}</a>
          </li>
          <li class="uk-active">
            <.link navigate={~p"/service-permissions/gis-links"}>
              {dgettext("instances", "GIS links")}
            </.link>
          </li>
        </ul>

        <.uk_form
          :if={Ebau.Instances.can_create_gis_link?(@actor, reuse_values?: true)}
          for={@create_form}
          id="new-gis-link"
          class="uk-form-stacked"
          phx-submit="save"
        >
          <div class="uk-margin">
            <.uk_input field={@create_form[:name]} required>
              <:label>
                {dgettext("instances", "Name")}
                <span class="mandatory-asterisk">*</span>
              </:label>
            </.uk_input>
          </div>
          <div class="uk-margin">
            <.uk_input field={@create_form[:placeholder]} required>
              <:label>
                {dgettext("instances", "Link")}
                <span class="mandatory-asterisk">*</span>
              </:label>
            </.uk_input>
          </div>
          <div class="uk-margin">
            <.uk_button variant="primary" type="submit">{dgettext("instances", "Save")}</.uk_button>
          </div>
        </.uk_form>

        <hr />

        <form phx-change="search" id="search-form">
          <label for="gis-link-search" class="uk-hidden">{dgettext("instances", "Search")}</label>
          <.uk_form_icon icon="search" wrapper_class="uk-width-1-1">
            <input
              id="gis-link-search"
              name="search"
              value={@search}
              class="uk-input"
              placeholder={dgettext("instances", "Search")}
              type="search"
              phx-debounce="300"
            />
          </.uk_form_icon>
        </form>

        <.uk_table striped middle>
          <.uk_thead>
            <tr>
              <th class="uk-width-1-5">{dgettext("instances", "Description")}</th>
              <th>{dgettext("instances", "Link")}</th>
              <th></th>
            </tr>
          </.uk_thead>
          <.uk_tbody phx-update="stream" id="gis-links">
            <tr id="gis-links-empty" class="empty-row">
              <td class="uk-text-center uk-text-italic" colspan="3">
                {dgettext("instances", "No entries found")}
              </td>
            </tr>
            <tr :for={{dom_id, gis_link} <- @streams.gis_links} id={dom_id}>
              <td>{gis_link.name}</td>
              <td>
                <a href={gis_link.placeholder} target="_blank" rel="noopener noreferrer">
                  {gis_link.placeholder}
                </a>
              </td>
              <td class="uk-text-right">
                <.uk_button
                  :if={Ebau.Instances.can_destroy_gis_link?(@actor, gis_link, reuse_values?: true)}
                  variant="link"
                  phx-click="delete"
                  phx-value-id={gis_link.id}
                >
                  <.uk_icon name="trash" />
                  <span class="uk-hidden">{dgettext("instances", "Delete")}</span>
                </.uk_button>
              </td>
            </tr>
          </.uk_tbody>
        </.uk_table>
      </.uk_container>
    </Layouts.app>
    """
  end

  @impl true
  def mount(_params, _session, socket) do
    socket =
      socket
      |> assign(:search, "")
      |> stream_gis_links()
      |> assign_create_form()

    {:ok, socket}
  end

  @impl true
  def handle_event("save", %{"form" => form}, socket) do
    case AshPhoenix.Form.submit(socket.assigns.create_form,
           params: form,
           scope: socket.assigns.scope
         ) do
      {:ok, _gis_link} ->
        socket =
          socket
          |> push_event("reset-form", %{id: "new-gis-link"})
          |> assign_create_form()
          |> stream_gis_links()

        {:noreply, socket}

      {:error, form} ->
        {:noreply, assign(socket, :create_form, form)}
    end
  end

  @impl true
  def handle_event("delete", %{"id" => id}, socket) do
    case Ebau.Instances.destroy_gis_link(id, scope: socket.assigns.scope, return_destroyed?: true) do
      {:ok, destroyed_gis_link} ->
        {:noreply, stream_delete(socket, :gis_links, destroyed_gis_link)}

      {:error, _} ->
        {:noreply, socket}
    end
  end

  @impl true
  def handle_event("search", %{"search" => ""}, socket) do
    {:noreply, socket |> assign(:search, "") |> stream_gis_links()}
  end

  @impl true
  def handle_event("search", %{"search" => search}, socket) do
    case Ebau.Instances.search_gis_link(search, scope: socket.assigns.scope) do
      {:ok, links} ->
        {:noreply, socket |> assign(:search, search) |> stream(:gis_links, links, reset: true)}

      {:error, _} ->
        {:noreply, socket}
    end
  end

  defp assign_create_form(socket) do
    assign(
      socket,
      :create_form,
      Ebau.Instances.form_to_create_gis_link(scope: socket.assigns.scope) |> to_form()
    )
  end

  defp stream_gis_links(socket) do
    stream(
      socket,
      :gis_links,
      Ebau.Instances.read_gis_links!(nil, scope: socket.assigns.scope),
      reset: true
    )
  end
end
