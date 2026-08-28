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

    # No `require_actor?` here: AshAuthentication resolves the session user
    # via `subject_to_user/3` without an actor (covered by the
    # AshAuthenticationInteraction bypass on the User resource).
  end

  resources do
    resource Ebau.User.User do
      define :create_user, action: :create
      define :read_users, action: :read
      define :get_user, get_by: :id, action: :read
      define :get_user_by_email, get_by: :email, action: :read
      define :get_user_by_username, get_by: :username, action: :read
      define :set_default_language, args: [:language]
    end

    resource Ebau.User.Token do
      define :get_token, action: :get_token, args: [:jti, :purpose]
      define :session_tokens_by_keycloak_sid, action: :by_keycloak_sid, args: [:sid]
      define :set_keycloak_session, action: :set_keycloak_session
    end

    resource Ebau.User.Role do
      define :create_role, action: :create
    end

    resource Ebau.User.Group do
      define :create_group
      define :get_group_for_actor, get_by: [:id]
      define :get_group_by_id, get_by: [:id], action: :read
    end

    resource Ebau.User.GroupT

    resource Ebau.User.UserGroup do
      define :set_default_user_group
      define :clear_default_user_group
    end

    resource Ebau.User.Service do
      define :create_service
    end

    resource Ebau.User.ServiceGroup do
      define :get_service_group_by_slug, action: :read, get_by: [:slug]
    end

    resource Ebau.User.UserIdentity
  end
end
