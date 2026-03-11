defmodule EbauWeb.OAuth2 do
  alias Assent.Strategy.OAuth2

  defp config do
    [
      client_id: "camac",
      client_secret: "dont-need",
      auth_method: :client_secret_post,
      base_url: "http://ebau-keycloak.localhost/auth/",
      authorization_params: [scope: "user:read user:write"],
      user_url:
        "http://ebau-keycloak.localhost/auth/realms/ebau/protocol/openid-connect/userinfo",
      redirect_uri: "http://localhost:4000/auth/callback"
    ]
  end

  @spec fetch_user(binary()) :: {:ok, Ebau.User.User.t()} | nil
  def fetch_user(token) do
    case OAuth2.fetch_user(config(), %{"access_token" => token}) do
      {:ok, %{"email" => email}} ->
        # Here it is safe to use authorize? false since what is in the token is validated
        # by keycloak. If we managed to get a valid, certified token with a claims["email"]
        # of another user we have other problems.
        Ebau.User.get_user_by_email(email, authorize?: false)

      _ ->
        nil
    end
  end
end
