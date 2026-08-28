defmodule Ebau.Policies.Checks.ActorIsSystem do
  @moduledoc """
  Policy check that authorizes `Ebau.Scope.System`.

  Used for actions that run on behalf of no user, such as recording or
  revoking sessions during the Keycloak sign-in and logout flows.

      bypass action([:get_token, :set_keycloak_session]) do
        authorize_if Ebau.Policies.Checks.ActorIsSystem
      end
  """

  use Ash.Policy.SimpleCheck

  @impl true
  def describe(_options), do: "The actor is the system"

  @impl true
  def match?(%Ebau.Scope.System{}, _context, _options), do: true
  def match?(_actor, _context, _options), do: false
end
