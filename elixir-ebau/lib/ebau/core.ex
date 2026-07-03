defmodule Ebau.Core do
  @moduledoc """
  Ash domain for legacy CAMAC core tables (`RESOURCE`, `RESOURCE_T`,
  `R_ROLE_ACL`). These tables are owned by the legacy PHP/Django stack and
  are not migrated by Ash (they use `migrate? false`).
  """

  use Ash.Domain, otp_app: :ebau

  authorization do
    authorize :by_default
  end

  resources do
    resource Ebau.Core.Resource do
      define :read_resources, action: :read
    end

    resource Ebau.Core.ResourceT
    resource Ebau.Core.RRoleAcl
  end
end
