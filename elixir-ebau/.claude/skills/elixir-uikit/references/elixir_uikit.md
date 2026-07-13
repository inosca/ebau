# elixir_uikit — Usage Rules

`elixir_uikit` provides [UIkit 3](https://getuikit.com/) components and LiveView hooks for Phoenix applications. Use these components instead of writing raw UIkit HTML.

## Setup

Run `mix uikit.setup` to configure your project automatically (imports, hooks, CSS).

## Component Quick Reference

### UI Components (`Uikit.Components`)

| Component | Key Attrs | Slots |
|---|---|---|
| `uk_button` | `variant` (`default\|primary\|secondary\|danger\|text\|link`), `size` (`small\|large`), `type`, `disabled`, `uk_toggle` | `inner_block` |
| `uk_badge` | `class` | `inner_block` |
| `uk_card` | `variant` (`default\|primary\|secondary`), `size` (`small\|large`), `hover` | `header`, `body`, `footer` (has `class`), `close`, `inner_block` |
| `uk_card_title` | `class` | `inner_block` |
| `uk_container` | `size` (`xsmall\|small\|large\|xlarge\|expand`) | `inner_block` |
| `uk_section` | `variant` (`default\|muted\|primary\|secondary`), `size` (`xsmall\|small\|large\|xlarge\|remove-vertical`) | `inner_block` |
| `uk_grid` | `gap` (`small\|medium\|large\|collapse`), `divider`, `match`, `masonry` | `inner_block` |
| `uk_sortable` | `id` (required), `group`, `handle`, `grid`, `animation`, `threshold`, `cls_custom` | `inner_block` |
| `uk_icon` | `name` (required), `ratio`, `button` | — |
| `uk_modal` | `id` (required), `center`, `container` (default `false`), `full`, `esc_close`, `bg_close`, `stack`, `show`, `on_close` | `header`, `body`, `footer` (has `class`), `close`, `inner_block` |
| `uk_modal_title` | `class` | `inner_block` |
| `uk_label` | `variant` (`success\|warning\|danger`) | `inner_block` |
| `uk_spinner` | `ratio` | — |
| `uk_subnav` | `id` (required), `divider`, `pill`, `switcher`, `active`, `on_change` | `item` (has `href`, `active`, `disabled`, `class`) |
| `uk_switcher` | `id` (required), `animation` | `inner_block` |
| `uk_comment` | `id`, `primary` | `avatar` (has `src`, `width`, `height`, `alt`), `title`, `meta`, `body`, `inner_block` |
| `uk_comment_list` | `class` | `inner_block` |

### Form Components (`Uikit.FormComponents`)

| Component | Key Attrs | Slots |
|---|---|---|
| `uk_form` | `for` (required), `id` (required), `layout` (`stacked\|horizontal`) | `inner_block` |
| `uk_input` | `field`, `type` (text/email/select/textarea/etc.), `size`, `width`, `state`, `blank`, `margin`, `options`, `prompt`, `multiple` | `label` |
| `uk_checkbox` | `field`, `value`, `checked`, `state` | `label` |
| `uk_radio` | `field`, `value` (required), `checked`, `state` | `label` |
| `uk_range` | `field`, `value` | `label` |
| `uk_fieldset` | `class` | `legend`, `inner_block` |
| `uk_form_label` | `for`, `class` | `inner_block` |
| `uk_form_controls` | `text` | `inner_block` |
| `uk_form_icon` | `icon` (required), `flip`, `clickable` | `inner_block` |

## LiveView Hooks

Three hooks are exported from `elixir_uikit`: **Sortable**, **Modal**, **Switcher**. See [usage-rules/hooks.md](usage-rules/hooks.md) for details.

## Common Patterns

See [usage-rules/patterns.md](usage-rules/patterns.md) for cards in grids, forms with validation, server-controlled modals, and tab navigation.

## UIkit CSS Utilities

See [usage-rules/css-utilities.md](usage-rules/css-utilities.md) for `uk-*` utility classes (layout, text, spacing, visibility, flex).

## Agent Skills Configuration

If your project uses the [`usage_rules`](https://hex.pm/packages/usage_rules) package, you can build agent skills that include `elixir_uikit`'s usage rules. Add the following to your `mix.exs`:

```elixir
# mix.exs
def project do
  [
    # ...
    usage_rules: usage_rules()
  ]
end

defp usage_rules do
  [
    file: "CLAUDE.md",
    skills: [
      location: ".claude/skills",
      build: [
        # Combine elixir_uikit with Phoenix into a single skill
        "phoenix-framework": [
          description:
            "Use this skill when working with Phoenix Framework, LiveView, and UIkit components.",
          usage_rules: [:phoenix, ~r/^phoenix_/, :elixir_uikit]
        ]
      ]
    ]
  ]
end
```

Then run `mix usage_rules.sync` to generate the skill files. This creates a `.claude/skills/phoenix-framework/` directory containing the combined usage rules from Phoenix, Phoenix LiveView, Phoenix HTML, and elixir_uikit.

You can also create a standalone UIkit skill:

```elixir
build: [
  "uikit": [
    description:
      "Use this skill when building UI with UIkit components in Phoenix LiveView templates.",
    usage_rules: [:elixir_uikit]
  ]
]
```

## Do's and Don'ts

**Do:**
- Always use `container: false` (the default) on modals — this keeps the modal in the LiveView DOM tree so LiveView can patch it.
- Always provide stable `id` attributes on `uk_sortable`, `uk_subnav`, `uk_switcher`, and `uk_modal` elements. Child items of sortable containers must also have unique IDs.
- Use `uk_button` with `navigate` or `patch` for navigation instead of raw `<a>` tags.
- Use `field={@form[:field_name]}` on form components for automatic ID, name, value, and error handling.
- Use `<.uk_checkbox>` for checkboxes (not `uk_input` with `type="checkbox"`) — it handles the hidden false-value field.
- Use `uk-*` UIkit utility classes for all styling (spacing, text, flex, visibility, etc.).

**Don't:**
- **NEVER use Tailwind CSS or DaisyUI classes** — this project uses UIkit for styling. Tailwind classes (`flex`, `p-4`, `text-lg`, `bg-blue-500`, etc.) and DaisyUI classes (`btn`, `card`, `modal`, etc.) will not work and must not be used. Use `uk-*` classes instead.
- **Do NOT use `core_components.ex`** — the default Phoenix `CoreComponents` module generated by `phx.new` depends on Tailwind CSS and will not render correctly with UIkit. Use `elixir_uikit` components (`uk_button`, `uk_modal`, `uk_input`, etc.) instead of `CoreComponents` (`button`, `modal`, `input`, `table`, etc.).
- Don't set `container: true` on modals in LiveView — UIkit will move the modal outside the LiveView DOM tree, breaking patching.
- Don't use raw UIkit HTML when a component exists — the components handle class generation and LiveView integration.
- Don't forget `id` on interactive components (`uk_sortable`, `uk_subnav` with switcher, `uk_modal` with `show`).
- Don't use `uk_input` with `type="checkbox"` — use `uk_checkbox` instead.
