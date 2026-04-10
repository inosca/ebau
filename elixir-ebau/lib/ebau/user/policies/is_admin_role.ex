defmodule Ebau.User.Policies.IsAdminRole do
  use Ash.Policy.SimpleCheck

  @impl true
  def describe(_options) do
    "The slug of the role of the actor ends with -admin which makes them an admin"
  end

  @impl true
  def match?(%{role: role}, _context, _options) when is_binary(role) do
    String.ends_with?(role, "-admin")
  end

  @impl true
  def match?(_, _, _), do: false
end
