defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, context) do
    instance =
      Ebau.Instances.get_instance_by_id!(
        context.arguments.instance_id,
        load: [plot_data: [:coord_north, :coord_east]],
        actor: context.actor
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
