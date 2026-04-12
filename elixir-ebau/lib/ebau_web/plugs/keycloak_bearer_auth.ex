defmodule EbauWeb.Plugs.KeycloakBearerAuth do
  @moduledoc """
  Plug that authenticates API requests using Keycloak bearer tokens and stores
  the found user in the conn.
  """

  @behaviour Plug

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
      _ ->
        conn
    end
  end
end
