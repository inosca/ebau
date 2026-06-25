import Config

canton =
  case System.get_env("APPLICATION") do
    "kt_gr" -> :gr
    "kt_so" -> :so
    _ -> :demo
  end

config :ash_json_api,
  show_public_calculations_when_loaded?: true,
  authorize_update_destroy_with_error?: true

config :ebau, Ebau.Mailer, adapter: Swoosh.Adapters.Local

# Configure the endpoint
config :ebau, EbauWeb.Endpoint,
  url: [host: "localhost"],
  adapter: Bandit.PhoenixAdapter,
  render_errors: [
    formats: [html: EbauWeb.ErrorHTML, json: EbauWeb.ErrorJSON],
    layout: false
  ],
  pubsub_server: Ebau.PubSub,
  live_view: [signing_salt: "IJufaPql"]

config :ebau,
  canton: canton,
  ecto_repos: [Ebau.Repo],
  generators: [timestamp_type: :utc_datetime],
  ash_domains: [
    Ebau.Permissions,
    Caluma.Workflow,
    Caluma.Form,
    Ebau.Instances,
    Ebau.MasterData,
    Ebau.User
  ]

# Configure esbuild (the version is required)
config :esbuild,
  version: "0.25.4",
  ebau: [
    args:
      ~w(js/app.js --bundle --target=es2022 --outdir=../priv/static/assets/js --external:/fonts/* --external:/images/* --alias:@=.),
    cd: Path.expand("../assets", __DIR__),
    env: %{"NODE_PATH" => [Path.expand("../deps", __DIR__), Mix.Project.build_path()]}
  ]

# Configure Elixir's Logger
config :logger, :default_formatter,
  format: "$time $metadata[$level] $message\n",
  metadata: [:request_id]

config :mime,
  extensions: %{"json" => "application/vnd.api+json"},
  types: %{"application/vnd.api+json" => ["json"]}

# Use Elixir's built-in JSON module in Phoenix
config :phoenix, :json_library, JSON

config :spark,
  formatter: [
    "Ash.Resource": [section_order: [:json_api]],
    "Ash.Domain": [section_order: [:json_api]]
  ]

if config_env() in [:dev, :test] do
  config :ash, :policies, show_policy_breakdown?: true

  config :phoenix, :plug_init_mode, :runtime

  config :swoosh, :api_client, false
end

import_config "#{config_env()}.exs"
