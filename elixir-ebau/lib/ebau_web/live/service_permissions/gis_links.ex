defmodule EbauWeb.Live.ServicePermissions.GisLinks do
  @moduledoc """
  LiveView twin of the ember service-permissions GIS links page.

  Lists the GIS link templates of the actor's service, supports live
  search by name, and lets service admins create and delete links.
  """

  use EbauWeb, :live_view

  @impl true
  def render(assigns) do
    ~H"""
    <Layouts.app flash={@flash} scope={@scope} resources={@resources} current_path={@current_path}>
      <.uk_container>
        <.uk_subnav id="service-permissions-tabs">
          <:item href="/service-permissions/permissions">{gettext("Permissions")}</:item>
          <:item href="/service-permissions/invitations">{gettext("Invitations")}</:item>
          <:item href="/service-permissions/organisation">{gettext("Master data")}</:item>
          <:item href="/service-permissions/sub-services">{gettext("Sub-services")}</:item>
          <:item href="/service-permissions/gis-links" active>{gettext("GIS links")}</:item>
        </.uk_subnav>

        <.uk_form
          :if={Ebau.Instances.can_create_gis_link?(@actor, reuse_values?: true)}
          for={@create_form}
          id="new-gis-link"
          class="uk-form-stacked"
          phx-submit="save"
        >
          <div class="uk-margin">
            <.uk_input field={@create_form[:name]}>
              <:label>{gettext("Name")}</:label>
            </.uk_input>
          </div>
          <div class="uk-margin">
            <.uk_input field={@create_form[:placeholder]} required>
              <:label>{gettext("Link")}</:label>
            </.uk_input>
          </div>
          <div class="uk-margin">
            <.uk_button variant="primary" type="submit">{gettext("Save")}</.uk_button>
          </div>
        </.uk_form>

        <form phx-change="search" id="search-form" class="uk-margin-large-top">
          <label for="gis-link-search" class="uk-hidden">{gettext("Search")}</label>
          <.uk_form_icon icon="search">
            <input
              id="gis-link-search"
              name="search"
              value={@search}
              class="uk-input"
              placeholder={gettext("Search")}
              type="search"
              phx-debounce="300"
            />
          </.uk_form_icon>
        </form>

        <.uk_table striped middle>
          <.uk_thead>
            <tr>
              <th>{gettext("Description")}</th>
              <th>{gettext("Link")}</th>
              <th></th>
            </tr>
          </.uk_thead>
          <.uk_tbody phx-update="stream" id="gis-links">
            <tr :for={{dom_id, gis_link} <- @streams.gis_links} id={dom_id}>
              <td>{gis_link.name}</td>
              <td>{gis_link.placeholder}</td>
              <td>
                <.uk_button
                  :if={Ebau.Instances.can_destroy_gis_link?(@actor, gis_link, reuse_values?: true)}
                  variant="link"
                  phx-click="delete"
                  phx-value-id={gis_link.id}
                >
                  <.uk_icon name="trash" />
                  <span class="uk-hidden">{gettext("Delete")}</span>
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
