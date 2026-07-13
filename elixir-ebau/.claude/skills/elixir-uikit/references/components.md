# Component API Reference

**Important:** These components replace the default Phoenix `CoreComponents` (`button`, `modal`, `input`, `table`, etc.) which depend on Tailwind CSS. Do NOT use `CoreComponents` or Tailwind/DaisyUI classes — use `elixir_uikit` components and `uk-*` utility classes instead.

## UI Components (`Uikit.Components`)

### `uk_button`

Renders a UIkit button. Automatically renders as a `<.link>` when `href`, `navigate`, or `patch` is provided.

```heex
<.uk_button>Default</.uk_button>
<.uk_button variant="primary">Primary</.uk_button>
<.uk_button variant="danger" size="small">Delete</.uk_button>
<.uk_button navigate={~p"/users"}>Go to Users</.uk_button>
<.uk_button uk_toggle="target: #my-modal">Open Modal</.uk_button>
```

**Attrs:** `variant` (`default|primary|secondary|danger|text|link`), `size` (`small|large`), `type` (default `"button"`), `uk_toggle`, `disabled`, `class`. Global attrs include `href`, `navigate`, `patch`, `method`, `download`.

### `uk_badge`

```heex
<.uk_badge>5</.uk_badge>
```

**Attrs:** `class`. Slot: `inner_block`.

### `uk_card`

Cards with optional header, body, and footer slots.

```heex
<.uk_card variant="default" hover>
  <:header>
    <.uk_card_title>Title</.uk_card_title>
  </:header>
  <:body>Content here</:body>
  <:footer class="uk-text-right">
    <.uk_button variant="primary">Save</.uk_button>
  </:footer>
</.uk_card>
```

**Attrs:** `variant` (`default|primary|secondary`), `size` (`small|large`), `hover`, `class`.
**Slots:** `header`, `body`, `footer` (accepts `class`), `close`, `inner_block`.

### `uk_card_title`

Renders an `<h3>` with `uk-card-title` class.

```heex
<.uk_card_title>My Card</.uk_card_title>
```

### `uk_container`

Constrains content width and centers it.

```heex
<.uk_container size="small">
  Narrow content
</.uk_container>
```

**Attrs:** `size` (`xsmall|small|large|xlarge|expand`), `class`.

### `uk_section`

Creates horizontal layout blocks with background variants.

```heex
<.uk_section variant="muted" size="small">
  <.uk_container>Section content</.uk_container>
</.uk_section>
```

**Attrs:** `variant` (`default|muted|primary|secondary`), `size` (`xsmall|small|large|xlarge|remove-vertical`), `class`.

### `uk_grid`

Responsive grid layout. Children are grid cells — use `uk-width-*` classes on children for sizing.

```heex
<.uk_grid gap="small" match>
  <div class="uk-width-1-3">Column 1</div>
  <div class="uk-width-2-3">Column 2</div>
</.uk_grid>
```

**Attrs:** `gap` (`small|medium|large|collapse`), `divider`, `match`, `masonry` (`pack|next|true`), `class`.

### `uk_sortable`

Drag-and-drop reorderable container. **Every child must have a unique `id`.**

```heex
<.uk_sortable id="my-list" phx-hook="Sortable">
  <div :for={item <- @items} id={"item-#{item.id}"}>
    {item.name}
  </div>
</.uk_sortable>
```

**Attrs:** `id` (required), `group`, `handle`, `grid`, `animation`, `threshold`, `cls_custom`, `class`.

### `uk_icon`

Renders a UIkit SVG icon. Becomes a link when `href`/`navigate`/`patch` is set, or a button with `button={true}`.

```heex
<.uk_icon name="check" />
<.uk_icon name="heart" ratio={2} />
<.uk_icon name="settings" button navigate={~p"/settings"} />
```

**Attrs:** `name` (required), `ratio` (default 1), `id`, `button`, `class`. Global attrs include `href`, `navigate`, `patch`.

### `uk_modal`

Modal dialog. Use `show` + `on_close` for server-controlled visibility, or `uk_toggle` on a button for client-side toggling.

```heex
<%!-- Client-side toggle --%>
<.uk_button uk_toggle="target: #confirm-modal">Open</.uk_button>
<.uk_modal id="confirm-modal">
  <:header><.uk_modal_title>Confirm</.uk_modal_title></:header>
  <:body><p>Are you sure?</p></:body>
  <:footer class="uk-text-right">
    <.uk_button class="uk-modal-close">Cancel</.uk_button>
    <.uk_button variant="primary" phx-click="confirm">Yes</.uk_button>
  </:footer>
</.uk_modal>

<%!-- Server-controlled --%>
<.uk_modal id="server-modal" show={@show_modal} on_close="close_modal">
  <:body>Controlled by the server</:body>
</.uk_modal>
```

**Attrs:** `id` (required), `center`, `container` (default `false`), `full`, `esc_close`, `bg_close`, `stack`, `show`, `on_close`, `class`, `dialog_class`.
**Slots:** `header`, `body`, `footer` (accepts `class`), `close`, `inner_block`.

**Important:** `container` defaults to `false` so the modal stays in the LiveView DOM tree. Do not set `container: true` in LiveView.

### `uk_modal_title`

Renders an `<h2>` with `uk-modal-title` class.

### `uk_label`

Status/category indicator.

```heex
<.uk_label variant="success">Active</.uk_label>
<.uk_label variant="danger">Expired</.uk_label>
```

**Attrs:** `variant` (`success|warning|danger`), `class`.

### `uk_spinner`

Loading indicator.

```heex
<.uk_spinner />
<.uk_spinner ratio={2} />
```

**Attrs:** `ratio` (default 1), `id`, `class`.

### `uk_subnav`

Sub-navigation, optionally as a tab switcher. **`id` is required.**

```heex
<.uk_subnav id="tabs" pill switcher="connect: #tab-content">
  <:item href="#">Tab 1</:item>
  <:item href="#">Tab 2</:item>
</.uk_subnav>
```

**Attrs:** `id` (required), `divider`, `pill`, `switcher`, `active` (integer index), `on_change`, `class`.
**Slot `item`:** `href`, `active`, `disabled`, `class`, `id`.

### `uk_switcher`

Content container connected to a subnav switcher.

```heex
<.uk_switcher id="tab-content">
  <li>Content for tab 1</li>
  <li>Content for tab 2</li>
</.uk_switcher>
```

**Attrs:** `id` (required), `animation`, `class`.

### `uk_dropdown`

Toggleable overlay triggered by an adjacent element. Wrap both the toggle and dropdown in a `uk-inline` container.

```heex
<%!-- Simple content dropdown --%>
<div class="uk-inline">
  <.uk_button>Hover</.uk_button>
  <.uk_dropdown id="my-dropdown">
    <p>Dropdown content</p>
  </.uk_dropdown>
</div>

<%!-- Click-triggered with positioning --%>
<div class="uk-inline">
  <.uk_button>Click Me</.uk_button>
  <.uk_dropdown id="click-dropdown" mode="click" pos="top-center">
    <p>Click-triggered dropdown</p>
  </.uk_dropdown>
</div>

<%!-- Navigation dropdown --%>
<div class="uk-inline">
  <.uk_button>Menu</.uk_button>
  <.uk_dropdown id="nav-dropdown">
    <:nav>
      <li class="uk-active"><a href="/dashboard">Dashboard</a></li>
      <li><a href="/settings">Settings</a></li>
      <li class="uk-nav-header">More</li>
      <li class="uk-nav-divider"></li>
      <li><a href="/logout">Logout</a></li>
    </:nav>
  </.uk_dropdown>
</div>
```

**Attrs:** `id` (required), `mode` (`click|hover|click, hover`), `pos` (e.g. `bottom-left`, `top-center`, `right-top`), `offset`, `delay_show`, `delay_hide`, `stretch` (`true|x|y`), `animation`, `animate_out`, `duration`, `flip`, `shift`, `auto_update`, `close_on_scroll`, `large`, `class`.
**Slots:** `nav` (accepts `class` — place `<li>` elements inside for a `uk-dropdown-nav` list), `inner_block`.

### `uk_alert`

Displays feedback messages with optional close button and style variants.

```heex
<.uk_alert>Default alert.</.uk_alert>
<.uk_alert variant="success" closable>Operation completed.</.uk_alert>
<.uk_alert variant="danger" closable>
  <h3>Error</h3>
  <p>Something went wrong.</p>
</.uk_alert>
```

**Attrs:** `variant` (`primary|success|warning|danger`), `closable`, `animation` (default true), `duration` (default 150), `class`.

### `uk_comment`

Displays user-generated content with avatar, author info, and body. Use `primary` for highlighted comments (e.g. admin responses).

```heex
<.uk_comment id="comment-1">
  <:avatar src="/images/avatar.jpg" width="80" height="80" alt="Author" />
  <:title>Author Name</:title>
  <:meta>12 days ago</:meta>
  <:meta><a href="#">Reply</a></:meta>
  <:body><p>Comment text goes here.</p></:body>
</.uk_comment>

<.uk_comment id="comment-admin" primary>
  <:avatar src="/images/admin.jpg" width="80" height="80" alt="Admin" />
  <:title>Admin</:title>
  <:meta>Just now</:meta>
  <:body><p>Highlighted admin response.</p></:body>
</.uk_comment>
```

**Attrs:** `id`, `primary`, `class`.
**Slots:** `avatar` (has `src` required, `width`, `height`, `alt`), `title`, `meta` (multiple allowed), `body`, `inner_block`.

### `uk_comment_list`

Threaded comment layout. Wrap comments in `<li>` elements; nest a `<ul>` inside an `<li>` for replies.

```heex
<.uk_comment_list>
  <li>
    <.uk_comment id="comment-1">
      <:avatar src="/images/user1.jpg" width="80" height="80" alt="User 1" />
      <:title>User 1</:title>
      <:meta>12 days ago</:meta>
      <:body><p>Top-level comment.</p></:body>
    </.uk_comment>
    <ul>
      <li>
        <.uk_comment id="comment-1-1">
          <:avatar src="/images/user2.jpg" width="80" height="80" alt="User 2" />
          <:title>User 2</:title>
          <:meta>6 days ago</:meta>
          <:body><p>A nested reply.</p></:body>
        </.uk_comment>
      </li>
    </ul>
  </li>
</.uk_comment_list>
```

**Attrs:** `class`.

---

## Form Components (`Uikit.FormComponents`)

### `uk_form`

Wraps Phoenix `<.form>` with UIkit layout classes.

```heex
<.uk_form for={@form} id="user-form" layout="stacked" phx-change="validate" phx-submit="save">
  ...
</.uk_form>
```

**Attrs:** `for` (required), `id` (required), `layout` (`stacked|horizontal`), `class`. Global attrs include `phx-change`, `phx-submit`, `action`, `method`.

### `uk_input`

Universal input component. Renders `<input>`, `<select>`, or `<textarea>` based on `type`. Automatically extracts errors from the form field.

Labels are passed via the `<:label>` slot, which accepts arbitrary HEEx (required markers, icons, links, etc.). Omit the slot to render the input without a label.
Pass `margin` to add UIkit's default `uk-margin` spacing to the generated wrapper for non-hidden inputs.

```heex
<.uk_input field={@form[:name]}>
  <:label>Full Name</:label>
</.uk_input>

<.uk_input field={@form[:email]} type="email" size="large" margin>
  <:label>Email <span class="uk-text-danger">*</span></:label>
</.uk_input>

<.uk_input field={@form[:bio]} type="textarea" rows="4">
  <:label>Bio</:label>
</.uk_input>

<.uk_input field={@form[:role]} type="select"
           options={["Admin": "admin", "User": "user"]} prompt="Select...">
  <:label>Role</:label>
</.uk_input>
```

**Attrs:** `field`, `type` (default `"text"`), `id`, `name`, `value`, `errors`, `size` (`small|large`), `width` (`xsmall|small|medium|large`), `state` (`danger|success`), `blank`, `margin`, `class`. For select: `options`, `prompt`, `multiple`. Global attrs include `placeholder`, `required`, `disabled`, `readonly`, `min`, `max`, `step`, `rows`, `cols`, `pattern`, `maxlength`, `minlength`.
**Slots:** `label` (HEEx-capable label content).

### `uk_checkbox`

Checkbox with hidden false-value field for LiveView forms. Label goes in the `<:label>` slot.

```heex
<.uk_checkbox field={@form[:agree]}>
  <:label>I agree to the <a href="/terms">terms</a></:label>
</.uk_checkbox>
```

**Attrs:** `field`, `id`, `name`, `value` (default `"true"`), `checked`, `errors`, `state`, `class`. Global: `disabled`, `required`.
**Slots:** `label`.

### `uk_radio`

Radio input. Use multiple with the same field/name for a group. Label goes in the `<:label>` slot.

```heex
<.uk_radio field={@form[:role]} value="admin">
  <:label>Admin</:label>
</.uk_radio>
<.uk_radio field={@form[:role]} value="user">
  <:label>User</:label>
</.uk_radio>
```

**Attrs:** `field`, `id`, `name`, `value` (required), `checked`, `state`, `class`. Global: `disabled`, `required`.
**Slots:** `label`.

### `uk_range`

Range slider input. Label goes in the `<:label>` slot.

```heex
<.uk_range field={@form[:volume]} min="0" max="100" step="1">
  <:label>Volume</:label>
</.uk_range>
```

**Attrs:** `field`, `id`, `name`, `value`, `errors`, `class`. Global: `min`, `max`, `step`, `disabled`, `required`.
**Slots:** `label`.

### `uk_fieldset`

Groups form fields with an optional legend.

```heex
<.uk_fieldset>
  <:legend>Account Details</:legend>
  <.uk_input field={@form[:email]} type="email" label="Email" />
</.uk_fieldset>
```

**Attrs:** `class`. **Slots:** `legend`, `inner_block`.

### `uk_form_label`

Standalone form label.

```heex
<.uk_form_label for="user-email">Email</.uk_form_label>
```

**Attrs:** `for`, `class`.

### `uk_form_controls`

Wrapper for form controls, useful in horizontal layouts.

```heex
<.uk_form_controls text>
  <.uk_checkbox name="agree" label="I agree" />
</.uk_form_controls>
```

**Attrs:** `text` (for checkbox/radio alignment in horizontal forms), `class`.

### `uk_form_icon`

Positions an icon inside an input. Wrap around a raw `<input>` element.

```heex
<.uk_form_label for="search">Search</.uk_form_label>
<.uk_form_icon icon="search" flip>
  <input class="uk-input" type="search" id="search" name="search" />
</.uk_form_icon>
```

**Attrs:** `icon` (required), `flip`, `clickable`, `class`. Global: `href`, `navigate`, `patch`, `phx-click`.
