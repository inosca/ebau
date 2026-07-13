defmodule EbauWeb.LocaleController do
  @moduledoc """
  Handles switching the active locale.

  Persists the chosen locale on the user as well as the session.
  """
  use EbauWeb, :controller

  require Logger

  def set_locale(conn, params) do
    scope = conn.assigns[:scope]

    Ebau.User.set_default_language!(scope.actor.user, params["language"], scope: scope)

    conn
    |> put_resp_cookie("language", params["language"],
      path: "/",
      same_site: "Lax",
      http_only: false
    )
    |> redirect(to: params["return_to"])
  end
end
