# This file is responsible for configuring your application
# and its dependencies with the aid of the Config module.
#
# This configuration file is loaded before any dependency and
# is restricted to this project.

# General application configuration
import Config

config :ash_json_api,
  show_public_calculations_when_loaded?: false,
  authorize_update_destroy_with_error?: true

# Configure the mailer
#
# By default it uses the "Local" adapter which stores the emails
# locally. You can see the emails in your browser, at "/dev/mailbox".
#
# For production it's recommended to configure a different adapter
# at the `config/runtime.exs`.
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
  ecto_repos: [Ebau.Repo],
  generators: [timestamp_type: :utc_datetime],
  ash_domains: [
    Caluma.Workflow,
    Caluma.Form,
    Ebau.Users,
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

# Use Jason for JSON parsing in Phoenix
config :phoenix, :json_library, Jason

config :spark,
  formatter: [
    "Ash.Resource": [section_order: [:json_api]],
    "Ash.Domain": [section_order: [:json_api]]
  ]

import_config "#{config_env()}.exs"
