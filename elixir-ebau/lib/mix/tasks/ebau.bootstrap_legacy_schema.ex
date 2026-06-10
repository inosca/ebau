defmodule Mix.Tasks.Ebau.BootstrapLegacySchema do
  @shortdoc "Bootstraps legacy schema from priv/repo/ebau_schema.sql"

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
      |> Path.join("priv/repo/ebau_schema.sql")

    ensure_case_insensitive_collation!()

    if legacy_schema_present?() do
      Mix.shell().info("Legacy schema already present, reconciling compatibility patches")
      reconcile_legacy_schema!()
    else
      filtered_path = filter_psql_meta_commands!(sql_path)

      try do
        Mix.shell().info("Bootstrapping legacy schema from #{sql_path}")

        case System.cmd("psql", psql_args(repo_config, filtered_path),
               env: psql_env(repo_config),
               stderr_to_stdout: true
             ) do
          {_output, 0} ->
            reconcile_legacy_schema!()
            Mix.shell().info("Legacy schema bootstrap complete")

          {output, status} ->
            Mix.raise("""
            psql failed while importing legacy schema (exit #{status})

            #{tail_output(output)}
            """)
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

    %{rows: [[present?]]} = Ecto.Adapters.SQL.query!(Ebau.Repo, sql, [])
    present?
  end

  defp filter_psql_meta_commands!(sql_path) do
    filtered_path =
      Path.join(
        System.tmp_dir!(),
        "ebau_legacy_structure_#{System.unique_integer([:positive])}.sql"
      )

    sql_path
    |> File.read!()
    |> String.replace(~r/^\\.*$\n?/m, "")
    |> String.replace("CREATE SCHEMA keycloak;\n", "CREATE SCHEMA IF NOT EXISTS keycloak;\n")
    |> then(&File.write!(filtered_path, &1))

    filtered_path
  end

  defp reconcile_legacy_schema! do
    ensure_case_insensitive_collation!()
    ensure_role_slug_column!()
    ensure_role_slug_unique_constraint!()
  end

  defp ensure_case_insensitive_collation! do
    sql = """
    CREATE COLLATION IF NOT EXISTS public.case_insensitive (
      provider = icu,
      locale = 'und-u-ks-level2',
      deterministic = false
    )
    """

    Ecto.Adapters.SQL.query!(Ebau.Repo, sql, [])
  end

  defp ensure_role_slug_column! do
    sql = ~S|ALTER TABLE public."ROLE" ADD COLUMN IF NOT EXISTS slug character varying(50)|
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
        ALTER TABLE public."ROLE" ADD CONSTRAINT "ROLE_slug_key" UNIQUE (slug);
      END IF;
    END
    $$;
    """

    Ecto.Adapters.SQL.query!(Ebau.Repo, sql, [])
  end

  defp psql_args(repo_config, filtered_path) do
    [
      "-q",
      "-v",
      "ON_ERROR_STOP=1",
      "-d",
      Keyword.fetch!(repo_config, :database)
    ] ++
      maybe_arg("-h", repo_config[:hostname]) ++
      maybe_arg("-p", repo_config[:port]) ++
      maybe_arg("-U", repo_config[:username]) ++
      ["-f", filtered_path]
  end

  defp psql_env(repo_config) do
    if password = repo_config[:password], do: [{"PGPASSWORD", password}], else: []
  end

  defp maybe_arg(_flag, nil), do: []
  defp maybe_arg(flag, value), do: [flag, to_string(value)]

  defp tail_output(output, line_count \\ 80) do
    case output |> String.trim() |> String.split("\n", trim: true) do
      [] ->
        "psql did not produce any output"

      lines ->
        title =
          if length(lines) > line_count,
            do: "--- psql output (last #{line_count} lines) ---",
            else: "--- psql output ---"

        [title | Enum.take(lines, -line_count)]
        |> Enum.join("\n")
    end
  end
end
