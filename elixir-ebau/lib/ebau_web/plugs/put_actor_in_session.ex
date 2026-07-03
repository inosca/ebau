defmodule EbauWeb.Plugs.PutActorInSession do
  @moduledoc """
  Builds an `%Ebau.Scope{}` (actor + locale) for browser requests and
  stores it on the conn under `:scope` (and `:actor` for convenience in
  templates). Also calls `Ash.PlugHelpers.set_actor/set_context` so
  plain controllers that rely on conn-derived Ash plumbing pick them up.

  Runs after `EbauWeb.Plugs.InitialiseGettext`, so the current locale is
  available via `Gettext.get_locale/1`.
  """

  @behaviour Plug

  require Logger

  @impl true
  def init(opts), do: opts

  @impl true
  def call(conn, _opts) do
    locale = Gettext.get_locale(EbauWeb.Gettext)

    actor =
      case Ebau.Actor.build(conn.assigns[:current_user], locale) do
        {:ok, actor} ->
          actor

        {:error, error} ->
          Logger.warning("Could not build actor: #{inspect(error)}")
          nil
      end

    scope = Ebau.Scope.build(actor, locale)

    conn
    |> Plug.Conn.assign(:actor, scope.actor)
    |> Plug.Conn.assign(:scope, scope)
    |> Ash.PlugHelpers.set_actor(scope.actor)
    |> Ash.PlugHelpers.set_context(%{locale: scope.locale})
  end
end
