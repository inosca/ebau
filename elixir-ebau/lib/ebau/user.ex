defmodule Ebau.User do
  use Ash.Domain, otp_app: :ebau, extensions: [AshJsonApi.Domain]

  resources do
    resource Ebau.User.User do
      define :read_users, action: :read
      define :get_user, get_by: :id, action: :read
      define :get_user_by_email, get_by: :email, action: :read
    end

    resource Ebau.User.Token
    resource Ebau.User.Role

    resource Ebau.User.Group do
      define :get_group_for_actor, get_by: [:id]
    end

    resource Ebau.User.UserGroup

    resource Ebau.User.Service
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
