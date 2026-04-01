defmodule Ebau.User.UserGroup do
  @moduledoc false
  use Ash.Resource, domain: Ebau.User, data_layer: AshPostgres.DataLayer

  postgres do
    table "USER_GROUP"
    repo Ebau.Repo
    migrate? false
  end

  actions do
    defaults [:read]
  end

  attributes do
    integer_primary_key :id do
      source :ID
    end
    attribute :user_id, :integer, source: :USER_ID
    attribute :group_id, :integer, source: :GROUP_ID
  end

  relationships do
    belongs_to :user, Ebau.User.User
    belongs_to :group, Ebau.User.Group
  end
end
