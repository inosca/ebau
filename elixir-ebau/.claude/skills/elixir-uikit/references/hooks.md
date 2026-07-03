# LiveView Hooks

`elixir_uikit` exports three LiveView hooks (**Sortable**, **Modal**, **Switcher**) and a `dom` callback (`onBeforeElUpdated`). These are automatically registered when you run `mix uikit.setup`.

```javascript
import UikitHooks, { onBeforeElUpdated } from "elixir_uikit"

let liveSocket = new LiveSocket("/live", Socket, {
  hooks: UikitHooks,
  dom: { onBeforeElUpdated }
})
```

The `onBeforeElUpdated` callback preserves UIkit's runtime DOM state (icon SVGs, runtime classes, dropdown open state/positioning) across LiveView patches. Without it, morphdom strips UIkit's injected content on every server update.

## Sortable Hook

Enables drag-and-drop reordering with server-side sync.

### Setup

```heex
<.uk_sortable id="my-list" phx-hook="Sortable" data-event="reorder_items">
  <div :for={item <- @items} id={"item-#{item.id}"} class="uk-card uk-card-default uk-card-body">
    {item.name}
  </div>
</.uk_sortable>
```

### Event

When items are reordered, the hook pushes an event to the server with the new order of element IDs.

- **Default event name:** `"uikit:reorder"`
- **Custom event name:** Set `data-event` on the container
- **Payload:** `%{"items" => ["item-3", "item-1", "item-2"]}`

### Server handler

```elixir
def handle_event("reorder_items", %{"items" => ids}, socket) do
  # ids is a list of DOM element IDs in the new order
  # Extract your record IDs and update positions
  {:noreply, socket}
end
```

### Requirements

- The container **must** have an `id` and `phx-hook="Sortable"`.
- **Every child element must have a unique `id`** — otherwise LiveView cannot track reordered items.

---

## Modal Hook

Enables server-controlled modal show/hide via assigns.

### Setup

The hook is automatically attached when you use `show` on `uk_modal`:

```heex
<.uk_modal id="my-modal" show={@show_modal} on_close="modal_closed">
  <:header><.uk_modal_title>Title</.uk_modal_title></:header>
  <:body><p>Content</p></:body>
</.uk_modal>
```

### How it works

- Set `show={true}` to open the modal, `show={false}` to close it.
- When the user dismisses the modal (Esc key or background click), the hook pushes the `on_close` event (default: `"uikit:modal_closed"`) so you can sync state.
- **Payload:** `%{"id" => "my-modal"}`

### Server handler

```elixir
def handle_event("modal_closed", %{"id" => _id}, socket) do
  {:noreply, assign(socket, show_modal: false)}
end
```

### Client-side only alternative

If you don't need server control, skip `show` and use `uk_toggle` on a button:

```heex
<.uk_button uk_toggle="target: #my-modal">Open</.uk_button>
<.uk_modal id="my-modal">
  <:body>Content</:body>
</.uk_modal>
```

---

## `onBeforeElUpdated` DOM Callback

The exported `onBeforeElUpdated` function handles three things that hooks cannot do cleanly:

### Icons

UIkit injects SVGs into icon elements. Morphdom would strip them on every patch because the server HTML has no children. The callback copies the SVG from the current DOM into the incoming DOM before the patch, so it's never lost. When the `uk-icon` attribute changes (new icon name), it lets morphdom clear the old SVG and schedules a UIkit re-render after the patch.

No `id` or `phx-update="ignore"` needed — icons can be changed dynamically from server assigns.

### Runtime Classes

UIkit's JS adds classes at runtime (e.g. the `uk-icon` class on `uk-icon` and `uk-close` elements). Morphdom strips these on every patch. On icon elements (any attribute in the SVG list above), the callback copies the current DOM's classes into the incoming DOM so the icon styling survives.

### Dropdowns

UIkit adds `uk-open` class and inline positioning styles when a dropdown is shown. The callback copies these from the current DOM into the incoming DOM, so open dropdowns stay open through patches. No per-element hook needed — UIkit auto-initializes elements with the `uk-dropdown` attribute.

The `uk_dropdown` component still requires a stable `id` because UIkit manipulates the dropdown's DOM structure.

---

## Switcher Hook

Enables server-controlled tab switching via assigns.

### Setup

The hook is automatically attached when you use `active` on `uk_subnav`:

```heex
<.uk_subnav id="my-tabs" pill switcher="connect: #my-content" active={@active_tab} on_change="tab_changed">
  <:item href="#">Tab 1</:item>
  <:item href="#">Tab 2</:item>
  <:item href="#">Tab 3</:item>
</.uk_subnav>

<.uk_switcher id="my-content">
  <li>Content 1</li>
  <li>Content 2</li>
  <li>Content 3</li>
</.uk_switcher>
```

### How it works

- Set `active={0}`, `active={1}`, etc. to programmatically switch tabs.
- When the user clicks a tab, the hook pushes the `on_change` event (default: `"uikit:switcher_changed"`) with the new index.
- **Payload:** `%{"id" => "my-tabs", "index" => 1}`

### Server handler

```elixir
def handle_event("tab_changed", %{"index" => index}, socket) do
  {:noreply, assign(socket, active_tab: index)}
end
```

### Client-side only alternative

If you don't need server-side tab state, omit `active` and `on_change`:

```heex
<.uk_subnav id="tabs" pill switcher="connect: #content">
  <:item href="#">Tab 1</:item>
  <:item href="#">Tab 2</:item>
</.uk_subnav>

<.uk_switcher id="content">
  <li>Content 1</li>
  <li>Content 2</li>
</.uk_switcher>
```
