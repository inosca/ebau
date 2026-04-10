defmodule Ebau.Permissions do
  use Ash.Domain

  resources do
    resource Ebau.Permissions.InstanceACL do
      define :grant_acl_for_instance, action: :create
    end
  end
end
