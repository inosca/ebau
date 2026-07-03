defmodule EbauWeb.LoadLiveContext do
  @moduledoc """
  Single `on_mount` hook that assembles all session-derived context for
  authenticated LiveViews.

  Assigns set on the socket:

    * `:actor` — `%Ebau.Actor{}` or `nil` when the user belongs to no groups
    * `:scope` — `%Ebau.Scope{}` bundling actor + locale (always present)
    * `:resources` — navbar resource navigation entries
    * `:current_path` — updated on every `handle_params` via `attach_hook/4`
  """
  import Phoenix.Component, only: [assign: 3]
  import Phoenix.LiveView, only: [attach_hook: 4]

  require Logger

  def on_mount(_action, _params, _session, socket) do
    locale = Gettext.get_locale(EbauWeb.Gettext)

    actor =
      case Ebau.Actor.build(socket.assigns[:current_user], locale) do
        {:ok, actor} ->
          actor

        {:error, error} ->
          Logger.warning("Could not build actor: #{inspect(error)}")
          nil
      end

    scope = Ebau.Scope.build(actor, locale)

    socket =
      socket
      |> assign(:actor, scope.actor)
      |> assign(:scope, scope)
      |> assign(:resources, load_resources(scope))
      |> attach_hook(:track_current_path, :handle_params, &track_path/3)

    {:cont, socket}
  end

  defp load_resources(%Ebau.Scope{actor: nil}), do: []

  defp load_resources(scope) do
    Ebau.Core.read_resources!(scope: scope, load: [:name, :link])
  end

  defp track_path(_params, uri, socket) do
    %URI{} = uri = URI.new!(uri)
    path = %{uri | scheme: nil, host: nil, port: nil, authority: nil, userinfo: nil}
    {:cont, assign(socket, :current_path, URI.to_string(path))}
  end
end
