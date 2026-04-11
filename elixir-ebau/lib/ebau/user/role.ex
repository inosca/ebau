defmodule Ebau.User.Role do
  @moduledoc false
  use Ash.Resource, domain: Ebau.User, data_layer: AshPostgres.DataLayer

  postgres do
    table "ROLE"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, :destroy, update: :*, create: :*]
  end

  attributes do
    integer_primary_key :id, source: :ROLE_ID

    attribute :name, :string do
      constraints max_length: 100
      source :NAME
    end

    attribute :slug, :string do
      public? true
      source :SLUG
    end

    attribute :group_prefix, :string do
      constraints max_length: 100
      source :GROUP_PREFIX
    end

    attribute :role_parent_id, :integer do
      source :ROLE_PARENT_ID
    end
  end

  relationships do
    belongs_to :role_parent, __MODULE__, source_attribute: :role_parent_id
    has_many :groups, Ebau.User.Group
  end

  identities do
    identity :unique_slug, [:slug]
  end
end
