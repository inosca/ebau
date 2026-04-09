defmodule Ebau.Caluma.Extensions.DocumentBackedTest do
  use ExUnit.Case, async: true

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      domain: nil,
      data_layer: Ash.DataLayer.Simple,
      extensions: [Ebau.Caluma.Extensions.DocumentBacked]

    resource do
      require_primary_key? false
    end

    caluma_document do
      field :plot_number, :string, question_ids: %{default: "parzellennummer"}

      field :coord_east, :string,
        question_ids: %{default: "lagekoordinaten-ost", gr: "coordinates-east"}
    end
  end

  describe "transformer" do
    test "adds a calculation for each declared field" do
      calc_names = TestResource |> Ash.Resource.Info.calculations() |> Enum.map(& &1.name)
      assert :plot_number in calc_names
      assert :coord_east in calc_names
    end

    test "uses DocumentAnswer as the calculation module" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :plot_number))
      assert {Ebau.Caluma.Calculations.DocumentAnswer, _opts} = calc.calculation
    end

    test "passes question_ids option to the calculation" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :plot_number))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "parzellennummer"}
    end

    test "supports canton-specific question_ids" do
      calc = Enum.find(Ash.Resource.Info.calculations(TestResource), &(&1.name == :coord_east))
      {_mod, opts} = calc.calculation
      assert opts[:question_ids] == %{default: "lagekoordinaten-ost", gr: "coordinates-east"}
    end
  end
end
