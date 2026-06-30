defmodule Caluma.Form.Extensions.Document.AnswerTransformerTest do
  use ExUnit.Case, async: true

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      domain: nil,
      data_layer: AshPostgres.DataLayer,
      extensions: [Caluma.Form.Extensions.Document]

    postgres do
      table "caluma_form_document"
      repo Ebau.Repo
      migrate? false
    end

    caluma_document do
      answer :plot_number, :string, question_id: "parzellennummer"
      answer :coord_east, :string, question_id: ["lagekoordinaten-ost", "coordinates-east"]
    end
  end

  describe "answer transformer" do
    test "adds a calculation for each declared field" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :plot_number in calc_names
      assert :coord_east in calc_names
    end

    test "uses Caluma.Form.Calculations.DocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :plot_number))
      assert {Caluma.Form.Calculations.DocumentAnswer, _opts} = calc.calculation
    end

    test "generates a has_one with the question_id slug in its filter" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :plot_number))
      {_mod, opts} = calc.calculation
      rel = Ash.Resource.Info.relationship(TestResource, opts[:relationship])
      assert inspect(rel.filter) =~ "\"parzellennummer\""
    end

    test "supports list of question IDs" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :coord_east))
      {_mod, opts} = calc.calculation
      rel = Ash.Resource.Info.relationship(TestResource, opts[:relationship])
      filter = inspect(rel.filter)
      assert filter =~ "\"lagekoordinaten-ost\""
      assert filter =~ "\"coordinates-east\""
    end
  end
end
