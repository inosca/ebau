defmodule Mix.Tasks.Ebau.EnsureLegacySchema do
  @shortdoc "Checks that legacy schema has been imported before running Elixir tests"

  @moduledoc """
  Verifies that required legacy tables exist in the current database.

  Intended for use before `mix test`, so developers get a clear error instead of
  obscure migration/runtime failures when the legacy schema has not been imported yet.
  """

  use Mix.Task

  @required_tables [
    ~s(public."SERVICE"),
    ~s(public."SERVICE_GROUP"),
    ~s(public."ROLE"),
    ~s(public."GROUP"),
    ~s(public."USER"),
    ~s(public."INSTANCE")
  ]

  @impl true
  def run(_args) do
    # Only the repo, not the application: this runs before `ecto.migrate` on a
    # fresh database, and starting the supervision tree here would boot Oban
    # before its tables exist.
    Mix.Task.run("app.config")

    {:ok, _result, _started} = Ecto.Migrator.with_repo(Ebau.Repo, fn _repo -> check() end)
  end

  defp check do
    missing =
      Enum.reject(@required_tables, fn table ->
        table_exists?(table)
      end)

    if missing != [] do
      missing_list =
        missing
        |> Enum.map_join("\n", &"  - missing table: #{&1}")

      Mix.raise("""

      ==========================================
      LEGACY SCHEMA NOT IMPORTED OR OUTDATED
      ==========================================

      This project depends on legacy CAMAC tables and columns that are not created by Ash migrations.
      The current database is missing required legacy structure:

      #{missing_list}

      Import or reconcile the legacy schema first:

          make setup-test

      Then rerun:

          mix test
      """)
    end
  end

  defp table_exists?(table_name) do
    sql = "select to_regclass($1) is not null"

    case Ecto.Adapters.SQL.query(Ebau.Repo, sql, [table_name]) do
      {:ok, %{rows: [[true]]}} -> true
      _ -> false
    end
  end
end
