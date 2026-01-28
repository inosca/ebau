defmodule Ebau.Repo do
  use AshPostgres.Repo, otp_app: :ebau

  def installed_extensions do
    ["ash-functions", "citext"]
  end

  def min_pg_version do
    %Version{major: 15, minor: 0, patch: 0}
  end
end
