defmodule Ebau.Scope do
  @moduledoc false
  defstruct [:current_user, :current_tenant, :locale]

  defimpl Ash.Scope.ToOpts do
    def get_actor(%{current_user: current_user}), do: {:ok, current_user}
    def get_tenant(%{current_tenant: current_tenant}), do: {:ok, current_tenant}
    # TODO Canton
    def get_context(%{locale: locale}), do: {:ok, %{shared: %{locale: locale, canton: :so}}}
    # You typically configure tracers in config files
    # so this will typically return :error
    def get_tracer(_), do: :error

    # This should likely always return :error
    # unless you want a way to bypass authorization configured in your scope
    def get_authorize?(_), do: :error
  end
end
