defmodule Ebau.MixProject do
  use Mix.Project

  def project do
    [
      app: :ebau,
      version: "0.1.0",
      elixir: "~> 1.19",
      elixirc_paths: elixirc_paths(Mix.env()),
      consolidate_protocols: Mix.env() != :test,
      start_permanent: Mix.env() == :prod,
      aliases: aliases(),
      deps: deps(),
      compilers: [:phoenix_live_view] ++ Mix.compilers(),
      listeners: [Phoenix.CodeReloader],
      elixirc_options: [module_definition: :interpreted, ignore_already_consolidated: true],
      docs: [
        main: "readme",
        extras: [
          "README.md",
          "guides/ash-domains.md",
          "guides/ash-policies.md"
        ],
        groups_for_extras: [
          Guides: ~r/guides\/.*/
        ],
        groups_for_modules: [
          Instances: [Ebau.Instances, ~r/Ebau\.Instances\..*/],
          "Master Data": [Ebau.MasterData, ~r/Ebau\.MasterData\..*/],
          Permissions: [Ebau.Permissions, ~r/Ebau\.Permissions\..*/],
          "User & Auth": [Ebau.User, ~r/Ebau\.User\..*/],
          Caluma: [Caluma.Form, Caluma.Workflow, ~r/Caluma\..*/],
          Web: [~r/EbauWeb\..*/]
        ]
      ],
      usage_rules: usage_rules()
    ]
  end

  # Configuration for the OTP application.
  #
  # Type `mix help compile.app` for more information.
  def application do
    [
      mod: {Ebau.Application, []},
      extra_applications: [:logger, :runtime_tools]
    ]
  end

  def cli do
    [
      preferred_envs: [precommit: :test]
    ]
  end

  # Specifies which paths to compile per environment.
  defp elixirc_paths(:test), do: ["lib", "test/support"]
  defp elixirc_paths(_), do: ["lib"]

  # Specifies your project dependencies.
  #
  # Type `mix help deps` for examples and options.
  defp deps do
    [
      {:ash, "~> 3.23"},
      {:ash_admin, "~> 0.13"},
      {:ash_authentication, "~> 4.0"},
      {:ash_authentication_phoenix, "~> 2.0"},
      {:ash_json_api, "~> 1.0"},
      {:ash_oban, "~> 0.7"},
      {:ash_phoenix, "~> 2.0"},
      {:ash_postgres, "~> 2.0"},
      {:bandit, "~> 1.5"},
      {:dart_sass, "~> 0.7", only: [:dev]},
      {:dns_cluster, "~> 0.2.0"},
      {:ecto_sql, "~> 3.13"},
      {:elixir_uikit, "~> 0.7.2"},
      {:esbuild, "~> 0.10", runtime: Mix.env() == :dev},
      {:ex_doc, "~> 0.38", only: :dev, runtime: false},
      {:gettext, "~> 1.0"},
      {:igniter, "~> 0.6", only: [:dev, :test]},
      {:lazy_html, ">= 0.1.0", only: :test},
      {:live_debugger, "~> 0.5", only: [:dev]},
      {:mix_test_interactive, "~> 5.0", only: [:dev, :test], runtime: false},
      {:nvir, "~> 0.15.0"},
      {:oban_web, "~> 2.0"},
      {:open_api_spex, "~> 3.0"},
      {:phoenix, "~> 1.8.3"},
      {:phoenix_ecto, "~> 4.5"},
      {:phoenix_html, "~> 4.1"},
      {:phoenix_live_dashboard, "~> 0.8.3"},
      {:phoenix_live_reload, "~> 1.2", only: :dev},
      {:phoenix_live_view, "~> 1.1.0"},
      {:phoenix_test, "~> 0.8", only: :test, runtime: false},
      {:picosat_elixir, "~> 0.2"},
      {:postgrex, ">= 0.0.0"},
      {:quokka, "~> 2.11", only: [:dev, :test], runtime: false},
      {:req, "~> 0.5"},
      {:swoosh, "~> 1.16"},
      {:telemetry_metrics, "~> 1.0"},
      {:telemetry_poller, "~> 1.0"},
      {:usage_rules, "~> 1.0", only: [:dev]}
    ]
  end

  # Aliases are shortcuts or tasks specific to the current project.
  # For example, to install project dependencies and perform other setup tasks, run:
  #
  #     $ mix setup
  #
  # See the documentation for `Mix` for more info on aliases.
  defp aliases do
    [
      setup: ["deps.get", "ecto.setup", "assets.setup", "assets.build"],
      "ecto.setup": [
        "ecto.create",
        "ebau.bootstrap_legacy_schema",
        "ecto.migrate",
        "run priv/repo/seeds.exs"
      ],
      "ecto.reset": ["ecto.drop", "ecto.setup"],
      test: [
        "ecto.create --quiet",
        "ebau.ensure_legacy_schema",
        "ecto.migrate --quiet",
        "test"
      ],
      "assets.setup": ["esbuild.install --if-missing"],
      "assets.build": ["compile", "esbuild ebau"],
      "assets.deploy": [
        "esbuild ebau --minify",
        "sass default --no-source-map --style=compressed",
        "phx.digest"
      ],
      precommit: [
        "compile --warnings-as-errors",
        "deps.unlock --unused",
        "format",
        "ash.codegen --check"
      ],
      "phx.server": [&phx_server_with_sass/1]
    ]
  end

  defp phx_server_with_sass(args) do
    if Mix.env() == :dev do
      Mix.Task.run("sass", [
        "--runtime-config",
        "default",
        "--embed-source-map",
        "--source-map-urls=absolute"
      ])
    end

    Mix.Tasks.Phx.Server.run(args)
  end

  defp usage_rules do
    [
      file: "CLAUDE.md",
      usage_rules: ["usage_rules:all"],
      skills: [
        location: ".claude/skills",
        build: [
          "ash-framework": [
            description:
              "Use this skill working with Ash Framework or any of its extensions. Always consult this when making any domain changes, features or fixes.",
            usage_rules: [:ash, ~r/^ash_/]
          ],
          "phoenix-framework": [
            description:
              "Use this skill working with Phoenix Framework. Consult this when working with the web layer, controllers, views, liveviews etc.",
            usage_rules: [:phoenix, ~r/^phoenix_/]
          ]
        ]
      ]
    ]
  end
end
