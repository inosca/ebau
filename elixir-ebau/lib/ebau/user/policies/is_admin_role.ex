defmodule Ebau.User.Policies.IsAdminRole do
  @moduledoc """
  Policy check that authorizes actors whose role slug ends with `-admin`.

  Used to restrict create/destroy actions on resources like GIS links
  to service administrators.
  """

  use Ash.Policy.SimpleCheck

  @impl true
  def describe(_options) do
    "The slug of the role of the actor ends with -admin which makes them an admin"
  end

  @impl true
  def match?(%{role: %{slug: slug}}, _context, _options) do
    String.ends_with?(slug, "-admin")
  end

  @impl true
  def match?(_, _, _), do: false
end
