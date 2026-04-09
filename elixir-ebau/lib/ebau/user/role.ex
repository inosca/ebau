defmodule Ebau.User.Role do
  @moduledoc false
  use Ash.Resource, domain: Ebau.User, data_layer: AshPostgres.DataLayer

  postgres do
    table "ROLE"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]
  end

  attributes do
    integer_primary_key :id, source: :ROLE_ID
    attribute :name, :string, constraints: [max_length: 100], source: :NAME
    attribute :slug, :string
    attribute :group_prefix, :string, constraints: [max_length: 100], source: :GROUP_PREFIX
    attribute :role_parent_id, :integer, source: :ROLE_PARENT_ID, source: :ROLE_PARENT_ID
  end

  relationships do
    belongs_to :role_parent, __MODULE__, source_attribute: :role_parent_id
    has_many :groups, Ebau.User.Group
  end
end
