import Config

# Configure your database
#
# The MIX_TEST_PARTITION environment variable can be used

# In test we don't send emails
# to provide built-in test partitioning in CI environment.
# Run `mix help test` for more information.
config :ebau, Ebau.Mailer, adapter: Swoosh.Adapters.Test

config :ebau, Ebau.Repo,
  username: System.get_env("DATABASE_USER", "camac"),
  password: System.get_env("DATABASE_PASSWORD", "camac"),
  hostname: System.get_env("DATABASE_HOST", "localhost"),
  database: "ebau_test#{System.get_env("MIX_TEST_PARTITION")}",
  pool: Ecto.Adapters.SQL.Sandbox,
  # We don't run a server during test. If one is required,
  # you can enable the server option below.
  pool_size: System.schedulers_online() * 2

config :ebau, EbauWeb.Endpoint,
  http: [ip: {127, 0, 0, 1}, port: 4002],
  secret_key_base: "T0W1/wc0qchpSGAM3hjpqGkwOPXaKmA4ZWhs6l0/9LRkZ3Bgy6Hc9AnvViaUeHrw",
  server: false

# Print only warnings and errors during test
config :logger, level: :warning

# Initialize plugs at runtime for faster test compilation
config :phoenix, :plug_init_mode, :runtime

# Sort query params output of verified routes for robust url comparisons
config :phoenix,
  sort_verified_routes_query_params: true

# Enable helpful, but potentially expensive runtime checks
config :phoenix_live_view,
  enable_expensive_runtime_checks: true

# Disable swoosh api client as it is only required for production adapters
config :swoosh, :api_client, false
