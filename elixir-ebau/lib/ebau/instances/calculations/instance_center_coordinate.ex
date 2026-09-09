defmodule Ebau.Instances.Calculations.InstanceCenterCoordinate do
  @moduledoc """
  Read an axis of the dossier center coordinates.

  Either from the :gis_map_geometry_json answer or from the
  first :data_plot row as fallback.

  Always a float, or nil when neither source has the axis. Both sources are
  coerced: the geometry carries JSON numbers, so a center that lands on a whole
  number decodes as an integer, and a plot row answer is a plain text string.

  This is a elixir calculation module rather than db expression because the
  geometry is decoded in elixir. The question is a plain text question so a legacy
  import or a manual edit can leave invalid JSON. A `::jsonb` cast in the query
  raises `22P02` which fails the read for every instance in the result.

  Postgres 15 has no way to guard that cast inline. `IS JSON` and
  `pg_input_is_valid/2` are both 16+.

  TODO: this can become a db calculation with fragments once:

    * the jsonb cast can be made safe: either on Postgres 16+ via `IS JSON`,
      or by shipping a `try_jsonb(text) RETURNS jsonb` plpgsql function as an
      `AshPostgres.CustomExtension`. Note its `EXCEPTION` block opens a
      subtransaction per call, so guard it with a cheap prefilter.
  """

  use Ash.Resource.Calculation

  @plot_fields %{x: :coord_east, y: :coord_north}

  @impl true
  def init(opts) do
    case opts[:axis] do
      axis when axis in [:x, :y] -> {:ok, opts}
      _ -> {:error, "axis option is required (:x or :y)"}
    end
  end

  @impl true
  def load(_query, _opts, _context) do
    [:gis_map_geometry_json, plot_data: [:coord_east, :coord_north]]
  end

  @impl true
  def calculate(records, opts, _context) do
    Enum.map(records, fn record ->
      record
      |> decode_geometry()
      |> get_center_coordinate(record, opts[:axis])
    end)
  end

  defp get_center_coordinate(%{"center" => %{"x" => x}}, _instance, :x) when not is_nil(x),
    do: to_float(x)

  defp get_center_coordinate(%{"center" => %{"y" => y}}, _instance, :y) when not is_nil(y),
    do: to_float(y)

  defp get_center_coordinate(_geometry, %{plot_data: [first_plot | _tail]}, axis),
    do: first_plot |> Map.get(@plot_fields[axis]) |> to_float()

  defp get_center_coordinate(_geometry, _instance, _axis), do: nil

  defp to_float(value) when is_float(value), do: value

  defp to_float(value) do
    case Ecto.Type.cast(:float, value) do
      {:ok, float} -> float
      :error -> nil
    end
  end

  defp decode_geometry(%{gis_map_geometry_json: json}) when is_binary(json) do
    case JSON.decode(json) do
      {:ok, geometry} -> geometry
      {:error, _reason} -> nil
    end
  end

  defp decode_geometry(_instance), do: nil
end
