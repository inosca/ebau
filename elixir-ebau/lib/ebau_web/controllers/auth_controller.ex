defmodule EbauWeb.AuthController do
  use EbauWeb, :controller
  use AshAuthentication.Phoenix.Controller

  alias AshAuthentication.Errors.AuthenticationFailed

  require Logger

  def success(conn, activity, user, _token) do
    return_to = get_session(conn, :return_to) || "/"

    message =
      case activity do
        {:confirm_new_user, :confirm} -> "Your email address has now been confirmed"
        {:password, :reset} -> "Your password has successfully been reset"
        _ -> "You are now signed in"
      end

    conn
    |> delete_session(:return_to)
    |> store_in_session(user)
    |> assign(:current_user, user)
    |> put_flash(:info, message)
    |> redirect(to: return_to)
  end

  def sign_in(conn, _params) do
    redirect(conn, external: ~p"/elixir/auth/user/ebau")
  end

  def failure(conn, activity, reason) do
    Logger.warning("""
    Authentication failed: #{describe_failure(reason)}
      activity: #{inspect(activity)}
    """)

    message =
      case {activity, reason} do
        {_,
         %AuthenticationFailed{
           caused_by: %Ash.Error.Forbidden{
             errors: [%AshAuthentication.Errors.CannotConfirmUnconfirmedUser{}]
           }
         }} ->
          """
          You have already signed in another way, but have not confirmed your account.
          You can confirm your account using the link we sent to you, or by resetting your password.
          """

        _ ->
          "Incorrect email or password"
      end

    conn
    |> put_flash(:error, message)
    |> redirect(to: ~p"/elixir/sign-in")
  end

  defp describe_failure(%AuthenticationFailed{caused_by: caused_by}),
    do: describe_failure(caused_by)

  defp describe_failure(exception) when is_exception(exception), do: Exception.message(exception)
  defp describe_failure(%{message: message}) when is_binary(message), do: message
  defp describe_failure(other), do: inspect(other)

  @doc """
  Signs the user out of Phoenix and then out of Keycloak.

  Clearing the local session alone is not enough: Keycloak's SSO cookie would
  survive and silently re-authenticate the user on the next protected page.

  This is deliberately a `GET` reached from a plain link, which accepts logout
  CSRF.
  """
  @spec sign_out(Plug.Conn.t(), map()) :: Plug.Conn.t()
  def sign_out(conn, _params) do
    query =
      conn
      |> session_token()
      |> logout_params()
      |> Keyword.put(:post_logout_redirect_uri, url(~p"/elixir/sign-in"))
      |> URI.encode_query()

    conn
    |> clear_session(:ebau)
    |> redirect(external: Ebau.Secrets.end_session_url() <> "?" <> query)
  end

  # Keycloak 26.2+ only skips its logout confirmation screen for a request
  # carrying a signed `id_token_hint`. It verifies the signature and token type
  # but not expiry so the token minted at login stays usable for the life of
  # the session. `client_id` is the fallback when we never received one, and
  # still logs the user out just by way of the confirmation screen.
  #
  # The `id_token` is dropped from the row on the way out: `clear_session/2`
  # turns the row into a revocation record that is never expunged.
  @spec logout_params(Ash.Resource.record() | nil) :: keyword()
  defp logout_params(%{extra_data: %{"id_token" => id_token}} = token) when is_binary(id_token) do
    Ebau.User.set_keycloak_session!(token, %{extra_data: nil}, scope: %Ebau.Scope.System{})
    [id_token_hint: id_token]
  end

  defp logout_params(_token), do: [client_id: Ebau.Secrets.client_id()]

  @spec session_token(Plug.Conn.t()) :: Ash.Resource.record() | nil
  defp session_token(conn) do
    with token when is_binary(token) <- get_session(conn, "user_token"),
         {:ok, %{"jti" => jti}} <- AshAuthentication.Jwt.peek(token),
         {:ok, row} <- Ebau.User.get_token(jti, "user", scope: %Ebau.Scope.System{}) do
      row
    else
      _ -> nil
    end
  end
end
