defmodule Mix.Tasks.Ebau.BootstrapLegacySchema do
  @shortdoc "Bootstraps legacy schema from priv/repo/legacy_structure.sql"

  @moduledoc """
  Imports the legacy schema SQL dump into the configured database.

      mix ecto.create
      mix ebau.bootstrap_legacy_schema

  Requires `psql` to be available on PATH.
  """

  use Mix.Task

  @impl true
  def run(_args) do
    Mix.Task.run("app.start")

    repo_config = Application.fetch_env!(:ebau, Ebau.Repo)

    sql_path =
      Mix.Project.project_file()
      |> Path.dirname()
      |> Path.join("priv/repo/legacy_structure.sql")

    if !File.exists?(sql_path) do
      Mix.raise("legacy schema file not found: #{sql_path}")
    end

    if legacy_schema_present?() do
      Mix.shell().info("Legacy schema already present, reconciling compatibility patches")
      reconcile_legacy_schema!()
    else
      filtered_path = filter_psql_meta_commands!(sql_path)

      try do
        args =
          [
            "-v",
            "ON_ERROR_STOP=1"
          ] ++
            host_args(repo_config) ++
            port_args(repo_config) ++
            user_args(repo_config) ++
            database_args(repo_config) ++ ["-f", filtered_path]

        env =
          if password = repo_config[:password] do
            [{"PGPASSWORD", password}]
          else
            []
          end

        Mix.shell().info("Bootstrapping legacy schema from #{sql_path}")

        case System.cmd("psql", args,
               env: env,
               into: IO.stream(:stdio, :line),
               stderr_to_stdout: true
             ) do
          {_output, 0} ->
            reconcile_legacy_schema!()
            Mix.shell().info("Legacy schema bootstrap complete")

          {_output, status} ->
            Mix.raise("psql failed while importing legacy schema (exit #{status})")
        end
      after
        File.rm(filtered_path)
      end
    end
  end

  defp legacy_schema_present? do
    sql = """
    select
      to_regclass('public."SERVICE"') is not null
      and to_regclass('public."SERVICE_GROUP"') is not null
      and to_regclass('public."ROLE"') is not null
    """

    case Ecto.Adapters.SQL.query(Ebau.Repo, sql, []) do
      {:ok, %{rows: [[true]]}} -> true
      _ -> false
    end
  end

  defp filter_psql_meta_commands!(sql_path) do
    filtered_path =
      Path.join(
        System.tmp_dir!(),
        "ebau_legacy_structure_#{System.unique_integer([:positive])}.sql"
      )

    sql_path
    |> File.stream!()
    |> Stream.reject(&String.starts_with?(&1, "\\"))
    |> Enum.into(File.stream!(filtered_path), fn
      "CREATE SCHEMA keycloak;\n" -> "CREATE SCHEMA IF NOT EXISTS keycloak;\n"
      line -> line
    end)

    filtered_path
  end

  defp reconcile_legacy_schema! do
    ensure_role_slug_column!()
    ensure_role_slug_unique_constraint!()
  end

  defp ensure_role_slug_column! do
    sql = ~S|ALTER TABLE public."ROLE" ADD COLUMN IF NOT EXISTS "SLUG" character varying(50)|
    Ecto.Adapters.SQL.query!(Ebau.Repo, sql, [])
  end

  defp ensure_role_slug_unique_constraint! do
    sql = """
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1
        FROM pg_constraint
        WHERE conname = 'ROLE_slug_key'
          AND conrelid = 'public."ROLE"'::regclass
      ) THEN
        ALTER TABLE public."ROLE" ADD CONSTRAINT "ROLE_slug_key" UNIQUE ("SLUG");
      END IF;
    END
    $$;
    """

    Ecto.Adapters.SQL.query!(Ebau.Repo, sql, [])
  end

  defp host_args(repo_config) do
    if host = repo_config[:hostname], do: ["-h", host], else: []
  end

  defp port_args(repo_config) do
    if port = repo_config[:port], do: ["-p", to_string(port)], else: []
  end

  defp user_args(repo_config) do
    if user = repo_config[:username], do: ["-U", user], else: []
  end

  defp database_args(repo_config) do
    if database = repo_config[:database] do
      ["-d", database]
    else
      Mix.raise("repo database missing in Ebau.Repo config")
    end
  end
end
