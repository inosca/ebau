# UIkit CSS Utility Classes

Use these `uk-*` classes alongside elixir_uikit components for layout and styling. Apply them via the `class` attribute on components or on plain HTML elements.

**Important:** Do NOT use Tailwind CSS classes (`flex`, `p-4`, `text-lg`, `bg-blue-500`, etc.) or DaisyUI classes. This project uses UIkit — use `uk-*` utility classes for all styling.

## Width

Control element widths using fractions or fixed sizes.

| Class | Description |
|---|---|
| `uk-width-1-1` | Full width |
| `uk-width-1-2` | Half width |
| `uk-width-1-3`, `uk-width-2-3` | Thirds |
| `uk-width-1-4`, `uk-width-3-4` | Quarters |
| `uk-width-1-5`, `uk-width-2-5`, etc. | Fifths |
| `uk-width-1-6`, `uk-width-5-6` | Sixths |
| `uk-width-auto` | Natural content width |
| `uk-width-expand` | Fill remaining space |
| `uk-width-small`, `uk-width-medium`, `uk-width-large`, `uk-width-xlarge`, `uk-width-2xlarge` | Fixed breakpoint widths |

**Responsive:** Add `@s`, `@m`, `@l`, `@xl` suffixes: `uk-width-1-2@m` (half width at medium+).

## Text

| Class | Description |
|---|---|
| `uk-text-left`, `uk-text-center`, `uk-text-right`, `uk-text-justify` | Alignment |
| `uk-text-lead` | Larger intro text |
| `uk-text-meta` | Small muted meta text |
| `uk-text-small`, `uk-text-large` | Size modifiers |
| `uk-text-bold`, `uk-text-light`, `uk-text-normal` | Weight |
| `uk-text-italic` | Italic |
| `uk-text-uppercase`, `uk-text-lowercase`, `uk-text-capitalize` | Transform |
| `uk-text-muted`, `uk-text-emphasis`, `uk-text-primary`, `uk-text-secondary`, `uk-text-success`, `uk-text-warning`, `uk-text-danger` | Color |
| `uk-text-truncate` | Truncate with ellipsis |
| `uk-text-break` | Break long words |
| `uk-text-nowrap` | No wrapping |

## Margin

| Class | Description |
|---|---|
| `uk-margin` | Default margin (top + bottom) |
| `uk-margin-top`, `uk-margin-bottom`, `uk-margin-left`, `uk-margin-right` | Directional |
| `uk-margin-small`, `uk-margin-small-top`, etc. | Small spacing |
| `uk-margin-medium`, `uk-margin-medium-top`, etc. | Medium spacing |
| `uk-margin-large`, `uk-margin-large-top`, etc. | Large spacing |
| `uk-margin-xlarge`, `uk-margin-xlarge-top`, etc. | Extra-large spacing |
| `uk-margin-remove`, `uk-margin-remove-top`, etc. | Remove margin |
| `uk-margin-auto`, `uk-margin-auto-left`, `uk-margin-auto-right` | Auto margins (centering) |

## Padding

| Class | Description |
|---|---|
| `uk-padding` | Default padding |
| `uk-padding-small` | Small padding |
| `uk-padding-large` | Large padding |
| `uk-padding-remove`, `uk-padding-remove-top`, etc. | Remove padding |

## Flex

Apply to a container to use flexbox. Combine with width utilities on children.

| Class | Description |
|---|---|
| `uk-flex` | Enable flexbox |
| `uk-flex-inline` | Inline flexbox |
| `uk-flex-row`, `uk-flex-column` | Direction |
| `uk-flex-row-reverse`, `uk-flex-column-reverse` | Reverse direction |
| `uk-flex-wrap`, `uk-flex-nowrap`, `uk-flex-wrap-reverse` | Wrapping |
| `uk-flex-left`, `uk-flex-center`, `uk-flex-right`, `uk-flex-between`, `uk-flex-around` | Horizontal alignment |
| `uk-flex-top`, `uk-flex-middle`, `uk-flex-bottom`, `uk-flex-stretch` | Vertical alignment |
| `uk-flex-first`, `uk-flex-last` | Reorder items |
| `uk-flex-none` | Prevent flex shrink/grow |

## Visibility

| Class | Description |
|---|---|
| `uk-hidden` | Always hidden |
| `uk-invisible` | Hidden but takes up space |
| `uk-visible@s`, `uk-visible@m`, `uk-visible@l`, `uk-visible@xl` | Show at breakpoint+ |
| `uk-hidden@s`, `uk-hidden@m`, `uk-hidden@l`, `uk-hidden@xl` | Hide at breakpoint+ |

## Position

| Class | Description |
|---|---|
| `uk-position-relative`, `uk-position-absolute`, `uk-position-fixed` | Positioning |
| `uk-position-top`, `uk-position-bottom`, `uk-position-left`, `uk-position-right` | Edge positioning |
| `uk-position-top-left`, `uk-position-top-right`, `uk-position-bottom-left`, `uk-position-bottom-right` | Corner positioning |
| `uk-position-center` | Center in parent |
| `uk-position-z-index` | High z-index |

## Background

| Class | Description |
|---|---|
| `uk-background-default`, `uk-background-muted`, `uk-background-primary`, `uk-background-secondary` | Background color |
| `uk-background-cover`, `uk-background-contain` | Background image sizing |

## Overflow

| Class | Description |
|---|---|
| `uk-overflow-auto` | Scroll when content overflows |
| `uk-overflow-hidden` | Hide overflow |

## Border

| Class | Description |
|---|---|
| `uk-border-rounded` | Slightly rounded corners |
| `uk-border-circle` | Circular element |
| `uk-border-pill` | Pill shape |
