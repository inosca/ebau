defmodule EbauWeb.SessionRevocation do
  @moduledoc """
  Tells connected LiveViews that their session has been revoked.

  `EbauWeb.LiveUserAuth` only checks the token store when a LiveView mounts, so
  without this an already-open tab stays fully interactive after a back-channel
  logout until the user happens to navigate. Revoking broadcasts here and the
  live session redirects itself to sign-in.
  """

  @doc """
  Announces that the session identified by `jti` is no longer valid.
  """
  @spec broadcast(String.t()) :: :ok
  def broadcast(jti) do
    Phoenix.PubSub.broadcast(Ebau.PubSub, topic(jti), :session_revoked)
  end

  @doc """
  Subscribes the calling process to revocations of `jti`.
  """
  @spec subscribe(String.t()) :: :ok | {:error, term()}
  def subscribe(jti), do: Phoenix.PubSub.subscribe(Ebau.PubSub, topic(jti))

  defp topic(jti), do: "session_revocation:#{jti}"
end
