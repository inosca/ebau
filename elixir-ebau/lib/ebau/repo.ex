defmodule Ebau.Repo do
  use Ecto.Repo,
    otp_app: :ebau,
    adapter: Ecto.Adapters.Postgres
end
