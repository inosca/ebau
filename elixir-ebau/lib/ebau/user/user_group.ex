defmodule Ebau.User.UserGroup do
  @moduledoc false
  use Ash.Resource, domain: Ebau.User, data_layer: AshPostgres.DataLayer

  postgres do
    table "USER_GROUP"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read, :destroy, create: :*, update: :*]
  end

  attributes do
    integer_primary_key :id do
      source :ID
    end

    attribute :default_group, :integer do
      default 0
      source :DEFAULT_GROUP
    end

    attribute :user_id, :integer, allow_nil?: false, source: :USER_ID
    attribute :group_id, :integer, allow_nil?: false, source: :GROUP_ID
  end

  relationships do
    belongs_to :user, Ebau.User.User
    belongs_to :group, Ebau.User.Group
  end
end
