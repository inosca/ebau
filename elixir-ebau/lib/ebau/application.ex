defmodule Ebau.Application do
  # See https://hexdocs.pm/elixir/Application.html
  # for more information on OTP Applications
  @moduledoc false

  use Application

  @impl true
  def start(_type, _args) do
    children = [
      EbauWeb.Telemetry,
      Ebau.Repo,
      {DNSCluster, query: Application.get_env(:ebau, :dns_cluster_query) || :ignore},
      {Phoenix.PubSub, name: Ebau.PubSub},
      {AshAuthentication.Supervisor, otp_app: :ebau},
      # Start a worker by calling: Ebau.Worker.start_link(arg)
      # {Ebau.Worker, arg},
      # Start to serve requests, typically the last entry
      EbauWeb.Endpoint
    ]

    # See https://hexdocs.pm/elixir/Supervisor.html
    # for other strategies and supported options
    opts = [strategy: :one_for_one, name: Ebau.Supervisor]
    Supervisor.start_link(children, opts)
  end

  # Tell Phoenix to update the endpoint configuration
  # whenever the application is updated.
  @impl true
  def config_change(changed, _new, removed) do
    EbauWeb.Endpoint.config_change(changed, removed)
    :ok
  end
end
