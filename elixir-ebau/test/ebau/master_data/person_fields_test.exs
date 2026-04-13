defmodule Ebau.MasterData.PersonFieldsTest do
  use ExUnit.Case, async: true

  defmodule TestResource do
    use Ash.Resource,
      otp_app: :ebau,
      data_layer: AshPostgres.DataLayer,
      extensions: [Caluma.Form.Extensions.Document, Ebau.MasterData.PersonFields],
      domain: nil

    postgres do
      table "caluma_form_document"
      repo Ebau.Repo
      migrate? false
    end
  end

  @expected_fields [
    :title,
    :last_name,
    :first_name,
    :street,
    :street_number,
    :zip,
    :town,
    :country,
    :email,
    :tel,
    :po_box,
    :juristic_name,
    :representative_title,
    :representative_last_name,
    :representative_first_name,
    :representative_street,
    :representative_street_number,
    :representative_zip,
    :representative_town,
    :representative_country,
    :representative_email,
    :representative_tel,
    :representative_po_box,
    :representative_juristic_name
  ]

  describe "PersonFields extension" do
    test "injects all 24 person field calculations" do
      calc_names =
        TestResource
        |> Ash.Resource.Info.calculations()
        |> Enum.map(& &1.name)

      for field <- @expected_fields do
        assert field in calc_names, "expected calculation #{inspect(field)} to be present"
      end

      assert length(@expected_fields) == 24
    end

    test "each calculation uses DocumentAnswer as the calculation module" do
      calculations = Ash.Resource.Info.calculations(TestResource)

      for field <- @expected_fields do
        calc = Enum.find(calculations, &(&1.name == field))

        {module, _opts} = calc.calculation
        assert module == Caluma.Form.Calculations.DocumentAnswer
      end
    end

    test "each calculation references an auto-generated has_one relationship" do
      calculations = Ash.Resource.Info.calculations(TestResource)
      relationships = Ash.Resource.Info.relationships(TestResource)

      for field <- @expected_fields do
        calc = Enum.find(calculations, &(&1.name == field))
        {_module, opts} = calc.calculation

        rel_name = Keyword.fetch!(opts, :relationship)
        assert is_atom(rel_name)

        rel = Enum.find(relationships, &(&1.name == rel_name))
        assert rel, "expected relationship #{inspect(rel_name)} for field #{field}"
        assert rel.type == :has_one
        assert rel.destination == Caluma.Form.Answer
        assert rel.filter != nil
      end
    end
  end
end
