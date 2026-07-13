# Common UI Patterns

## Cards in a Grid

Display a collection of cards in a responsive grid layout.

```heex
<.uk_grid gap="medium" match>
  <div :for={item <- @items} class="uk-width-1-3@m">
    <.uk_card hover>
      <:header>
        <.uk_card_title>{item.title}</.uk_card_title>
      </:header>
      <:body>
        <p>{item.description}</p>
      </:body>
      <:footer class="uk-text-right">
        <.uk_button variant="primary" size="small" navigate={~p"/items/#{item}"}>
          View
        </.uk_button>
      </:footer>
    </.uk_card>
  </div>
</.uk_grid>
```

Key points:
- Use `match` on the grid so all cards have equal height.
- Width classes (`uk-width-1-3@m`) go on the grid children, not the cards.
- Use responsive suffixes (`@s`, `@m`, `@l`) for breakpoint-specific widths.

## Form with Validation

A complete form with real-time validation and submission.

```heex
<.uk_form for={@form} id="user-form" layout="stacked" phx-change="validate" phx-submit="save">
  <.uk_fieldset>
    <:legend>User Details</:legend>

    <.uk_input field={@form[:name]} required margin>
      <:label>Full Name <span class="uk-text-danger">*</span></:label>
    </.uk_input>

    <.uk_input field={@form[:email]} type="email" required margin>
      <:label>Email <span class="uk-text-danger">*</span></:label>
    </.uk_input>

    <.uk_input field={@form[:role]} type="select" margin
               options={["Admin": "admin", "Editor": "editor", "Viewer": "viewer"]}
               prompt="Select a role...">
      <:label>Role</:label>
    </.uk_input>

    <.uk_input field={@form[:bio]} type="textarea" rows="4" margin>
      <:label>Bio</:label>
    </.uk_input>

    <div class="uk-margin">
      <.uk_checkbox field={@form[:agree]}>
        <:label>I agree to the <a href="/terms">terms</a></:label>
      </.uk_checkbox>
    </div>
  </.uk_fieldset>

  <div class="uk-margin">
    <.uk_button variant="primary" type="submit">Save</.uk_button>
  </div>
</.uk_form>
```

Key points:
- Pass `margin` to `uk_input` when you want built-in `uk-margin` spacing without an extra wrapper.
- Wrap other controls such as `uk_checkbox` and action rows in `<div class="uk-margin">` for consistent spacing.
- Errors display automatically when the field has been touched (`used_input?` check).
- The `state` attr auto-sets to `"danger"` when errors are present.
- Labels are passed via the `<:label>` slot so you can embed arbitrary HTML (required markers, links, icons, etc.).

## Server-Controlled Modal

Open and close a modal from server-side logic.

```heex
<%!-- Trigger --%>
<.uk_button variant="primary" phx-click="open_delete_modal">Delete Item</.uk_button>

<%!-- Modal --%>
<.uk_modal id="delete-modal" show={@show_delete_modal} on_close="close_delete_modal">
  <:header>
    <.uk_modal_title>Confirm Deletion</.uk_modal_title>
  </:header>
  <:body>
    <p>Are you sure you want to delete <strong>{@item_name}</strong>?</p>
  </:body>
  <:footer class="uk-text-right">
    <.uk_button class="uk-modal-close" phx-click="close_delete_modal">Cancel</.uk_button>
    <.uk_button variant="danger" phx-click="delete_item">Delete</.uk_button>
  </:footer>
</.uk_modal>
```

```elixir
# In the LiveView
def handle_event("open_delete_modal", _, socket) do
  {:noreply, assign(socket, show_delete_modal: true)}
end

def handle_event("close_delete_modal", _, socket) do
  {:noreply, assign(socket, show_delete_modal: false)}
end

def handle_event("delete_item", _, socket) do
  # ... delete logic ...
  {:noreply, assign(socket, show_delete_modal: false)}
end
```

Key points:
- `show` controls visibility from the server. The Modal hook shows/hides accordingly.
- `on_close` fires when the user dismisses the modal via Esc or background click — use it to sync your assign back to `false`.
- `container` defaults to `false` — don't change this in LiveView.

## Tab Navigation

Tabs with server-synced active state.

```heex
<.uk_subnav id="settings-tabs" pill switcher="connect: #settings-content; animation: uk-animation-fade"
            active={@active_tab} on_change="change_tab">
  <:item href="#">General</:item>
  <:item href="#">Security</:item>
  <:item href="#">Notifications</:item>
</.uk_subnav>

<.uk_switcher id="settings-content">
  <li>
    <.uk_card>
      <:body>General settings content</:body>
    </.uk_card>
  </li>
  <li>
    <.uk_card>
      <:body>Security settings content</:body>
    </.uk_card>
  </li>
  <li>
    <.uk_card>
      <:body>Notification settings content</:body>
    </.uk_card>
  </li>
</.uk_switcher>
```

```elixir
def mount(_params, _session, socket) do
  {:ok, assign(socket, active_tab: 0)}
end

def handle_event("change_tab", %{"index" => index}, socket) do
  {:noreply, assign(socket, active_tab: index)}
end
```

Key points:
- The `switcher` attr on `uk_subnav` connects to the `uk_switcher` via `connect: #id`.
- `active` programmatically selects a tab; `on_change` reports user clicks.
- Both `uk_subnav` and `uk_switcher` require `id` attributes.

## Sortable List

Drag-and-drop reorderable list with server sync.

```heex
<.uk_sortable id="task-list" phx-hook="Sortable" data-event="reorder_tasks">
  <div :for={task <- @tasks} id={"task-#{task.id}"} class="uk-card uk-card-default uk-card-body uk-margin-small">
    <div class="uk-flex uk-flex-between uk-flex-middle">
      <span>{task.title}</span>
      <.uk_label variant={status_variant(task.status)}>{task.status}</.uk_label>
    </div>
  </div>
</.uk_sortable>
```

```elixir
def handle_event("reorder_tasks", %{"items" => ids}, socket) do
  # ids = ["task-3", "task-1", "task-2"]
  ordered_ids = Enum.map(ids, fn "task-" <> id -> String.to_integer(id) end)
  # Update positions in database...
  {:noreply, socket}
end
```

Key points:
- Every child must have a unique `id`.
- Use `data-event` to customize the event name (default: `"uikit:reorder"`).
- The payload `items` is a list of DOM IDs in the new order.

## Section + Container Layout

Standard page layout pattern.

```heex
<.uk_section variant="muted">
  <.uk_container size="large">
    <h1 class="uk-heading-small">Page Title</h1>
    <p class="uk-text-lead">Introductory text</p>
  </.uk_container>
</.uk_section>

<.uk_section>
  <.uk_container size="large">
    <%!-- Main content --%>
  </.uk_container>
</.uk_section>
```
