defmodule Ebau.User do
  @moduledoc """
  Ash domain for users, roles, groups, services, and service groups.

  This domain wraps the legacy CAMAC user tables (`USER`, `ROLE`, `GROUP`,
  `SERVICE`, `SERVICE_GROUP`, `USER_GROUP`). These tables are owned by
  Django and are not migrated by Ash (they use `migrate? false`).
  """

  use Ash.Domain, otp_app: :ebau

  authorization do
    authorize :by_default
  end

  resources do
    resource Ebau.User.User do
      define :create_user, action: :create
      define :read_users, action: :read
      define :get_user, get_by: :id, action: :read
      define :get_user_by_email, get_by: :email, action: :read
    end

    resource Ebau.User.Token

    resource Ebau.User.Role do
      define :create_role, action: :create
    end

    resource Ebau.User.Group do
      define :create_group
      define :get_group_for_actor, get_by: [:id]
    end

    resource Ebau.User.UserGroup

    resource Ebau.User.Service do
      define :create_service
    end

    resource Ebau.User.ServiceGroup do
      define :get_service_group_by_slug, action: :read, get_by: [:slug]
    end
  end
end
