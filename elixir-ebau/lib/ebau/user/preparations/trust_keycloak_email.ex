defmodule Ebau.User.Preparations.TrustKeycloakEmail do
  @moduledoc """
  Overwrites the `email_verified` claim with `true` for the `sign_in_with_ebau`
  action.

  `AshAuthentication` won't link a username to an existing account unless the
  provider says the email is verified. Django has no such rule, so honouring the
  claim would lock users out of the elixir app only.
  """

  use Ash.Resource.Preparation

  @impl true
  def prepare(query, _opts, _context) do
    user_info = Ash.Query.get_argument(query, :user_info)

    Ash.Query.set_argument(query, :user_info, Map.put(user_info, "email_verified", true))
  end
end
