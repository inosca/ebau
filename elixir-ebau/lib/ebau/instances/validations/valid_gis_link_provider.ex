defmodule Ebau.Instances.Validations.ValidGisLinkProvider do
  use Ash.Resource.Validation
  use Gettext, backend: EbauWeb.Gettext
  alias Ebau.Instances.GisLink

  @impl true
  def validate(changeset, _opts, _context) do
    uri = URI.parse(Ash.Changeset.get_argument_or_attribute(changeset, :placeholder) || "")

    if GisLink.provider_for_host(uri.host) do
      :ok
    else
      supported_providers_str = GisLink.supported_providers() |> Map.keys() |> Enum.join(", ")

      {:error,
       field: :placeholder,
       message:
         dgettext(
           "errors",
           "Invalid GIS provider. The following providers are supported: %{providers}",
           providers: supported_providers_str
         )}
    end
  end
end
