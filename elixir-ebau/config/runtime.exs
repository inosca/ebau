import Config

# config/runtime.exs is executed for all environments, including
# during releases. It is executed after compilation and before the
# system starts, so it is typically used to load production configuration
# and secrets from environment variables or elsewhere. Do not define
# any compile-time configuration in here, as it won't be applied.
# The block below contains prod specific runtime configuration.

# ## Using releases
#
# If you use `mix release`, you need to explicitly enable the server
# by passing the PHX_SERVER=true when you start it:
#
#     PHX_SERVER=true bin/ebau start
#
# Alternatively, you can use `mix phx.gen.release` to generate a `bin/server`
# script that automatically sets the env var above.
if System.get_env("PHX_SERVER") do
  config :ebau, EbauWeb.Endpoint, server: true
end

Nvir.dotenv!(["../.env", ".env", ".env.#{config_env()}"])

# We don't build scss in test
if config_env() in [:dev, :prod] do
  # We dynamically need to build different cantonal scss files here
  config :dart_sass,
    version: "1.77.8",
    default: [
      args: [
        "css/app-#{System.fetch_env!("APPLICATION")}.scss",
        "../priv/static/assets/css/app.css"
      ],
      cd: Path.expand("../assets", __DIR__)
    ]
end

config :ebau, Ebau.Repo,
  username: System.get_env("DATABASE_USER", "camac"),
  password: System.get_env("DATABASE_PASSWORD", "camac"),
  hostname: System.get_env("DATABASE_HOST", "localhost"),
  port: String.to_integer(System.get_env("DATABASE_PORT", "5432")),
  database: System.get_env("DATABASE_NAME", System.fetch_env!("APPLICATION")),
  ssl: System.get_env("DATABASE_ENABLE_SSL") == "true",
  pool_size: String.to_integer(System.get_env("POOL_SIZE", "10")),
  pool_count: String.to_integer(System.get_env("POOL_COUNT", "1"))

config :ebau, EbauWeb.Endpoint,
  http: [port: String.to_integer(System.get_env("PORT", "4000"))],
  url: [path: System.get_env("URL_PREFIX", "/")]

config :ebau, :keycloak,
  url: System.get_env("KEYCLOAK_URL", "http://ebau-keycloak.localhost/auth/"),
  realm: System.get_env("KEYCLOAK_REALM", "ebau"),
  client_id: System.get_env("KEYCLOAK_CLIENT", "camac"),
  scopes: System.get_env("KEYCLOAK_SCOPES", "openid email"),
  email_claim: System.get_env("DJANGO_OIDC_EMAIL_CLAIM", "email")

if config_env() == :dev do
  config :ebau, Ebau.Repo,
    stacktrace: true,
    show_sensitive_data_on_connection_error: true,
    pool_size: 10
end

if config_env() == :prod do
  maybe_ipv6 = if System.get_env("ECTO_IPV6") in ~w(true 1), do: [:inet6], else: []

  # The secret key base is used to sign/encrypt cookies and other secrets.
  # A default value is used in config/dev.exs and config/test.exs but you
  # want to use a different value for prod and you most likely don't want
  # to check this value into version control, so we use an environment
  # variable instead.
  secret_key_base =
    System.get_env("SECRET_KEY_BASE") ||
      raise """
      environment variable SECRET_KEY_BASE is missing.
      You can generate one by calling: mix phx.gen.secret
      """

  host = System.get_env("BASE_URL")

  config :ebau, Ebau.Repo, socket_options: maybe_ipv6

  config :ebau, EbauWeb.Endpoint,
    url: [host: host, port: 443, scheme: "https"],
    http: [
      # Enable IPv6 and bind on all interfaces.
      # Set it to  {0, 0, 0, 0, 0, 0, 0, 1} for local network only access.
      # See the documentation on https://hexdocs.pm/bandit/Bandit.html#t:options/0
      # for details about using IPv6 vs IPv4 and loopback vs public addresses.
      ip: {0, 0, 0, 0, 0, 0, 0, 0}
    ],
    secret_key_base: secret_key_base

  config :ebau, :dns_cluster_query, System.get_env("DNS_CLUSTER_QUERY")

  config :ebau,
    token_signing_secret:
      System.get_env("TOKEN_SIGNING_SECRET") ||
        raise("""
        Missing environment variable `TOKEN_SIGNING_SECRET`!
        You can generate one by calling: mix phx.gen.secret
        """)

  # ## SSL Support
  #
  # To get SSL working, you will need to add the `https` key
  # to your endpoint configuration:
  #
  #     config :ebau, EbauWeb.Endpoint,
  #       https: [
  #         ...,
  #         port: 443,
  #         cipher_suite: :strong,
  #         keyfile: System.get_env("SOME_APP_SSL_KEY_PATH"),
  #         certfile: System.get_env("SOME_APP_SSL_CERT_PATH")
  #       ]
  #
  # The `cipher_suite` is set to `:strong` to support only the
  # latest and more secure SSL ciphers. This means old browsers
  # and clients may not be supported. You can set it to
  # `:compatible` for wider support.
  #
  # `:keyfile` and `:certfile` expect an absolute path to the key
  # and cert in disk or a relative path inside priv, for example
  # "priv/ssl/server.key". For all supported SSL configuration
  # options, see https://hexdocs.pm/plug/Plug.SSL.html#configure/1
  #
  # We also recommend setting `force_ssl` in your config/prod.exs,
  # ensuring no data is ever sent via http, always redirecting to https:
  #
  #     config :ebau, EbauWeb.Endpoint,
  #       force_ssl: [hsts: true]
  #
  # Check `Plug.SSL` for all available options in `force_ssl`.

  # ## Configuring the mailer
  #
  # In production you need to configure the mailer to use a different adapter.
  # Here is an example configuration for Mailgun:
  #
  #     config :ebau, Ebau.Mailer,
  #       adapter: Swoosh.Adapters.Mailgun,
  #       api_key: System.get_env("MAILGUN_API_KEY"),
  #       domain: System.get_env("MAILGUN_DOMAIN")
  #
  # Most non-SMTP adapters require an API client. Swoosh supports Req, Hackney,
  # and Finch out-of-the-box. This configuration is typically done at
  # compile-time in your config/prod.exs:
  #
  #     config :swoosh, :api_client, Swoosh.ApiClient.Req
  #
  # See https://hexdocs.pm/swoosh/Swoosh.html#module-installation for details.
end
