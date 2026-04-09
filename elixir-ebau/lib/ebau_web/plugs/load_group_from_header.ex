defmodule EbauWeb.Plugs.LoadGroupFromHeader do
  @behaviour Plug

  alias Ebau.User.User

  @impl true
  def init(opts) do
    opts
  end

  @impl true
  def call(conn, _opts) do
    [group_id | _] = Plug.Conn.get_req_header(conn, "x-camac-group")

    # TODO: i'm not sure about this yet
    with %User{} = actor <- Ash.PlugHelpers.get_actor(conn),
         {:ok, group} <- Ebau.User.get_group_for_actor(group_id, actor: actor),
         {:ok, actor} <-
           Ash.load(actor, [:current_group_id, :current_group_service_id],
             context: %{current_group_id: group.id}
           ) do
      conn
      |> Ash.PlugHelpers.set_actor(actor)
      |> Ash.PlugHelpers.set_context(%{group_id: group.id})
    else
      _ ->
        conn
    end
  end
end
