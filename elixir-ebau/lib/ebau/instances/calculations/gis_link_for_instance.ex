defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  @moduledoc """
  Renders a GIS link placeholder for a concrete instance.

  The calculation loads the instance's plot data and substitutes `{x}` with the
  east coordinate and `{y}` with the north coordinate of the first available plot.
  If no plot data exists, both placeholders are replaced with empty strings.
  """

  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, context) do
    action_opts = Ash.Context.to_opts(context)

    instance =
      Ebau.Instances.get_instance_by_id!(
        context.arguments.instance_id,
        Keyword.put(action_opts, :load, plot_data: [:coord_north, :coord_east])
      )

    {x, y} = coordinates(List.first(instance.plot_data))

    Enum.map(records, fn record ->
      record.placeholder
      |> String.replace("{x}", x)
      |> String.replace("{y}", y)
    end)
  end

  defp coordinates(nil), do: {"", ""}
  defp coordinates(plot), do: {to_string(plot.coord_east), to_string(plot.coord_north)}
end
