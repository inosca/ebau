defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  @moduledoc """
  Renders a GIS link placeholder for a concrete instance.

  The calculation loads the instance's plot data and substitutes `{x}` with the
  east coordinate and `{y}` with the north coordinate of the first available plot.
  If no plot data exists, both placeholders are replaced with empty strings.
  """

  use Ash.Resource.Calculation

  # If no instance_id argument is supplied we can't load anything so we just return
  # the records and the link will be nil
  @impl true
  def calculate(records, _opts, %{arguments: %{instance_id: nil}}) do
    Enum.map(records, fn _record -> nil end)
  end

  @impl true
  def calculate(records, _opts, context) do
    action_opts = Ash.Context.to_opts(context)

    instance =
      Ebau.Instances.get_instance_by_id!(
        context.arguments.instance_id,
        Keyword.put(action_opts, :load, plot_data: [:coord_north, :coord_east])
      )

    {x, y} =
      instance.plot_data
      |> List.first()
      |> coordinates()

    Enum.map(records, fn record -> replace_coordinates(record.placeholder, x, y) end)
  end

  defp replace_coordinates(placeholder, x, y) do
    uri = URI.parse(placeholder)

    query =
      (uri.query || "")
      |> URI.decode_query()
      |> Map.put("c", "#{x},#{y}")
      |> URI.encode_query()

    URI.to_string(%{uri | query: query})
  end

  defp coordinates(nil), do: {"", ""}

  defp coordinates(plot) do
    x = plot.coord_east |> String.to_float() |> trunc() |> to_string()
    y = plot.coord_north |> String.to_float() |> trunc() |> to_string()
    {x, y}
  end
end
