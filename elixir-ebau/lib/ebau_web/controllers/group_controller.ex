defmodule EbauWeb.GroupController do
  @moduledoc """
  Handles switching the active group.

  Persists the chosen group as the user's default (picked up on the next
  LiveView mount via `Ebau.Actor.build/2`) and mirrors the selection
  into a `camac_group` cookie for ember consumption. Redirects back to
  the calling page via a sanitised `return_to` param.
  """
  use EbauWeb, :controller

  require Logger

  def switch(conn, params) do
    scope = conn.assigns[:scope]

    with %Ebau.Scope{actor: %Ebau.Actor{}} <- scope,
         {:ok, group} <-
           Ebau.User.get_group_by_id(params["id"], scope: scope, load: [:user_group_for_user]),
         {:ok, _} <- Ebau.User.set_default_user_group(group.user_group_for_user, scope: scope) do
      conn
      |> put_resp_cookie("camac_group", Integer.to_string(group.id),
        path: "/",
        same_site: "Lax",
        http_only: false
      )
      |> redirect(to: safe_return_to(params["return_to"]))
    else
      other ->
        Logger.warning("Group switch failed: #{inspect(other)}")
        redirect(conn, to: safe_return_to(params["return_to"]))
    end
  end

  defp safe_return_to(path) when is_binary(path) do
    if String.starts_with?(path, "/") and not String.starts_with?(path, "//") and
         not String.starts_with?(path, "/auth/") do
      path
    else
      "/"
    end
  end

  defp safe_return_to(_), do: "/"
end
