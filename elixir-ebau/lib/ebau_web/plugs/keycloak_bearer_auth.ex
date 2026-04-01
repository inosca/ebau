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
         {:ok, user} <- EbauWeb.OAuth2.fetch_user(token) do
      # todo: properly
      group = Ash.read!(Ebau.User.Group, authorize?: false) |> List.first()
      actor = %{user: user, group: group}
      Ash.PlugHelpers.set_actor(conn, actor)
    else
      _ ->
        conn
    end
  end
end
