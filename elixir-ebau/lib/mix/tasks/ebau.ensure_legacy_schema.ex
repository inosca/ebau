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

  @required_columns [
    {~s(public."ROLE"), "SLUG"}
  ]

  @impl true
  def run(_args) do
    Mix.Task.run("app.start")

    missing =
      Enum.reject(@required_tables, fn table ->
        table_exists?(table)
      end)

    missing_columns =
      Enum.reject(@required_columns, fn {table, column} ->
        column_exists?(table, column)
      end)

    if missing != [] or missing_columns != [] do
      missing_list =
        [
          Enum.map(missing, &"  - missing table: #{&1}"),
          Enum.map(missing_columns, fn {table, column} ->
            "  - missing column: #{table}.#{column}"
          end)
        ]
        |> List.flatten()
        |> Enum.join("\n")

      Mix.raise("""

      ==========================================
      LEGACY SCHEMA NOT IMPORTED OR OUTDATED
      ==========================================

      This project depends on legacy CAMAC tables and columns that are not created by Ash migrations.
      The current database is missing required legacy structure:

      #{missing_list}

      Import or reconcile the legacy schema first:

          mix ebau.bootstrap_legacy_schema

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

  defp column_exists?(table_name, column_name) do
    sql = """
    select exists (
      select 1
      from information_schema.columns
      where table_schema = split_part($1, '.', 1)
        and table_name = trim(both '"' from split_part($1, '.', 2))
        and column_name = $2
    )
    """

    case Ecto.Adapters.SQL.query(Ebau.Repo, sql, [table_name, column_name]) do
      {:ok, %{rows: [[true]]}} -> true
      _ -> false
    end
  end
end
