# Translations (Gettext)

eBau uses [Gettext](https://hexdocs.pm/gettext) for internationalization. The
backend module is `EbauWeb.Gettext`. Translation files live under
`priv/gettext`, and we currently ship **German (`de`)**, **French (`fr`)** and **Italian (`it`)**.

## How it fits together

```
priv/gettext/
  default.pot            # template: every msgid from gettext(...) calls
  errors.pot             # template: every msgid from dgettext("errors", ...)
  de/LC_MESSAGES/
    default.po           # German translations, :default domain
    errors.po            # German translations, :errors domain
  fr/LC_MESSAGES/
    default.po           # French
    errors.po
  it/LC_MESSAGES/
    default.po           # Italian
    errors.po
```

- **`.pot`** files are *templates*: they hold the source strings (`msgid`) with
  empty translations. One per domain. They are generated, never edited by hand.
- **`.po`** files hold the actual translations (`msgstr`) for one locale and
  domain. These are what translators edit.
- A **domain** namespaces strings. `default` covers plain `gettext("...")`
  calls; `errors` covers `dgettext("errors", "...")`, used for validation and
  error messages.

At runtime the `.po` files are compiled into the backend. `Gettext.put_locale/1`
selects the active locale. A missing or empty `msgstr` falls back to the source
string, so untranslated text never crashes; it just renders in the original
language.

## Marking strings for translation

```elixir
use Gettext, backend: EbauWeb.Gettext

# :default domain
gettext("Hello")

# plural
ngettext("One instance", "%{count} instances", count)

# :errors domain
dgettext("errors", "is invalid")
```

## Extracting strings

After adding or changing any `gettext`/`dgettext` call, re-extract the templates:

```
mix gettext.extract
```

This scans the source and rewrites the `.pot` files. To extract and push the new
strings into every locale's `.po` in one step:

```
mix gettext.extract --merge
```

## Merging into locales

`merge` syncs each locale `.po` against the `.pot` templates: it adds new
msgids (with empty translations), removes dead ones, and marks changed strings
`#, fuzzy` for review.

```
mix gettext.merge priv/gettext
```

## Translating

Open the locale's `.po` file and fill in each `msgstr`:

```po
#: lib/ebau_web/components/core_components.ex:42
msgid "Hello"
msgstr "Hallo"
```

If a string was changed after translation, gettext flags it:

```po
#, fuzzy
msgid "Hello there"
msgstr "Hallo"
```

Update the `msgstr` and remove the `#, fuzzy` line to mark it done.

## Further reading

- [Gettext for Elixir](https://hexdocs.pm/gettext)
- [Gettext mix tasks](https://hexdocs.pm/gettext/Mix.Tasks.Gettext.Extract.html)
