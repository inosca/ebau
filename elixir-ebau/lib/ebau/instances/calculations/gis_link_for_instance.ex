defmodule Ebau.Instances.Calculations.GisLinkForInstance do
  @moduledoc """
  Renders a GIS link URL for a concrete instance.

  Sets the provider-specific query parameters (see
  `Ebau.Instances.GisLink.supported_providers/0`) on the configured placeholder
  URL to the truncated east/north coordinates of the instance's first plot.
  Returns nil when no instance_id is supplied; returns the untouched placeholder
  when the instance has no plot data or the placeholder host is not a supported
  provider.
  """

  use Ash.Resource.Calculation

  @impl true
  def calculate(records, _opts, %{arguments: %{instance_id: nil}}) do
    # If we didn't pass an instance the gis link is nil
    Enum.map(records, fn _r -> nil end)
  end

  def calculate(records, _opts, context) do
    case Ebau.Instances.get_instance_by_id(
           context.arguments.instance_id,
           scope: context,
           load: [:dossier_center_coordinates_x, :dossier_center_coordinates_y]
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

  defp replace_placeholder(gis_link, %{
         dossier_center_coordinates_x: coordinate_x,
         dossier_center_coordinates_y: coordinate_y
       })
       when is_nil(coordinate_x) or is_nil(coordinate_y), do: gis_link.placeholder

  defp replace_placeholder(gis_link, %{
         dossier_center_coordinates_x: coordinate_x,
         dossier_center_coordinates_y: coordinate_y
       }) do
    supported_providers = Ebau.Instances.GisLink.supported_providers()
    uri = URI.parse(gis_link.placeholder)
    chosen_provider = Map.get(supported_providers, uri.host)

    if chosen_provider do
      # Some providers carry their query in the fragment (e.g. hash-routed maps).
      original_query = URI.decode_query(uri.query || uri.fragment || "")

      east_str = coord_to_string(coordinate_x)
      north_str = coord_to_string(coordinate_y)

      provider_query =
        Map.new(chosen_provider, fn {param, coordinate_function} ->
          {param, coordinate_function.(east_str, north_str)}
        end)

      query = original_query |> Map.merge(provider_query) |> URI.encode_query()

      URI.to_string(%{uri | query: query})
    else
      gis_link.placeholder
    end
  end

  # The coordinate calculations always yield a float, and the clause above
  # already returned for nil.
  defp coord_to_string(value) when is_float(value), do: Integer.to_string(trunc(value))
end
