defmodule Ebau.Users do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Ebau.Users.Service
  end
end
