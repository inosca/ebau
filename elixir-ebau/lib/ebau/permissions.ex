defmodule Ebau.Permissions do
  @moduledoc """
  Ash domain for instance-level access control.

  Manages `Ebau.Permissions.InstanceACL` records that grant users access to
  specific building permit instances with time-bounded validity.
  """

  use Ash.Domain

  resources do
    resource Ebau.Permissions.InstanceACL do
      define :grant_acl_for_instance, action: :create
    end
  end
end
