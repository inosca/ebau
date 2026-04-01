defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, context) do
    # gis_links_for_current_service = Ebau.Instances.list_gis_links!(actor: context.actor) |> dbg()

    for record <- records do
      record.placeholder
    end
  end
end
