defmodule Ebau.Scope do
  @moduledoc """
  Bundles per-request auth + presentation state into one value that Ash
  understands natively via the `Ash.Scope.ToOpts` protocol.

  Callers pass `scope: scope` instead of `actor: ...` + `context: ...`;
  Ash unpacks the actor and merges the locale (and anything else we add
  here later) into the action's `source_context`, so expression
  calculations can read it via `context.source_context[:locale]`.

  Built once per request — in the browser plug (`EbauWeb.Plugs.PutActorInSession`)
  and in the LiveView on_mount hook (`EbauWeb.LoadLiveContext`) — so the
  same struct flows through every code path.
  """

  @default_locale "de"

  defstruct [:actor, :locale]

  @type t :: %__MODULE__{actor: Ebau.Actor.t() | nil, locale: String.t()}

  @spec build(Ebau.Actor.t() | nil, String.t() | nil) :: t()
  def build(actor, locale) do
    %__MODULE__{actor: actor, locale: pick_locale(locale)}
  end

  @doc "The fallback locale used when no known locale is set."
  @spec default_locale() :: String.t()
  def default_locale, do: @default_locale

  @doc "Normalises a raw locale (header / session value) to a known one, or the default."
  @spec pick_locale(String.t() | nil) :: String.t()
  def pick_locale(locale) do
    if locale in Gettext.known_locales(EbauWeb.Gettext) do
      locale
    else
      @default_locale
    end
  end

  defimpl Ash.Scope.ToOpts do
    def get_actor(%{actor: actor}), do: {:ok, actor}
    def get_context(%{locale: locale}), do: {:ok, %{locale: locale}}
    def get_tenant(_), do: :error
    def get_tracer(_), do: :error
    def get_authorize?(_), do: :error
  end
end
