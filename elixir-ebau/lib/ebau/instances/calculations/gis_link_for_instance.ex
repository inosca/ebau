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
        coords = first_plot_coords(List.first(instance.plot_data))
        Enum.map(records, &set_coordinate_param(&1.placeholder, coords))

      {:error, %Ash.Error.Query.NotFound{}} ->
        {:error,
         Ash.Error.Query.InvalidArgument.exception(field: :instance_id, message: "not found")}

      {:error, error} ->
        {:error, error}
    end
  end

  defp first_plot_coords(nil), do: {:error}

  defp first_plot_coords(plot) do
    case {coord_int(plot.coord_east), coord_int(plot.coord_north)} do
      {{:ok, coord_east}, {:ok, coord_north}} -> {:ok, "#{coord_east},#{coord_north}"}
      _ -> {:error}
    end
  end

  defp coord_int(value) when is_integer(value), do: {:ok, Integer.to_string(value)}
  defp coord_int(value) when is_float(value), do: {:ok, Float.to_string(trunc(value))}

  defp coord_int(value) when is_binary(value) do
    case Float.parse(value) do
      {float, _rest} -> {:ok, Integer.to_string(trunc(float))}
      :error -> {:error}
    end
  end

  defp coord_int(_), do: {:error}

  defp set_coordinate_param(url, {:error}), do: url

  defp set_coordinate_param(url, {:ok, coords}) do
    uri = URI.parse(url)

    query =
      (uri.query || "")
      |> URI.decode_query()
      |> Map.put("c", coords)
      |> URI.encode_query()

    URI.to_string(%{uri | query: query})
  end
end
