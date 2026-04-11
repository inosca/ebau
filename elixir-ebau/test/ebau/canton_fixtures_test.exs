defmodule Ebau.Test.CantonFixturesTest do
  use Ebau.DataCase, async: false

  alias Ebau.Test.CantonFixtures

  test "finds canton config json files" do
    files = CantonFixtures.canton_files!(:so)

    assert Enum.any?(files, &String.ends_with?(&1, "/kt_so/config/caluma_form.json"))
    assert Enum.any?(files, &String.ends_with?(&1, "/kt_so/config/caluma_workflow.json"))
  end

  test "loads supported kt_so config fixtures into the test database" do
    assert :ok = CantonFixtures.load_canton_config!(:so)

    assert exists?("caluma_form_form", "allgemeine-informationen")
    assert exists?("caluma_form_question", "is-paper")
    assert exists?("caluma_workflow_workflow", "building-permit")
    assert question_type("is-paper") == "choice"
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

  defp question_type(slug) do
    %{rows: [[type]]} =
      Ecto.Adapters.SQL.query!(
        Repo,
        "select type from caluma_form_question where slug = $1",
        [slug]
      )

    type
  end
end
