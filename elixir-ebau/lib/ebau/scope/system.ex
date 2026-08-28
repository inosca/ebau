defmodule Ebau.Scope.System do
  @moduledoc """
  Scope for server-side work on behalf of no user: sign-in bookkeeping,
  Keycloak back-channel logout, scheduled jobs.

  Doubles as the actor, so policies can grant it per action with
  `Ebau.Policies.Checks.ActorIsSystem`. Use this instead of
  `authorize?: false`: policies still run and the grant shows up in the
  policy breakdown.

      Ebau.User.get_token(jti, "user", scope: %Ebau.Scope.System{})
  """

  defstruct []

  @type t :: %__MODULE__{}

  defimpl Ash.Scope.ToOpts do
    def get_actor(scope), do: {:ok, scope}
    def get_context(_), do: {:ok, %{locale: Ebau.Scope.default_locale()}}
    def get_tenant(_), do: :error
    def get_tracer(_), do: :error
    def get_authorize?(_), do: :error
  end
end
