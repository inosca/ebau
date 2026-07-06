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

  @impl true
  def calculate(records, _opts, context) do
    case Ebau.Instances.get_instance_by_id(
           context.arguments.instance_id,
           Keyword.put(Ash.Context.to_opts(context), :load,
             plot_data: [:coord_north, :coord_east]
           )
         ) do
      {:ok, instance} ->
        Enum.map(records, fn gis_link -> replace_placeholder(gis_link, instance) end)

      {:error, %Ash.Error.Query.NotFound{}} ->
        {:error,
         Ash.Error.Query.InvalidArgument.exception(field: :instance_id, message: "not found")}

      {:error, error} ->
        {:error, error}
    end
  end

  defp replace_placeholder(_gis_link, %{plot_data: []}), do: nil

  defp replace_placeholder(gis_link, %{plot_data: [first_plot_data | _rest]}) do
    uri = URI.parse(gis_link.placeholder)

    new_query =
      (uri.query || uri.fragment || "")
      |> URI.decode_query()
      |> replace_query(uri, first_plot_data)
      |> URI.encode_query()

    URI.to_string(%{uri | query: new_query})
  end

  defp replace_query(query_map, %{host: "map.geo.gr.ch"}, first_plot_data) do
    query_map
    |> Map.put("map_x", coord_int(first_plot_data.coord_east))
    |> Map.put("map_y", coord_int(first_plot_data.coord_north))
  end

  defp replace_query(query_map, %{host: "geo.so.ch"}, first_plot_data) do
    Map.put(
      query_map,
      "c",
      "#{coord_int(first_plot_data.coord_east)},#{coord_int(first_plot_data.coord_north)}"
    )
  end

  defp replace_query(query_map, %{host: "map.geo.admin.ch"}, first_plot_data) do
    Map.put(
      query_map,
      "center",
      "#{coord_int(first_plot_data.coord_east)},#{coord_int(first_plot_data.coord_north)}"
    )
  end

  defp replace_query(_, _, _), do: %{}

  defp coord_int(value) when is_integer(value), do: Integer.to_string(value)
  defp coord_int(value) when is_float(value), do: Float.to_string(trunc(value))

  defp coord_int(value) when is_binary(value) do
    case Float.parse(value) do
      {float, _rest} -> Integer.to_string(trunc(float))
      :error -> {:error}
    end
  end
end
