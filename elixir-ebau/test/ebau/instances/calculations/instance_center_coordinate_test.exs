defmodule Ebau.Instances.Calculations.InstanceCenterCoordinateTest do
  use Ebau.DataCase, async: true

  import Ebau.Test.InstanceFixtures

  @geometry %{
    "markers" => [%{"x" => 2_760_907.75, "y" => 1_191_927.88}],
    "geometry" => "POINT",
    "center" => %{"x" => 2_760_907.75, "y" => 1_191_927.88}
  }

  setup [:create_workflow, :create_form]

  describe "the drawn GIS geometry" do
    test "provides both coordinates of its center" do
      assert coordinates(geometry: @geometry) == {2_760_907.75, 1_191_927.88}
    end

    test "takes precedence over the plot coordinates" do
      assert coordinates(geometry: @geometry, plots: [%{east: "456.0", north: "123.0"}]) ==
               {2_760_907.75, 1_191_927.88}
    end

    test "provides floats for a center that landed on whole numbers" do
      geometry = Map.put(@geometry, "center", %{"x" => 2_760_907, "y" => 1_191_927})

      assert coordinates(geometry: geometry) === {2_760_907.0, 1_191_927.0}
    end
  end

  describe "the first plot row as fallback" do
    test "provides east as x and north as y" do
      assert coordinates(plots: [%{east: "456.0", north: "123.0"}]) === {456.0, 123.0}
    end

    test "is used when the geometry has no center" do
      geometry = Map.put(@geometry, "center", nil)

      assert coordinates(geometry: geometry, plots: [%{east: "456.0", north: "123.0"}]) ===
               {456.0, 123.0}
    end

    test "ignores all but the first plot row" do
      plots = [%{east: "456.0", north: "123.0"}, %{east: "888.0", north: "999.0"}]

      assert coordinates(plots: plots) === {456.0, 123.0}
    end

    test "is used when the geometry answer is not valid JSON" do
      assert coordinates(geometry_json: "not json", plots: [%{east: "456.0", north: "123.0"}]) ===
               {456.0, 123.0}
    end
  end

  describe "without any coordinates" do
    test "both are nil when the instance has neither geometry nor plots" do
      assert coordinates([]) == {nil, nil}
    end

    test "both are nil when the geometry answer is not valid JSON" do
      assert coordinates(geometry_json: "not json") == {nil, nil}
    end

    test "both are nil when the first plot row has no coordinates" do
      assert coordinates(plots: [%{}]) == {nil, nil}
    end

    test "both are nil when the first plot row's coordinates are not numbers" do
      assert coordinates(plots: [%{east: "n/a", north: "n/a"}]) == {nil, nil}
    end
  end

  defp coordinates(opts) do
    instance = create_instance!(gis_map_geometry_json: geometry_json(opts))

    Enum.each(opts[:plots] || [], fn plot ->
      Ebau.MasterData.create_plot_data_row!(
        %{
          document_id: document_id!(instance),
          coord_east: plot[:east],
          coord_north: plot[:north]
        },
        authorize?: false,
        actor: nil
      )
    end)

    instance =
      Ash.load!(instance, [:dossier_center_coordinates_x, :dossier_center_coordinates_y],
        authorize?: false,
        actor: nil
      )

    {instance.dossier_center_coordinates_x, instance.dossier_center_coordinates_y}
  end

  defp geometry_json(opts) do
    case Keyword.fetch(opts, :geometry) do
      {:ok, geometry} -> JSON.encode!(geometry)
      :error -> opts[:geometry_json]
    end
  end
end
