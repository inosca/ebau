defmodule Ebau.Test.CantonFixturesTest do
  use Ebau.DataCase, async: true

  alias Ebau.Test.CantonFixtures

  test "finds canton config json files" do
    files = CantonFixtures.canton_files!(:so)

    assert Enum.any?(files, &String.ends_with?(&1, "/kt_so/config/user.json"))
    assert Enum.any?(files, &String.ends_with?(&1, "/kt_so/config/caluma_workflow.json"))
  end

  test "loads supported kt_so config fixtures into the test database" do
    assert :ok = CantonFixtures.load_canton_config!(:so)

    assert exists?("caluma_workflow_workflow", "building-permit")
  end

  test "loads selected kt_so config files into the test database" do
    assert :ok =
             CantonFixtures.load_canton_files!(:so, [
               "user.json",
               "caluma_workflow.json"
             ])

    assert exists?("caluma_workflow_workflow", "building-permit")
  end

  defp exists?(table, slug) do
    %{rows: [[count]]} =
      Ecto.Adapters.SQL.query!(
        Repo,
        "select count(*) from #{table} where slug = $1",
        [slug]
      )

    count == 1
  end
end
