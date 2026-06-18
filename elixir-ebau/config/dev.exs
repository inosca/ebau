import Config

config :ebau, EbauWeb.Endpoint,
  # Bound to all interfaces — accessible from other machines (e.g. Docker host).
  # Change to `ip: {127, 0, 0, 1}` to restrict to loopback only.
  http: [ip: {0, 0, 0, 0}],
  check_origin: false,
  code_reloader: true,
  debug_errors: true,
  secret_key_base: "YQJEbV4PNghnQm7rjjkYtkiA/8yNipPpJRpBr4ITfEFO18jPiG77iUyguVY0dvjL",
  watchers: [
    esbuild: {Esbuild, :install_and_run, [:ebau, ~w(--sourcemap=inline --watch)]},
    sass: {
      DartSass,
      :install_and_run,
      [:default, ~w(--embed-source-map --source-map-urls=absolute --watch)]
    }
  ],
  # Reload browser tabs when matching files change.
  live_reload: [
    web_console_logger: true,
    patterns: [
      # Static assets, except user uploads
      ~r"priv/static/(?!uploads/).*\.(js|css|png|jpeg|jpg|gif|svg)$",
      # Gettext translations
      ~r"priv/gettext/.*\.po$",
      # Router, Controllers, LiveViews and LiveComponents
      ~r"lib/ebau_web/router\.ex$",
      ~r"lib/ebau_web/(controllers|live|components)/.*\.(ex|heex)$"
    ]
  ]

# Enable dev routes for dashboard and mailbox
config :ebau, dev_routes: true, token_signing_secret: "YoorlwyimV6kp8MGl5f74PhXVqJGvD4P"

# Do not include metadata nor timestamps in development logs
config :logger, :default_formatter, format: "[$level] $message\n"

# Set a higher stacktrace during development. Avoid configuring such
# in production as building large stacktraces may be expensive.
config :phoenix, :stacktrace_depth, 20

# Include debug annotations and locations in rendered markup.
# Changing this configuration will require mix clean and a full recompile.
config :phoenix_live_view,
  debug_heex_annotations: true,
  debug_attributes: true,
  enable_expensive_runtime_checks: true
