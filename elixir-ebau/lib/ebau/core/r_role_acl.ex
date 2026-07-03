defmodule Ebau.Core.RRoleAcl do
  @moduledoc """
  Legacy `R_ROLE_ACL` join table between `Ebau.Core.Resource` and
  `Ebau.User.Role`.
  """

  use Ash.Resource, domain: Ebau.Core, data_layer: AshPostgres.DataLayer

  postgres do
    table "R_ROLE_ACL"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]
  end

  attributes do
    integer_primary_key :id, source: :ID

    attribute :resource_id, :integer do
      allow_nil? false
      source :RESOURCE_ID
    end

    attribute :role_id, :integer do
      allow_nil? false
      source :ROLE_ID
    end
  end

  relationships do
    belongs_to :resource, Ebau.Core.Resource
    belongs_to :role, Ebau.User.Role
  end
end
