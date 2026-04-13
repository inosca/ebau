[
  import_deps: [
    :ash_json_api,
    :ash_authentication_phoenix,
    :ash_authentication,
    :ash_postgres,
    :ash,
    :ecto,
    :ecto_sql,
    :phoenix
  ],
  subdirectories: ["priv/*/migrations"],
  plugins: [Phoenix.LiveView.HTMLFormatter, Quokka],
  quokka: [
    # Disable Quokka's :module_directives style. It hoists large module
    # attributes out of `defmodule` blocks and unquotes them back in, which
    # breaks Spark DSL extensions where one @attr references another (e.g. a
    # Section whose :entities list references an @entity attribute): once
    # hoisted, the Section is evaluated at top level before @entity exists.
    exclude: [:module_directives]
  ],
  excludes: [
    # Quokka's :blocks style inverts `if is_nil(x) do nil else body end` into
    # `if !is_nil(x) do body end`, which breaks Ash expressions (no `!` operator).
    "lib/caluma/form/calculations/mapped_list_document_answer.ex"
  ],
  inputs: ["*.{heex,ex,exs}", "{config,lib,test}/**/*.{heex,ex,exs}", "priv/*/seeds.exs"],
  locals_without_parens: [
    table: 3,
    answer: 3,
    mapped_answer: 3,
    mapped_list_answer: 3,
    case_meta: 3,
    via: 3
  ]
]
