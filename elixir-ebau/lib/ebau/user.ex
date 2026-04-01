defmodule Ebau.User do
  use Ash.Domain,
    otp_app: :ebau

  resources do
    resource Ebau.User.User do
      define :read_users, action: :read
      define :get_user, get_by: :id, action: :read
    end

    resource Ebau.User.Token
  end
end
