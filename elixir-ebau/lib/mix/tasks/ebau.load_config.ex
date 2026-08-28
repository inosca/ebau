defmodule Mix.Tasks.Ebau.LoadConfig do
  @shortdoc "Loads legacy config fixtures for the selected APPLICATION"

  @moduledoc """
  Loads legacy JSON fixtures into the current database.

  The application is selected via `APPLICATION`, matching the Django layout
  under `django/<application>/`.

      APPLICATION=kt_so mix ebau.load_config
      APPLICATION=kt_so mix ebau.load_config --data
      APPLICATION=kt_so mix ebau.load_config --init
      mix ebau.load_config --application kt_gr --data
  """

  use Mix.Task

  alias Ebau.Legacy.ConfigLoader

  @impl true
  def run(args) do
    # Only the repo, not the application: this can be run against a database
    # that has not been migrated yet, and starting the supervision tree would
    # boot Oban before its tables exist.
    Mix.Task.run("app.config")

    {opts, _argv, invalid} =
      OptionParser.parse(args,
        strict: [
          application: :string,
          data: :boolean,
          init: :boolean
        ]
      )

    if invalid != [] do
      Mix.raise("invalid options: #{inspect(invalid)}")
    end

    application =
      opts[:application] ||
        System.get_env("APPLICATION") ||
        Mix.raise("missing application. Set APPLICATION=kt_so or pass --application kt_so")

    scope = if opts[:data], do: :all, else: :config
    include_init? = opts[:init] || false

    Mix.shell().info(
      "Loading legacy config for #{application} (scope=#{scope}, init=#{include_init?})"
    )

    {:ok, _result, _started} =
      Ecto.Migrator.with_repo(Ebau.Repo, fn _repo ->
        ConfigLoader.load_application_config!(application,
          scope: scope,
          include_init?: include_init?
        )
      end)

    Mix.shell().info("Legacy config loaded for #{application}")
  end
end
