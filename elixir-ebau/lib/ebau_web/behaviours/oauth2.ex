defmodule EbauWeb.Behaviours.OAuth2 do
  @moduledoc """
  Behaviour for working with OAuth2 in eBau.
  """

  @doc """
  Accepts a token and returns an eBau user struct or an error with a message.
  """
  @callback fetch_user(binary()) :: {:ok, Ebau.User.User.t()} | {:error, term()}
end
