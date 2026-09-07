defmodule Ebau.Mailer.Config do
  @moduledoc """
  Builds the mail configuration from the environment.

  Called from `config/runtime.exs`, which is evaluated before the application
  starts, so nothing in here may depend on runtime state.
  """

  @doc """
  Parses `ADMINS` into recipients. Uses the same pattern as django's
  `parse_admins`, so a value django boots with never makes this raise.
  """
  def admins(value \\ System.get_env("ADMINS", "")) do
    value
    |> String.split(",", trim: true)
    |> Enum.map(fn admin ->
      case Regex.run(~r/(.+) <(.+@.+)>/, admin) do
        [_, name, address] ->
          {String.trim(name), address}

        nil ->
          raise """
          In ADMINS the admin "#{admin}" is not in the correct format \
          "Firstname Lastname <email@example.com>"
          """
      end
    end)
  end

  @doc """
  Swoosh options for the relay in `EMAIL_HOST`, or the local adapter, which
  keeps mails in memory instead of sending them, when there is no relay.
  """
  def adapter(env \\ System.get_env())

  def adapter(%{"EMAIL_HOST" => host} = env) do
    # Mirrors django's SMTP backend: connect straight to EMAIL_HOST instead of
    # doing an MX lookup, which would fail for a relay like `mailpit`.
    [
      adapter: Swoosh.Adapters.SMTP,
      relay: host,
      port: String.to_integer(Map.get(env, "EMAIL_PORT", "25")),
      tls: if(Map.get(env, "EMAIL_USE_TLS", "false") in ~w(true 1), do: :always, else: :never),
      no_mx_lookups: true,
      retries: 1
    ] ++ credentials(env)
  end

  def adapter(_env), do: [adapter: Swoosh.Adapters.Local]

  # The adapter rejects a nil username, so credentials are only added when the
  # relay needs them.
  defp credentials(%{"EMAIL_HOST_USER" => user, "EMAIL_HOST_PASSWORD" => password} = _env) do
    [auth: :always, username: user, password: password]
  end

  defp credentials(_env), do: [auth: :never]
end
