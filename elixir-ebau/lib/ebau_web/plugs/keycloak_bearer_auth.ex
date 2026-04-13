defmodule EbauWeb.Plugs.KeycloakBearerAuth do
  @moduledoc """
  Plug that authenticates API requests using Keycloak bearer tokens and stores
  the found user in the conn.
  """

  @behaviour Plug

  require Logger

  @impl true
  def init(opts), do: opts

  @impl true
  def call(conn, _opts) do
    with ["Bearer " <> token] <- Plug.Conn.get_req_header(conn, "authorization"),
         [group_id | _] <- Plug.Conn.get_req_header(conn, "x-camac-group"),
         {:ok, user} <- EbauWeb.OAuth2.fetch_user(token),
         {:ok, group} <-
           Ebau.User.get_group_for_actor(group_id, load: [:service, :role], actor: %{user: user}) do
      Ash.PlugHelpers.set_actor(conn, %Ebau.Actor{
        user: user,
        group: group,
        service: group.service,
        role: group.role.slug
      })
    else
      error ->
        Logger.warning("Bearer auth failed: #{inspect(error)}")

        conn
        |> Plug.Conn.put_resp_content_type("application/vnd.api+json")
        |> Plug.Conn.send_resp(
          401,
          JSON.encode!(%{errors: [%{status: "401", title: "Unauthorized"}]})
        )
        |> Plug.Conn.halt()
    end
  end
end
