defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, _context) do
    for record <- records do
      record.placeholder
    end
  end
end
