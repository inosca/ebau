defmodule Ebau.Core.Calculations.Link do
  @moduledoc """
  Maps legacy `RESOURCE.TEMPLATE` paths (PHP `.phtml` entry points) to the
  ember-ebau route the resource lives at today.
  """

  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, _context) do
    Enum.map(records, &ember_ebau_link/1)
  end

  defp ember_ebau_link(%{template: "/ember-camac-ng/dms-admin.phtml"}), do: "/dms-admin"

  defp ember_ebau_link(%{template: "/ember-camac-ng/service-permissions.phtml"}),
    do: "/service-permissions"

  defp ember_ebau_link(%{template: "/ember-camac-ng/gwr-global.phtml"}), do: "/gwr"

  defp ember_ebau_link(%{template: "/ember-camac-ng/communications-global.phtml"}),
    do: "/communications-global"

  defp ember_ebau_link(%{template: "/ember-camac-ng/dossierimport.phtml"}), do: "/dossier-import"

  defp ember_ebau_link(%{template: "/ember-camac-ng/alexandria-search.phtml"}),
    do: "/documents/search"

  defp ember_ebau_link(%{template: "/ember-camac-ng/snippets-admin.phtml"}), do: "/snippets-admin"
  defp ember_ebau_link(%{template: "/ember-camac-ng/snippets.phtml"}), do: "/snippets"
  defp ember_ebau_link(%{template: "/ember-camac-ng/news.phtml"}), do: "/static-content/news"
  defp ember_ebau_link(%{template: "/ember-camac-ng/rulesets.phtml"}), do: "/rulesets"

  defp ember_ebau_link(%{template: "/ember-camac-ng/merge-municipality.phtml"}),
    do: "merge-municipality"

  defp ember_ebau_link(%{template: "/ember-camac-ng/bab-statistics-export.phtml"}),
    do: "/bab-statistics-export"

  defp ember_ebau_link(%{template: "/ember-camac-ng/statistics-export.phtml"}),
    do: "/statistics-export"

  defp ember_ebau_link(%{template: "/dashboard/news.phtml"}), do: "/news"
  defp ember_ebau_link(%{available_resources: "workitemlistall"}), do: "/"

  defp ember_ebau_link(%{available_resources: "emberlist", class_field: "displaySearch"}),
    do: "/cases"

  defp ember_ebau_link(_), do: "/"
end
