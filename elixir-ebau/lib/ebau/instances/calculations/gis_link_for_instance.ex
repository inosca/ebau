defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  @moduledoc """
  Renders a GIS link URL for a concrete instance.

  Sets the `c` query parameter on the configured placeholder URL to the
  truncated east/north coordinates of the instance's first plot. Returns nil
  when no instance_id is supplied; uses empty coordinates when the instance
  has no plot data.
  """

  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, %{arguments: %{instance_id: nil}}) do
    Enum.map(records, fn _ -> nil end)
  end

  def calculate(records, _opts, context) do
    instance =
      Ebau.Instances.get_instance_by_id!(
        context.arguments.instance_id,
        Keyword.put(Ash.Context.to_opts(context), :load, plot_data: [:coord_north, :coord_east])
      )

    coords = first_plot_coords(instance.plot_data)
    Enum.map(records, &set_coordinate_param(&1.placeholder, coords))
  end

  defp first_plot_coords([plot | _]),
    do: "#{coord_int(plot.coord_east)},#{coord_int(plot.coord_north)}"

  defp first_plot_coords([]), do: ","

  defp coord_int(value) when is_binary(value) do
    case Float.parse(value) do
      {float, _rest} -> trunc(float)
      :error -> ""
    end
  end

  defp coord_int(_), do: ""

  defp set_coordinate_param(url, coords) do
    uri = URI.parse(url)

    query =
      (uri.query || "")
      |> URI.decode_query()
      |> Map.put("c", coords)
      |> URI.encode_query()

    URI.to_string(%{uri | query: query})
  end
end
