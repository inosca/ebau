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
  inputs: ["*.{heex,ex,exs}", "{config,lib,test}/**/*.{heex,ex,exs}", "priv/*/seeds.exs"],
  locals_without_parens: [master_data: 1, table: 3, answer: 3, mapped_answer: 3, case_meta: 3]
]
