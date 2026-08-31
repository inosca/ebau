defmodule Ebau.Instances.InstanceAnswersTest do
  # Instance writes answers through its case (`caluma_case` with `through`).
  # The generic change is covered in test/caluma/workflow/changes.
  use Ebau.DataCase, async: true

  import Ebau.Test.InstanceFixtures

  setup [:create_workflow, :create_form]

  defp update!(instance, params) do
    Ebau.Instances.update_instance!(instance, params, authorize?: false, actor: nil)
  end

  defp reload(instance, load) do
    Ash.load!(instance, load, authorize?: false, actor: nil)
  end

  describe "create" do
    test "starts the case with the document and writes provided answers" do
      instance = create_instance!(proposal: "Neubau", is_paper: true)

      assert %{proposal: "Neubau", is_paper: true} = reload(instance, [:proposal, :is_paper])
    end

    test "leaves answers alone whose argument is not provided" do
      instance = create_instance!(proposal: "Neubau")

      assert %{proposal: "Neubau", is_paper: nil} = reload(instance, [:proposal, :is_paper])
    end
  end

  describe "update" do
    setup [:create_instance]

    test "sets an answer readable through the calculation", %{instance: instance} do
      update!(instance, %{proposal: "Neubau"})

      assert reload(instance, [:proposal]).proposal == "Neubau"
    end

    test "overwrites instead of duplicating", %{instance: instance} do
      update!(instance, %{proposal: "first"})
      update!(instance, %{proposal: "second"})

      assert reload(instance, [:proposal]).proposal == "second"
    end

    test "leaves answers alone whose argument is not provided", %{instance: instance} do
      update!(instance, %{proposal: "Neubau"})
      update!(instance, %{gis_map_geometry_json: "{}"})

      assert reload(instance, [:proposal]).proposal == "Neubau"
    end

    test "stores the option slug deduced from the mapping", %{instance: instance} do
      update!(instance, %{is_paper: true})

      assert reload(instance, [:is_paper]).is_paper == true
    end

    test "clears a mapped answer when given nil", %{instance: instance} do
      update!(instance, %{is_paper: true})
      update!(instance, %{is_paper: nil})

      assert reload(instance, [:is_paper]).is_paper == nil
    end
  end
end
