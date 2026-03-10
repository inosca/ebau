defmodule Ebau.User do
  use Ash.Domain, otp_app: :ebau, extensions: [AshJsonApi.Domain]

  resources do
    resource Ebau.User.User do
      define :read_users, action: :read
      define :get_user, get_by: :id, action: :read
    end

    resource Ebau.User.Token
  end

  json_api do
    routes do
      base_route "/users", Ebau.User.User do
        get :read
        index :read
      end
    end
  end
end
