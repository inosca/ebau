defmodule EbauWeb.OAuth2Dummy do
  @moduledoc """
  Dummy implementation of the real Keycloak adapter for testing.

  The token in this case is just the user id, example: "1"
  """
  @behaviour EbauWeb.Behaviours.OAuth2

  @impl EbauWeb.Behaviours.OAuth2
  def fetch_user(id) do
    Ebau.User.get_user(id, authorize?: false, actor: nil)
  end
end
