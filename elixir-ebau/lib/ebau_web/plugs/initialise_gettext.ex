defmodule EbauWeb.Plugs.InitialiseGettext do
  @moduledoc """
  Sets the Gettext locale for the current request/LiveView process.

  Works in two modes:

    * as a `Plug` in the browser pipeline — resolves the locale from the
      `accept-language` header (falling back to the session) and stores
      the normalised result in the session
    * as an `on_mount` hook for LiveViews — reads that session value

  Both modes therefore agree on the locale within one navigation.
  Falls back to the default locale (`Ebau.Scope.pick_locale/1`) when
  the source value is missing or unsupported.
  """

  @behaviour Plug

  @impl Plug
  def init(opts), do: opts

  @impl Plug
  def call(conn, _opts) do
    raw_locale =
      case Plug.Conn.get_req_header(conn, "accept-language") do
        [header | _] -> header |> String.split("-") |> List.first()
        [] -> Plug.Conn.get_session(conn, :locale)
      end

    locale = Ebau.Scope.pick_locale(raw_locale)
    Gettext.put_locale(locale)
    Plug.Conn.put_session(conn, :locale, locale)
  end

  def on_mount(_action, _params, session, %{assigns: %{current_user: current_user}} = socket)
      when not is_nil(current_user) do
    lang =
      if current_user.language do
        Atom.to_string(current_user.language)
      else
        session["locale"]
      end

    Gettext.put_locale(Ebau.Scope.pick_locale(lang)) |> dbg()
    {:cont, socket}
  end

  def on_mount(_action, _params, session, socket) do
    dbg(socket)
    Gettext.put_locale(Ebau.Scope.pick_locale(session["locale"]))
    {:cont, socket}
  end
end
