defmodule Ebau.User.Preparations.RecordKeycloakSession do
  @moduledoc """
  Stores the Keycloak `sid` and the raw `id_token` in `extra_data` of the
  token row created for this sign-in.

  - `sid`: back-channel logout tokens identify the session by it
  - `id_token`: sent as `id_token_hint` on sign-out, otherwise Keycloak >= 26.2
    shows a confirmation screen

  A missing `id_token` or `sid` is logged, not raised: sign-in still works,
  only back-channel logout and the hint are lost for that session.
  """

  use Ash.Resource.Preparation

  require Logger

  @impl true
  def prepare(query, _opts, _context) do
    # `oauth_tokens` is `allow_nil? false`, so it is always a map here.
    id_token = Map.get(query.arguments.oauth_tokens, "id_token")

    Ash.Query.after_action(query, fn _query, users ->
      Enum.each(users, &record(&1, id_token))
      {:ok, users}
    end)
  end

  defp record(user, id_token) do
    with {:ok, sid} <- sid(id_token),
         {:ok, %{"jti" => jti}} <- AshAuthentication.Jwt.peek(user.__metadata__.token),
         {:ok, token} <- Ebau.User.get_token(jti, "user", scope: %Ebau.Scope.System{}) do
      Ebau.User.set_keycloak_session!(token, %{extra_data: %{sid: sid, id_token: id_token}},
        scope: %Ebau.Scope.System{}
      )
    else
      error -> Logger.warning("Not recording the Keycloak session: #{inspect(error)}")
    end
  end

  # `session_state` is the name Keycloak used before it supported `sid`.
  defp sid(nil), do: {:error, :no_id_token}

  defp sid(id_token) do
    case AshAuthentication.Jwt.peek(id_token) do
      {:ok, %{"sid" => sid}} when is_binary(sid) and sid != "" -> {:ok, sid}
      {:ok, %{"session_state" => sid}} when is_binary(sid) and sid != "" -> {:ok, sid}
      {:ok, _claims} -> {:error, :no_sid}
      error -> error
    end
  end
end
