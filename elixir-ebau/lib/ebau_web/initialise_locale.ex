defmodule EbauWeb.InitialiseLocale do
  @moduledoc """
  Compares the locale defined in the session (which is taken from the brower accept header) and stores it in the :scope of the socket assigns.
  It also sets the current locale on the Gettext module of the application.

  If the browser sends a locale that is not supported it sets the @fallback_locale.
  """
  import Phoenix.Component, only: [assign: 3]

  @fallback_locale "de"

  def on_mount(_action, _params, session, socket) do
    locale =
      if Enum.member?(Gettext.known_locales(EbauWeb.Gettext), session[:locale]) do
        session[:locale]
      else
        @fallback_locale
      end

    # This sets the locale in the current process (which is the current liveview)
    Gettext.put_locale(locale)

    new_scope = socket.assigns.scope |> Map.put(:locale, locale)

    {:cont, assign(socket, :scope, new_scope)}
  end
end
