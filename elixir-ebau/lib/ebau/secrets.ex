defmodule Ebau.Secrets do
  @moduledoc false
  use AshAuthentication.Secret

  def secret_for([:authentication, :tokens, :signing_secret], Ebau.User.User, _opts) do
    Application.fetch_env(:ebau, :token_signing_secret)
  end
end
